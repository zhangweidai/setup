values = [
    ("Title", "val"),
    ("Title1", "val"),
    ("Title2", 3)]

def getTitle():
    return getTitle.title
getTitle.title = None

print ("{:>8}".format("huhthisis loger"[:5]))
print ("{:<8}".format("huhthisis loger"[:5]))

test_list = [('Akshat', 1), ('Bro', 2), ('is', 3), ('Placed', 4)] 
print ("Original list is : " + str(test_list)) 
#res = map(None, *test_list) 
res = list(zip(*test_list)) 
print ("Modified list is : " + str(res[1])) 

from colorama import Fore, Back, Style

def storeValuesForPrinting(values):
    res = list(zip(*values))
    if not storeValuesForPrinting.title:
        storeValuesForPrinting.title = res[0]
    storeValuesForPrinting.items.append(res[1])

storeValuesForPrinting.items = list()
storeValuesForPrinting.title = None



def getFormat(values):
    items = list()
    rets = list()
    for title, width, val in values:
        bar = "{:>" + "{}".format(width) + "}"
        if not getTitle.title:
            items.append(bar.format(title[:width]))
        rets.append(bar.format(val))

    if not getTitle.title:
        getTitle.title = " ".join(items)
        items.append(bar.format(title[:width]))
    return " ".join(rets)

#    items = list()
#    for title, width, val in values:
#        items.append(values)
#    return getTitle.title.format(*items)

storeValuesForPrinting(values)
values = [
    ("Title",  "25%"),
    ("Title1", "b"),
    ("Title2", 20.00)]

storeValuesForPrinting(values)
storeValuesForPrinting(values)

from collections import defaultdict
def printAll():
    print("\n")
    headerWidths = defaultdict(int)
    for items in storeValuesForPrinting.items:
        for j, individual in enumerate(items):
            ctitle = storeValuesForPrinting.title[j]
            if len(str(individual)) > headerWidths[ctitle]:
                headerWidths[ctitle] = len(str(individual))

    items = list()
    for headerName in storeValuesForPrinting.title:
        width = headerWidths[headerName]
        bar = "{:>" + "{}".format(width) + "}"
        items.append(bar.format(headerName[:width]))

    print(Fore.GREEN + Style.BRIGHT + " ".join(items) + Style.RESET_ALL)

    for items in storeValuesForPrinting.items:
        saveme = list()
        for j, individual in enumerate(items):
            ctitle = storeValuesForPrinting.title[j]
            bar = "{:>" + "{}".format(headerWidths[ctitle]) + "}"
            saveme.append(bar.format(individual))
        print(" ".join(saveme))

def clearAll():
    storeValuesForPrinting.items = list()

if __name__ == '__main__':
    printAll()
    clearAll()
    
    storeValuesForPrinting(values)
    
    values = [
        ("Title",  1, "25%"),
        ("Title1", 3, "b"),
        ("Title2", 3, 220.00)]
    
    
    printAll()
