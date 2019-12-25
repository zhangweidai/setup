from colorama import Fore, Back, Style
from collections import defaultdict
import statistics
import z

cidx = 0
use_percentages = list()
currentsort = 0

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
    global currentsort

    if currentsort >= len(store.items[cidx]):
        currentsort = 0

    ret = SortedSet()
    for item in store.items[cidx]:
        ret.add((item[currentsort], item))

    realret = list()
    for item in ret:
        realret.append(item[1])
    return realret

mm = dict()
titles = dict()
dates = z.getp("dates")
def printTable(tablename ="default"):
    global cidx, mm
    headerWidths = defaultdict(int)

    if cidx not in titles:
        titles[cidx] = tablename
    print ("\n=== " , titles[cidx] , dates[-1], "===")

    # determine headerWidths
    dics = defaultdict(list)
    print("cidx: {}".format( cidx))
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
            if ctitle in use_percentages:
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
            mm[key] = (m1,m2, avg)
        except:
            mm[key] = ("NA","NA", "NA")
            pass
    

    headeritems = list()
    for ctitle in store.title:
        width = headerWidths[ctitle]
        bar = "{:>" + "{}".format(width) + "}"
        headeritems.append(bar.format(ctitle[:width]))

    print(Fore.GREEN + Style.BRIGHT + "  ".join(headeritems) + Style.RESET_ALL)

    for x,items in enumerate(getItems()):
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
                            bar = Fore.BLACK + "{:>" + "{}".format(headerWidths[ctitle]) + "}"
                        else:
                            bar = Fore.GREEN + "{:>" + "{}".format(headerWidths[ctitle]) + "}"
                        updated = True
            except:
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

    print(Fore.GREEN + Style.BRIGHT + "  ".join(avgs) + Style.RESET_ALL  + "\n" +str(len(store.items[cidx])))

def initiate():
    global cidx
    global currentsort
    import readchar
    import os

    cidx = 0
    os.system("clear")
    printTable()

    key = readchar.readkey()
    while (key != "q"):
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


