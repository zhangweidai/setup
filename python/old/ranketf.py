
import z 
dates = z.getp("dates")
print("dates : {}".format( len(dates )))
sdate = "2013-01-02"
didx = dates.index(sdate)
print("didx : {}".format( didx ))
lens = len(dates)
for sdate in range(-1*(lens-didx),-252):
    edate = sdate + 252
    print("date : {}".format( dates[sdate] ))
    print("date : {}".format( dates[edate] ))
    raise SystemExit

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
#    z.setp(dics, "bigdic")
#    z.setp(dics, "bigdic")
#csvToDic(directory="ETF")
#raise SystemExit
dics = z.getp("bigdic")

#dics = z.getp("BUY2_P")
testpoints = 5000

dates = z.getp("dates")
num_days = len(dates)
endi = (num_days-252)-1
starti = dates.index("2014-01-02")

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
sdate = "2013-01-02"
didx = dates.index(sdate)
for test in range(testpoints):
    if not test % 100:
        print("test : {}".format( test ))
    first = random.randrange(starti, endi)
    second = first + 252
    fd = dates[first]
#    print("fd : {}".format( fd ))
    sd = dates[second]
#    print("sd : {}".format( sd ))
    for astock in stocks:
        if astock in problems:
            continue
#        print("astock : {}".format( astock ))
        try:

            first = dics[astock][fd]
            change = round(dics[astock][sd] / first,4)
#            print("change : {}".format( change ))
        except Exception as e:
#            print("dics: {}".format( dics[astock]))
#            print("first : {}".format( first ))
#            print("astock: {}".format( astock))
#            z.trace(e)
            problems.add(astock)
#            exit()
            continue

        if change < 1.00:
            negs[astock] += 1

        vals[astock].append(change)
#print("problems : {}".format( problems ))

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

import statistics
median = SortedSet()
lowest = SortedSet()
lowestdic = dict()
#yearlydic = z.getp("yearlydic")
for key,value in vals.items():
    if key in problems:
        continue
    y1m = statistics.median(value)
    y1w = min(value)
    lowest.add((y1w, key))
    median.add((y1m, key))
#    yearlydic[key] = (y1w, y1m)

#z.setp(lowestdic,"lowestdic")
#z.setp(yearlydic,"yearlydic")
print("lowest: {}".format( lowest[-20:]))
print("median: {}".format( median[-20:]))

z.setp(lowest[-20:],"lowyear")

#path = z.getPath("analysis/etfanalysis.csv")
#with open(path, "w") as f:
#    for item in ss:
#        f.write("{},{}\n".format(item[1], item[0]))

#save = ss[-15:]
#z.setp(save, "ranketf2")
#print(ss[-200:])
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



