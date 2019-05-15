
import z 
import statistics

from collections import defaultdict, deque
from sortedcontainers import SortedSet
import random
import zen
import csv
import os
stocks = zen.getLongEtfList()

#problems = z.getp("etfproblems")
dics = defaultdict(dict)
def csvToDic(directory = "historical"):
    path = z.getPath(directory)  
    listOfFiles = os.listdir(path)
    for idx,entry in enumerate(listOfFiles):
        if not idx % 100:
            print("idx: {}".format( idx))
    
        astock = os.path.splitext(entry)[0]
        path = z.getPath("{}/{}".format(directory, entry))
        for row in csv.DictReader(open(path)):
            date = row['Date']
            dics[astock][date] = float(row['Close'])
    z.setp(dics, "bigdic")

#csvToDic(directory="ETF")
#csvToDic()
#raise SystemExit
dics = z.getp("bigdic")

#dics = z.getp("BUY2_P")
testpoints = 0

dates = z.getp("dates")
num_days = len(dates)
endi = (num_days-252)-1

vals = defaultdict(list)
negs = defaultdict(int)
problems = set()

stocks = dics.keys()
#for astock in dics.keys():
#    rank = zen.getMCRank(astock)
#    if rank == "NA":
#        continue
#    if rank < 1200:
#        stocks.append(astock)
#didx = dates.index(sdate)

sdate = "2013-01-02"
didx = dates.index(sdate)
print("didx : {}".format( didx ))
lens = len(dates)
ayear = 202
#latestAnnual = dict()
latestAnnual = z.getp("latestAnnual")
thelist = list()
whats = set()
sdate_look = (-1  *  ayear ) 
for sdate in range(-1*(lens-didx),(-1*ayear)+1):
    edate = sdate + ayear - 1
    sday = dates[sdate]
    eday = dates[edate]
    score = 1
    if "2019" in eday:
        score = 2
#    print("sdate: {}".format( sdate))
#print("sdate_look : {}".format( sdate_look ))
#raise SystemExit
#def dele():
    for astock in stocks:
        if not astock == "IUSG":
            continue

        try:
            first = dics[astock][sday]
        except:
            try:
                sday = dates[sdate-1]
                first = dics[astock][sday]
            except:
                problems.add(astock)
                continue
        try:
            second = dics[astock][eday]
        except:
            try:
                eday = dates[edate-1]
                second = dics[astock][eday]
            except:
                problems.add(astock)
                continue
        change = round(second/first,4)

        if sdate == sdate_look:
            thelist.append(change)
            latestAnnual[astock] = change

            if change > 5.0:
                whats.add(astock)
                print("astock: {} {} {} {} {}".format( astock, change, first, second, sday))

        if astock in problems:
            continue

        if change > 2.0:
            change = 2.0

        if change < 1.00:
            negs[astock] += score

        if change < 0.90:
            print("astock: {} {} {} {} {}".format( astock, change, first, second, sday))

        vals[astock].append(change)
        if score == 2:
            vals[astock].append(change)
    testpoints += score
raise SystemExit
z.setp(latestAnnual, "latestAnnual")
print (z.avg(thelist))
print (statistics.median(thelist))
print (min(thelist))
print (max(thelist))
#z.setp(whats, "whats")
#raise SystemExit
#for test in range(testpoints):
#    if not test % 100:
#        print("test : {}".format( test ))
#    first = random.randrange(starti, endi)
#    second = first + 252
#    fd = dates[first]
##    print("fd : {}".format( fd ))
#    sd = dates[second]
##    print("sd : {}".format( sd ))
#    for astock in stocks:
#        if astock in problems:
#            continue
##        print("astock : {}".format( astock ))
#        try:
#            first = dics[astock][fd]
#            change = round(dics[astock][sd] / first,4)
##            print("change : {}".format( change ))
#        except Exception as e:
##            print("dics: {}".format( dics[astock]))
##            print("first : {}".format( first ))
##            print("astock: {}".format( astock))
##            z.trace(e)
#            problems.add(astock)
##            exit()
#            continue
#
##print("problems : {}".format( problems ))

#z.setp(problems, "etfproblems")

#ss = SortedSet()
#for key,value in vals.items():
#    avg = z.avg(value)
#    ss.add((avg, key))
#
#save = ss[-15:]
#z.setp(save, "ranketf2")
#print(ss[-15:])
#for item in ss[-15:]:
#    try:
#        print (item[1], round(negs[item[1]]/testpoints,3))
#    except:
#        pass

median = SortedSet()
lowest = SortedSet()
lowestdic = dict()
yearlydic = z.getp("yearlydic")
#yearlydic = dict()
yearlyscore = SortedSet()
for astock,value in vals.items():
    if astock in problems:
        continue
    y1m = statistics.median(value)
    y1w = min(value)
    lowest.add((y1w, astock))
    median.add((y1m, astock))
    yearlydic[astock] = (y1w, y1m)
    score = (1 - (negs[astock]/testpoints)) * (y1w + y1m)
    yearlyscore.add((score, astock))

ultdict = dict()
z.setp(yearlyscore[-30:],"ultrank")

for idx, item in enumerate(reversed(yearlyscore)):
    ultdict[item[1]] = idx

#print("savedict: {}".format( savedict[-30:]))
z.setp(ultdict, "ultdict")

#z.setp(lowestdic,"lowestdic")
z.setp(yearlydic,"yearlydic")
print("lowest: {}".format( lowest[-20:]))
print("median: {}".format( median[-20:]))

z.setp(lowest[-20:],"lowyear")
z.setp(lowest[-20:],"lowyear")

#path = z.getPath("analysis/etfanalysis.csv")
#with open(path, "w") as f:
#    for item in ss:
#        f.write("{},{}\n".format(item[1], item[0]))

#save = ss[-15:]
#z.setp(save, "ranketf2")
#print(ss[-200:])

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

#saveranketf()
#        try:
#            print (
#                item[1]
#                , round(negs[item[1]]/testpoints,3))
#        except:
#            pass

#print(ss[:10])



