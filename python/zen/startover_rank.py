
import z 
import statistics

from collections import defaultdict, deque
from sortedcontainers import SortedSet
import random
import zen
import csv
import os
import util

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
r2dict = dict()
def csvToDic(directory = "historical", generate_r2 = False):
    global dics, r2dict
    path = z.getPath(directory)  
    listOfFiles = os.listdir(path)
    last = list()
    for idx,entry in enumerate(listOfFiles):
        if not idx % 100:
            print("idx: {}".format( idx))
    
        astock = os.path.splitext(entry)[0]

        path = z.getPath("{}/{}".format(directory, entry))
        for row in csv.DictReader(open(path)):
            date = row['Date']

            if "201" not in date:
                continue

            close = float(row['Close'])

            if generate_r2 and "2019" in date:
                last.append(close)

            dics[astock][date] = close

        if generate_r2:
            try:
                r2dict[astock] = util.regress(last, rsquared=True)
            except:
                pass


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
    global dics, r2dict
    csvToDic(directory="ETF")
    z.setp(dics, "etf_bigdic")
    dics = defaultdict(dict)
    csvToDic(generate_r2 = True)
    z.setp(dics, "stocks_bigdic")
    z.setp(r2dict, "r2dict")
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

if __name__ == '__main__':
    # normal
    saveData()
    #csvToDic(generate_r2 = True)

