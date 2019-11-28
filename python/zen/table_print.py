from colorama import Fore, Back, Style
from collections import defaultdict

def store(values):
    res = list(zip(*values))
    if not store.title:
        store.title = res[0]
    store.items.append(res[1])
store.items = list()
store.title = None

def printTable():
    headerWidths = defaultdict(int)
    for items in store.items:
        for j, individual in enumerate(items):
            ctitle = store.title[j]
            if len(str(individual)) > headerWidths[ctitle]:
                headerWidths[ctitle] = len(str(individual))

    items = list()
    for headerName in store.title:
        width = headerWidths[headerName]
        bar = "{:>" + "{}".format(width) + "}"
        items.append(bar.format(headerName[:width]))

    print(Fore.GREEN + Style.BRIGHT + "  ".join(items) + Style.RESET_ALL)

    for items in store.items:
        saveme = list()
        for j, individual in enumerate(items):
            if not individual:
                individual = "NA"
            ctitle = store.title[j]
            bar = "{:>" + "{}".format(headerWidths[ctitle]) + "}"
            try:
                saveme.append(bar.format(individual))
            except:
                print ("problem with {} {}".format(ctitle, individual))
                exit()
        print("  ".join(saveme))

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
