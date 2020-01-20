from colorama import Fore, Back, Style
from collections import defaultdict
import statistics
import z
import buy

cidx = 0
use_percentages = list()
gavgs = list()
currentsort = 0
ivv = 0
iusg = 0
reversing = False
avgidx = False

def store(values):
    global cidx
    res = list(zip(*values))
    if not store.title:
        store.title = res[0]
    store.items[cidx].append(res[1])
store.items = defaultdict(list)
store.title = None

from sortedcontainers import SortedSet
def getItems():
    global currentsort, reversing

#    if currentsort >= len(store.items[cidx]):
#        currentsort = 0

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

    realret = list()
    if not reversing: 
        for item in ret:
            realret.append(item[1])
    else:
        for item in reversed(ret):
            realret.append(item[1])
    return realret

mm = dict()
titles = dict()
dates = z.getp("dates")
clist = list()
def printTable(tablename ="default"):
    global cidx, mm, ivv, iusg, clist, avgidx
    headerWidths = defaultdict(int)

    if cidx not in titles:
        titles[cidx] = tablename
    print ("\n=== " , titles[cidx] , dates[-1], "===")

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
            width = len(str(individual))
            if ctitle in use_percentages and type(individual) is float:
                width = len(str(round(individual,2))) + 3

            if width > headerWidths[ctitle]:
                headerWidths[ctitle] = width

    mm = dict()
    for key in dics.keys():
        ctitle = store.title[key]
        try:
            m1 = round(min(dics[key]),3)
            m2 = round(max(dics[key]),3)
            avg = round(statistics.mean(dics[key]),3)

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
    print(Fore.GREEN + Style.BRIGHT + "  ".join(headeritems) + Style.RESET_ALL)

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

        saveme = list()
        have = False

        if not x % 40 and x > 0:
            print(Fore.GREEN + Style.BRIGHT + "  ".join(headeritems) + Style.RESET_ALL)

        for j, individual in enumerate(items):
            if j == 0 and individual[0] == '*':
                have = True
            if not individual:
                individual = "NA"
            modifier = None
            ctitle = store.title[j]

            if individual == "NA":
                individual = ""

            bar = "{:>" + "{}".format(headerWidths[ctitle]) + "}"
            updated = False
            try:
                if individual != "NA" and j != 0 and type(individual) != str:
                    if individual == mm[j][0]:
                        bar = Fore.YELLOW + "{:>" + "{}".format(headerWidths[ctitle]) + "}"
                        updated = True
                    elif individual == mm[j][1]:
                        if have:
                            bar = Fore.GREEN + "{:>" + "{}".format(headerWidths[ctitle]) + "}"
                        else:
                            bar = Fore.GREEN + "{:>" + "{}".format(headerWidths[ctitle]) + "}"
                        updated = True
            except:
                print ("asdfa")
                pass
    
#            if individual == "NA":
#                individual = Style.DIM + individual

            if updated:
                bar = bar + Style.RESET_ALL
                if have:
                    bar = bar + Back.LIGHTBLACK_EX

            try:
                if ctitle in use_percentages:
                    saveme.append(bar.format(z.percentage(individual)))
                else:
                    saveme.append(bar.format(individual))
            except:
                print ("problem with {} {}".format(ctitle, individual))
                exit()

        saveme.append("{:>3}".format(str(x)))
        if not have:
            print("  ".join(saveme))
        else:
            print(Back.LIGHTBLACK_EX + "  ".join(saveme) + Style.RESET_ALL)

    avgs = list()
    for i,ctitle in enumerate(store.title):
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
                avgs.append(bar.format(z.percentage(val)))
            else:
                avgs.append(bar.format(val))
        except:
            pass

    print(Fore.GREEN + Style.BRIGHT + "  ".join(avgs) + Style.RESET_ALL  + "\nStocks Shown: " +str(len(store.items[cidx])))
    if not ivv:
        bar, bar, ivv, bar = buy.getYearly2("IVV")
        bar, bar, iusg, bar = buy.getYearly2("IUSG")
        ivv = z.percentage(ivv)
        iusg = z.percentage(iusg)
    print("IVV:  {}\nIUSG: {}".format(ivv, iusg))

lastf = 0
def initiate():
    global cidx
    global currentsort
    global clist
    global reversing
    global avgidx, lastf
    import readchar
    import os

    cidx = 0
    os.system("clear")
    printTable()

#    os.system("powershell.exe /c start firefox.exe ")
#    exit()
    key = readchar.readkey()
    while (key != "q"):
        avgidx = None
        try:
            if key == "p":
                cidx -= 1
                if cidx not in store.items:
                    cidx = 0
                os.system("clear")
                printTable()

            elif key == "n":
                cidx += 1
                if cidx not in store.items:
                    cidx = 0
                os.system("clear")
                printTable()

            elif key == "p":
                os.system("clear")
                printTable()

            elif key == "a":
                avgidx = True
                os.system("clear")
                printTable()

            elif key == "g":
                ticker = clist[0]
                webpage = 'https://snapshot.fidelity.com/fidresearch/snapshot/landing.jhtml#/research?symbol={}&appCode='.format(ticker)
                os.system("powershell.exe /c start firefox.exe \"'{}'\"".format(webpage))

            elif key == "r":
                reversing = not reversing
                os.system("clear")
                printTable()

            elif key == "s":
                bar = input("Enter Column: ")
                currentsort = store.title.index(bar)
                print("currentsort : {}".format( currentsort ))
                os.system("clear")
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
                os.system("clear")
                printTable()

            elif key == "-":
                currentsort = currentsort - 1
                os.system("clear")
                printTable()

            elif int(key):
                currentsort = int(key) - 1
                os.system("clear")
                printTable()
        except:
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


