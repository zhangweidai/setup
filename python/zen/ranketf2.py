import z 
import statistics
from collections import defaultdict, deque
from sortedcontainers import SortedSet
import random
import zen
import csv
import os

def csvToDic(directory = "historical"):
    dics = defaultdict(dict)
    path = z.getPath(directory)  
    listOfFiles = os.listdir(path)
    for idx,entry in enumerate(listOfFiles):
        if not idx % 100:
            print("idx: {}".format( idx))
    
        astock = os.path.splitext(entry)[0]
        path = z.getPath("{}/{}".format(directory, entry))
        for row in csv.DictReader(open(path)):
            date = row['Date']
            if "201" not in date:
                continue
            dics[astock][date] = float(row['Close'])
    z.setp(dics, "bigdic")
    return dics

#csvToDic(directory="ETF")
#csvToDic()
#raise SystemExit
def doitagain(dics = None):
    if not dics :
        dics = z.getp("stocks_bigdic")
    testpoints = 0
    dates = z.getp("dates")
    num_days = len(dates)
    endi = (num_days-252)-1
    vals = defaultdict(list)
    negs = defaultdict(int)
    problems = set()
    stocks = dics.keys()
    sdate = "2013-01-02"
    didx = dates.index(sdate)
    lens = len(dates)
    ayear = 252
    latestAnnual = z.getp("latestAnnual")
    thelist = list()
    whats = set()
    sdate_look = (-1  *  ayear ) 
    print("sdate_look : {}".format( sdate_look ))
    for sdate in range(-1*(lens-didx),(-1*ayear)+1):
        edate = sdate + ayear - 1
        sday = dates[sdate]
        eday = dates[edate]
        score = 1
        if "2019" in eday:
            score = 2
        for astock in stocks:
#            if astock != "AMZN":
#                continue
    
            try:
                first = dics[astock][sday]
            except:
                try:
                    sday = dates[sdate-1]
                    first = dics[astock][sday]
                except:
                    problems.add(astock)
#                    print("sday: {}".format( sday))
#                    print("astock: {}".format( astock))
#                    exit()
                    continue
            try:
                second = dics[astock][eday]
            except:
                try:
                    eday = dates[edate-1]
                    second = dics[astock][eday]
                except:
                    problems.add(astock)

#                    print("2sday: {}".format( sday))
#                    print("2astock: {}".format( astock))
#                    exit()
                    continue
            change = round(second/first,4)
    
            if sdate == sdate_look:
                thelist.append(change)
                latestAnnual[astock] = change
    
                if change > 5.0:
                    whats.add(astock)
#                    print("astock: {} {} {} {} {}".format( astock, change, first, second, sday))
    
#            if astock in problems:
#                continue
    
            if change > 2.0:
                change = 2.0
    
            if change < 1.00:
                negs[astock] += score
    
#            if change < 0.90:
#                print("astock: {} {} {} {} {}".format( astock, change, first, second, sday))
    
            vals[astock].append(change)
            if score == 2:
                vals[astock].append(change)
        testpoints += score
    z.setp(latestAnnual, "latestAnnual")
#    print (z.avg(thelist))
#    print (statistics.median(thelist))
#    print (min(thelist))
#    print (max(thelist))
    median = SortedSet()
    lowest = SortedSet()
    lowestdic = dict()
    yearlydic = z.getp("yearlydic")
    yearlyscore = SortedSet()
    for astock,value in vals.items():
        if astock in problems:
            continue
        print("Working astock : {}".format( astock ))
        y1m = statistics.median(value)
        y1w = min(value)
        lowest.add((y1w, astock))
        median.add((y1m, astock))
        yearlydic[astock] = (y1w, y1m)
        score = (1 - (negs[astock]/testpoints)) * (y1w + y1m)
        yearlyscore.add((score, astock))
    
    ultdict = dict()
    print("yearlyscore: {}".format( yearlyscore))
    z.setp(yearlyscore[-30:],"ultrank")
    
    for idx, item in enumerate(reversed(yearlyscore)):
        ultdict[item[1]] = idx
    
    z.setp(ultdict, "ultdict")
    z.setp(yearlydic,"yearlydic")
    z.setp(lowest[-20:],"lowyear")
    z.setp(lowest[-20:],"lowyear")

def adjustedStockScore():
    yearly = list()
    ss2 = SortedSet()
    import util
    
    for item in ss:
    #    print (item, round(
        print (item, round(negs[item[1]]/testpoints,3))
    
        try:
            etfc = float(util.getEtfQualifications(item[1], count=True))/10
            print("etfc : {}".format( etfc ))
        except:
            etfc = 1
    
        percent = negs[item[1]]/testpoints
        score = item[0] - (2*percent) - etfc
        ss2.add((score, item[1]))
    
    print("ss2: {}".format( ss2[-5:]))
    z.setp(ss2[-5:], "ranketf")


def saveranketf():
    yearly = list()
    ss2 = SortedSet()
    import util
    
    for item in ss:
    #    print (item, round(
        print (item, round(negs[item[1]]/testpoints,3))
    
        try:
            etfc = float(util.getEtfQualifications(item[1], count=True))/10
            print("etfc : {}".format( etfc ))
        except:
            etfc = 1
    
        percent = negs[item[1]]/testpoints
        score = item[0] - (2*percent) - etfc
        ss2.add((score, item[1]))
    
    print("ss2: {}".format( ss2[-5:]))
    z.setp(ss2[-5:], "ranketf")

def regen():
#    dics = csvToDic()
    doitagain()

if __name__ == '__main__':
    doitagain()
