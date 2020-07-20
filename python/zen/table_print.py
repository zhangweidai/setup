from colorama import Fore, Back, Style
from collections import defaultdict
import statistics
import z
import buy
import os
import current
import args

mode = 0
titleColor = Fore.YELLOW
color = Fore.CYAN
accurate = True
g_allow_clearing = True
cidx = 0

use_percentages = set()
use_often = set()

use_percentages2 = set()
use_often2 = set()

gavgs = list()
currentsort = 0
ivv = 0
iusg = 0
reversing = False
avgidx = False
#def setArgs(largs):
#    global args
#    args = largs
#
def store(values):
    if args.args.bta:
        return
    global cidx
    res = list(zip(*values))
    if not store.title:
        store.title = res[0]
        for item in values:
            if len(item) != 3:
                continue

            if item[-1] == '%':
                use_percentages.add(item[0])
            else:
                use_often.add(item[0])

    store.items[cidx].append(res[1])

store.items = defaultdict(list)
store.title = None

use_stock_order = False
from sortedcontainers import SortedSet
stock_order = list()
def getItems():
    global currentsort, reversing, use_stock_order, stock_order

#    if currentsort >= len(store.items[cidx]):
#        currentsort = 0

    if use_stock_order and stock_order:
        realret = list()
        for stock in stock_order:
            if stock[0] == "*":
                stock = stock[1:]
            for item in store.items[cidx]:
                citem = item[0]
                if citem[0] == "*":
                    citem = citem[1:]
                if citem == stock:
                    realret.append(item)
                    break
        return realret
  
    ret = SortedSet()
    for item in store.items[cidx]:
        bar = item[currentsort]
        if type(bar) is str:
            try:
                bar = float(bar)
            except:
                try:
                    bar = float(bar[:-1])
                except:
                    bar = 0
                    pass
        if not bar:
            bar = 0
        ret.add((bar, item))

    if reversing:
        ret = reversed(ret)

    stock_order = list()
    realret = list()
    for item in ret:
        stock_order.append(item[1][0])
        realret.append(item[1])
    return realret

mm = dict()
titles = dict()
dates = z.getp("dates")
clist = list()
def printTable(tablename ="default"):

    if args.args.bta:
        return
    global g_allow_clearing, accurate

#    try:
    if args.args.nc == False and g_allow_clearing:
        os.system("clear")
#        print ("parsing here")
#        if args.nc == False and g_allow_clearing:
#            os.system("clear")

    global cidx, mm, ivv, iusg, clist, avgidx
    headerWidths = defaultdict(int)

    if cidx not in titles:
        titles[cidx] = tablename
    print ("\n=== " , titles[cidx] , dates[-1], "\t\t5:", dates[-5], "\t\t15:", dates[-15], "\t\t30:", dates[-30], "\t\t50:", dates[-50], " \t100:", dates[-100], "===")

    # determine headerWidths
    dics = defaultdict(list)
    for items in store.items[cidx]:
        for j, individual in enumerate(items):
            ctitle = store.title[j]
            if type(individual) is str and "%" in individual:
                try:
                    dics[j].append(float(individual.split("%")[0]))
                except:
                    pass
            elif type(individual) is not str:
                dics[j].append(individual)
            ctitle_len = len(ctitle)
            width = max((len(str(individual)),  ctitle_len))
            if ctitle in use_percentages and type(individual) is float:
                useme = z.percentage(individual, accurate=accurate)
                width = max((len(str(useme)) + 1, ctitle_len))

            if width > headerWidths[ctitle]:
                headerWidths[ctitle] = width

    mm = dict()
    for key in dics.keys():
        ctitle = store.title[key]

        if ctitle == "pd1":
            print("ctitle : {}".format( ctitle ))

        try:
            m1 = round(min(dics[key]),3)
            m2 = round(max(dics[key]),3)

            roundme = 1 if ctitle not in use_percentages else 3
            if ctitle in use_often:
                roundme = 2
            avg = round(statistics.mean(dics[key]),roundme)
            if ctitle == "pd1":
                print("ctitle : {}".format( ctitle ))
                print("dics: {}".format( dics[key]))
                print("avg : {}".format( avg ))
            width = len(str(avg))
            if width > headerWidths[ctitle]:
                headerWidths[ctitle] = width
            mm[key] = (m1, m2, avg)
        except:
            mm[key] = ("NA","NA", "NA")
            pass

    headeritems = list()
    for ctitle in store.title:
        width = headerWidths[ctitle]
        bar = "{:>" + "{}".format(width) + "}"
        headeritems.append(bar.format(ctitle[:width]))

    print("cidx: {} \tSorting By : '{}' ({})".format( cidx, store.title[currentsort], currentsort))
    print(titleColor + Style.BRIGHT + "  ".join(headeritems) + Style.RESET_ALL)

