
import z 
import statistics

from collections import defaultdict, deque
from sortedcontainers import SortedSet
import random
import zen
import csv
import os

okList = ["IVV", "IUSG", "USMV"]
addrop = defaultdict(int)
def averageDailyDrop(directory = "historical"):
    global dics
    path = z.getPath(directory)  
    listOfFiles = os.listdir(path)
    for idx,entry in enumerate(listOfFiles):
        if not idx % 100:
            print("idx: {}".format( idx))
    
        astock = os.path.splitext(entry)[0]
        if astock not in okList:
            continue
        path = z.getPath("{}/{}".format(directory, entry))
        print("path: {}".format( path))
        for row in csv.DictReader(open(path)):
            low = float(row['Low'])
            op = float(row['Open'])
            try:
                avgDrop = round(float(row['Low'])/float(row['Open']),2)
            except:
                pass
#            if avgDrop < 0.7:
#                print("low : {}".format( low ))
#                print("op : {}".format( op ))
                
#            drop = z.percentage(avgDrop, 1)
#            if drop == "-0.0%" or drop == "0.0%":
#                drop = "0"
            addrop[avgDrop] += 1

#averageDailyDrop("ETF")
#print("drop : {}".format( addrop ))
#exit()

#problems = z.getp("etfproblems")
dics = defaultdict(dict)
def csvToDic(directory = "historical"):
    global dics
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

def etfToDic(directory = "ETF"):
    global dics
    path = z.getPath(directory)  
    etfs = z.getEtfList(buys = True)
    for entry in etfs:
        path = z.getPath("{}/{}.csv".format(directory, entry))
        for row in csv.DictReader(open(path)):
            date = row['Date']
            if "201" not in date:
                continue

            dics[astock][date] = float(row['Close'])


def saveData():
    global dics
    csvToDic(directory="ETF")
    z.setp(dics, "etf_bigdic")
    dics = defaultdict(dict)
    csvToDic()
    z.setp(dics, "stocks_bigdic")
#    exit()


def getClose(astock, sday, sdate, count = 3):
    global dics
    if count == 0:
        return None
    try:
        return dics[astock][sday]
    except:
        sdate = sdate + 1
        sday = dates[sdate]
        return getClose(astock, sday, sdate, count = count - 1)

def setTestpoints(lens, didx, ayear, dates, stocks):
    global testpoints, vals, negs
    testpoints = 0
    for sdate in range(-1*(lens-didx),(-1*ayear)+1):
        edate = sdate + ayear - 1
        sday = dates[sdate]
        eday = dates[edate]
        eyear = int(eday.split("-")[0]) - 2000
        score = float(eyear)/10.0
    
        for astock in stocks:
            first = getClose(astock, sday, sdate)
            second = getClose(astock, eday, edate)
    
            if first == None or second == None:
                continue
    
            change = round(second/first,4)
    
            if change > 2.0:
                change = 2.0
    
            if change < 1.00:
                negs[astock] += (score * 2)
                simple[astock] -= (score * score) 
            else:
                simple[astock] += score
    
    
            vals[astock].append(change)
    
            if "2018" in eday or "2019" in eday:
                vals[astock].append(change)
    
        testpoints += score
        return vals

#path = z.getPath("analysis/etfanalysis.csv")
#with open(path, "w") as f:
#    for item in ss:
#        f.write("{},{}\n".format(item[1], item[0]))

#save = ss[-15:]
#z.setp(save, "ranketf2")
#print(ss[-200:])

def adjustedStockScore():
    global negs
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
    global negs
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

#saveranketf()
#        try:
#            print (
#                item[1]
#                , round(negs[item[1]]/testpoints,3))
#        except:
#            pass

#print(ss[:10])


dates = z.getp("dates")
vals = None
simple = defaultdict(float)
negs = defaultdict(int)
testpoints = 0
def genStartOver():
    global vals, dics, testpoints
    saveData()
    dics = z.getp("stocks_bigdic")
    num_days = len(dates)
    endi = (num_days-252)-1
    vals = defaultdict(list)
    problems = set()
    stocks = dics.keys()
    sdate = "2013-01-02"
    didx = dates.index(sdate)
    lens = len(dates)
    ayear = 252
    
    vals = setTestpoints(lens, didx, ayear, dates, stocks)

    median = SortedSet()
    lowest = SortedSet()
    lowestdic = dict()
    #yearlydic = z.getp("yearlydic")
    yearlydic = dict()
    yearlyscore = SortedSet()
    simplescores = SortedSet()
    ivv = 0
    maxvals = len(vals["IVV"])
    print("maxvals : {}".format( maxvals ))
    for astock,value in vals.items():
        count = len(value)
        ratio = count / maxvals
        y1m = statistics.median(value)
        y1w = min(value)
        yearlydic[astock] = (y1w, y1m)
        sub = (negs[astock]/testpoints)
        score = (1 - sub) * (y1w + y1m)
        if ratio < .7:
            score = score * ratio
        else:
            try:
                zen.getPrice(astock, dates[-1], openp = 'both')
            except:
                print ("could not find a price for {} {}".format(astock, dates[-1]))
                continue
    
            lowest.add((y1w, astock))
            median.add((y1m, astock))
    
        yearlyscore.add((round(score,3), astock))
        simplescores.add((round(simple[astock] * ratio,3), astock))
    
    ultdict = dict()
    print("yearlyscore: {}".format( yearlyscore))
    z.setp(yearlyscore[-30:],"ultrank")
    z.setp(yearlyscore[:12],"worstrank")
    print ("ult")
    print (yearlyscore[-30:])
    print ("Worst")
    print (yearlyscore[:12])
    
    print ("simple")
    print (simplescores[-30:])
    z.setp(simplescores[-30:],"simplerank")
    
    #raise SystemExit
#    
#    for idx, item in enumerate(reversed(yearlyscore)):
#        ultdict[item[1]] = idx
#    
#    #print("savedict: {}".format( savedict[-30:]))
#    z.setp(ultdict, "ultdict")
#    
#    #z.setp(lowestdic,"lowestdic")
#    z.setp(yearlydic,"yearlydic")
##    print("lowest: {}".format( lowest[-20:]))
#    print("median: {}".format( median[-20:]))
#    z.setp(lowest[-20:],"lowyear")
#    

if __name__ == '__main__':
    genStartOver()
