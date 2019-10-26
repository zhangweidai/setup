from openpyxl import load_workbook
import download_financials
import os
import util
import fnmatch
import z
from collections import defaultdict, deque
from sortedcontainers import SortedSet
#want = ["Market Cap", "PE ratio", "Revenue per Share"]
want = ["PE ratio"]
icols = []
cdics = defaultdict(SortedSet)
bdics = SortedSet()

def proc(astock):
    global bdics
    path = download_financials.metrics(astock)
    if not os.path.exists(path):
        return
    wb = load_workbook(filename = path)
    ws = wb.active
    dates = list()
    for row in ws.values:
        title = None
        crow = list()
        save = list()
        for i, value in enumerate(row):
            if not dates:
                title = value
            if not title:
                title = value

            if value:
                crow.append(value)

            if title in want and type(value) != str :
                save.append(value)

        if not dates:
            dates = crow
            for i, date in enumerate(dates):
                icols.append(i+1)
#                if date.month == 12 or date.month == 11:
                
        if save:
            lists = []
            for i,ev in enumerate(save):
                if i < 4:
                    lists.append(ev)
            leng = len(lists)

            avg = sum(lists)/leng
            bdics.add((avg, astock))


def getXs():
    pattern = "*.xlsx"
    holds = []
    listOfFiles = os.listdir('../zen_dump/metrics')  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append(entry.split(".")[0])
    return holds

def doit():
    proc("COST")
    print("bdics: {}".format( bdics))
    return
    stocks = getXs()
    for astock in stocks:
        proc(astock)
    z.setp(bdics, "avg_pe")
    return

if __name__ == '__main__':
    doit()