#    try:
#        bar = getItems()
#        print("bar : {}".format( bar ))
#    except Exception as e:
#        z.trace(e)
    clist = list()
    for x,items in enumerate(getItems()):
        skipping = False
        try:
            if avgidx:
                for avgname in gavgs:
                    idx = store.title.index(avgname)
                    try:
                        if items[idx] < mm[idx][2]:
                            skipping = True
                            break
                    except:
                        pass
        except Exception as e:
            pass

        if skipping:
            continue

        clist.append(items[0].replace("*", ""))

        joinme = list()
        have = False

        if not x % 40 and x > 0:
            print(titleColor + Style.BRIGHT + "  ".join(headeritems) + Style.RESET_ALL)

        for j, individual in enumerate(items):
            if j == 0 and individual[0] == '*':
                have = True
            if not individual:
                individual = "NA"
            modifier = None
            ctitle = store.title[j]

            if individual == "NA":
                individual = ""

            ctitle_width = headerWidths[ctitle]
            bar = None
            if have and j == 0:
                bar = Back.LIGHTBLACK_EX + "{:>" + "{}".format(ctitle_width) + "}"
            else:
                bar = "{:>" + "{}".format(ctitle_width) + "}"
            updated = False
            try:
                if individual != "NA" and j != 0 and type(individual) != str:
                    if individual == mm[j][0]:
                        bar = color + "{:>" + "{}".format(ctitle_width) + "}"
                        updated = True
                    elif individual == mm[j][1]:
                        bar = titleColor + "{:>" + "{}".format(ctitle_width) + "}"
                        updated = True
            except:
                pass
    
#            if individual == "NA":
#                individual = Style.DIM + individual

            if updated or (have and j == 0):
                bar = bar + Style.RESET_ALL
#                if have and j == 0:
#                    bar = bar + Back.LIGHTBLACK_EX

            try:
                if ctitle in use_percentages:
                    useme = z.percentage(individual, accurate=accurate)
                    if len(useme) > ctitle_width:
                        print("ctitle_width: {}".format( ctitle_width))
                        print("useme : {}".format( len(useme)))
                        print("ctitle: {}".format( ctitle))
                        exit()
                    joinme.append(bar.format(useme))
                elif ctitle in use_often:
                    try:
                        joinme.append(bar.format("{}%".format(round(individual*100,2))))
                    except:
                        joinme.append(bar.format(individual))
                else:
                    joinme.append(bar.format(individual))
            except:
                print ("problem with {} {}".format(ctitle, individual))
                exit()


        joinme.append("{:>3}".format(str(x)))
#        if not have:
#        print("  ".join(joinme))
#        else:
        print("  ".join(joinme))

    avgs = list()
    for i, ctitle in enumerate(store.title):
        width = headerWidths[ctitle]
        bar = "{:>" + "{}".format(width) + "}"
        val = ""
        if i >= 1:
            try:
                val = mm[i][2]
            except:
                val = ""

        try:
            if ctitle in use_percentages:
                useme = z.percentage(val)
                useme = useme[:width]
                avgs.append(bar.format(useme))

            elif ctitle in use_often:
                avgs.append(bar.format("{}%".format(val)))
            else:
                avgs.append(bar.format(val))
        except:
            pass

    print(titleColor + Style.BRIGHT + "  ".join(avgs) + Style.RESET_ALL  + "\nStocks Shown: " +str(len(store.items[cidx])))
    if not ivv:
        for anetf in ["IVV", "IUSG", "VUG"]:
            y1pu, ivvb, wc, bc, avg, ly, l2y, avg8, dfh1y, gfl1y = buy.getFrom("probs", anetf)
            print("{:>4}:  {:>5} wc:{:>5} bc:{:>5}: avg:{:>5}, avg8:{:>5}".format(anetf, z.percentage(ly), z.percentage(wc), z.percentage(bc), z.percentage(avg), z.percentage(avg8), z.percentage(dfh1y), z.percentage(gfl1y)))

def resetAll():
    global use_percentages, use_often
    global use_percentages2, use_often2, currentsort
    use_percentages, use_percentages2 = use_percentages2, use_percentages
    use_often, use_often2 = use_often2, use_often
    store.items = defaultdict(list)
    store.title = None
    currentsort = 0

