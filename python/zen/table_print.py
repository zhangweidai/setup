from colorama import Fore, Back, Style
from collections import defaultdict
import z

use_percentages = None

def store(values):
    res = list(zip(*values))
    if not store.title:
        store.title = res[0]
    store.items.append(res[1])
store.items = list()
store.title = None

def printTable():
    headerWidths = defaultdict(int)

    # determine headerWidths
    dics = defaultdict(list)
    for items in store.items:
        for j, individual in enumerate(items):
            dics[j].append(individual)
            ctitle = store.title[j]
            width = len(str(individual))
            if ctitle in use_percentages:
                width = len(str(round(individual,2))) + 3

            if width > headerWidths[ctitle]:
                headerWidths[ctitle] = width

    mm = dict()
    for key in dics.keys():
        try:
            m1 = min(dics[key])
            m2 = max(dics[key])
            mm[key] = (m1,m2)
        except:
            pass
        

    headeritems = list()
    for headerName in store.title:
        width = headerWidths[headerName]
        bar = "{:>" + "{}".format(width) + "}"
        headeritems.append(bar.format(headerName[:width]))

    print(Fore.GREEN + Style.BRIGHT + "  ".join(headeritems) + Style.RESET_ALL)

    for x,items in enumerate(store.items):
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

def clearTable():
    store.items = list()

if __name__ == '__main__':
    printTable()
    clearTable()
    
    store(values)
    
    values = [
        ("Title",  "25%"),
        ("Title1", "b"),
        ("Title2", 220.00)]
    
    printTable()