lastf = 0
def initiate(allow_clearing = True):
    if args.args.bta:
        return
    global cidx
    global currentsort
    global clist
    global reversing
    global avgidx, lastf
    global g_allow_clearing
    global mode
    global use_stock_order
    allow_clearing = g_allow_clearing
    import readchar
    import os

    cidx = 0
    printTable()

#    os.system("powershell.exe /c start firefox.exe ")
#    try:
#        print ("no keyd")
#        if args.nc:
##            exit()
#    except Exception as e:
#        z.trace(e)

    try:
        key = readchar.readkey()
    except:
        print ("no key")
        key = None
    while (key != "q"):
        use_stock_order = False
        avgidx = None
        try:
            if key == "p":
                cidx -= 1
                if cidx not in store.items:
                    cidx = 0
                printTable()

            elif key == "n":
                cidx += 1
                if cidx not in store.items:
                    cidx = 0
                printTable()

            elif key == "p":
                printTable()

            elif key == "a":
                avgidx = True
                printTable()

            elif key == "c":
                import stock_plot
                stock_plot.preplot(clist)

#            elif key == "g":
#                ticker = clist[0]
#                webpage = 'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/research?symbol={}&appCode='.format(ticker)
#                os.system("powershell.exe /c start firefox.exe \"'{}'\"".format(webpage))

            elif key == "r":
                reversing = not reversing
                printTable()

            elif key == "g":
                import sys
                python = sys.executable
                types = titles[cidx]
                os.execl(python, python, "stock_plot.py", types)

            elif key == "s":
                bar = input("Enter Column: ")
                currentsort = store.title.index(bar)
                print("currentsort : {}".format( currentsort ))
                printTable()

            elif key == "w":
                stocks = [ bar[0].replace("*", "") for bar in store.items[0] ]
                resetAll()
                g_allow_clearing = False
                use_stock_order = True

                if mode == 0:
                    current.procs(stocks)
                    mode += 1
                else:
                    for astock in stocks:
                        buy.single(astock)
                    mode -= 1

                cidx = 0
                printTable()

            elif key == "l":
                ticker = clist[-1]
                webpage = 'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/research?symbol={}&appCode='.format(ticker)
                os.system("powershell.exe /c start firefox.exe \"'{}'\"".format(webpage))

            elif key == "f" or key == "z" or key == "c" or key == 'x':
                bar = input("Enter idx: ")
                try:
                    if "q" in bar:
                        exit()
                    idx = int(bar)
                except: 
                    idx = lastf
                lastf = idx

                if "q" in bar:
                    exit()

                ticker = clist[idx]
                print("ticker : {}".format( ticker ))
#                webpage = "https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/research?symbol={}&appCode=".format(ticker)
                webpage = 'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/research?symbol={}&appCode='.format(ticker)
                if key == "z":
                    webpage = 'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/financials?stockspage=financials&symbol={}&period=quarterly'.format(ticker)
                if key == "x":
                    webpage = 'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/financials?stockspage=incomestatement&symbol={}&period=quarterly'.format(ticker)
                if key == "c":
                    webpage = 'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/financials?stockspage=cashflow&symbol={}&period=quarterly'.format(ticker)
                os.system("powershell.exe /c start firefox.exe \"'{}'\"".format(webpage))

            elif key == "=":
                currentsort = currentsort + 1
                if args.args.nc == False and allow_clearing:
                    os.system("clear")
                printTable()

            elif key == "-":
                currentsort = currentsort - 1
                if args.args.nc == False and allow_clearing:
                    os.system("clear")
                printTable()

            elif int(key):
                currentsort = int(key) - 1
                if args.args.nc == False and allow_clearing:
                    os.system("clear")
                printTable()
        except Exception as e:
            args.restart_program()
            pass

        key = readchar.readkey()

def clearTable():
    global cidx
    cidx += 1
#    store.items = list()

if __name__ == '__main__':
    values = [
        ("Title",  "b"),
        ("Title1", 3),
        ("Title2", 220.00)]
    store(values)
    values = [
        ("Title",  "name2"),
        ("Title1", 23),
        ("Title2", 3220.00)]
    store(values)
    values = [
        ("Title",  "a"),
        ("Title1", 123),
        ("Title2", 20.00)]
    store(values)
    printTable()
    clearTable()
    values = [
        ("Title",  "huh"),
        ("Title1", 123),
        ("Title2", 20.00)]
    store(values)
    printTable()

    initiate()


