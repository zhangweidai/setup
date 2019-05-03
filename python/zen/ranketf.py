import z 
from collections import defaultdict, deque
from sortedcontainers import SortedSet
import random
import zen
import csv
import os
stocks = zen.getLongEtfList()

#problems = z.getp("etfproblems")
def csvToDic():
    dics = defaultdict(dict)
    path = z.getPath('historical')  
    listOfFiles = os.listdir(path)
    for idx,entry in enumerate(listOfFiles):
        if not idx % 100:
            print("idx: {}".format( idx))
    
        astock = os.path.splitext(entry)[0]
        path = z.getPath("historical/{}".format(entry))
        for row in csv.DictReader(open(path)):
            date = row['Date']
            dics[astock][date] = float(row['Close'])
    z.setp(dics, "etfdics")
#raise SystemExit
dics = z.getp("etfdics")

testpoints = 3000

dates = z.getp("dates")
num_days = len(dates)
endi = (num_days-252)-1
starti = dates.index("2013-01-02")

vals = defaultdict(list)
negs = defaultdict(int)
problems = set()

stocks = list()
for astock in dics.keys():
    rank = zen.getMCRank(astock)

    if rank == "NA":
        continue

    if rank < 1000:
        stocks.append(astock)

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
        try:

            first = dics[astock][fd]
            change = round(dics[astock][sd] / first,4)
        except Exception as e:
#            z.trace(e)
#            problems.add(astock)
            continue

        if change < 1.00:
            negs[astock] += 1

        vals[astock].append(change)
print("problems : {}".format( problems ))

#z.setp(problems, "etfproblems")

ss = SortedSet()
for key,value in vals.items():
    avg = z.avg(value)
    ss.add((avg, key))

save = ss[-15:]
#z.setp(save, "ranketf2")
print(ss[-15:])
for item in ss[-15:]:
    try:
        print (item[1], round(negs[item[1]]/testpoints,3))
    except:
        pass


import statistics
ss = SortedSet()
for key,value in vals.items():
    avg = statistics.median(value)
    ss.add((avg, key))


#path = z.getPath("analysis/etfanalysis.csv")
#with open(path, "w") as f:
#    for item in ss:
#        f.write("{},{}\n".format(item[1], item[0]))

save = ss[-15:]
#z.setp(save, "ranketf2")
print(ss[-15:])
for item in ss[-15:]:
    try:
        print (item[1], round(negs[item[1]]/testpoints,3))
    except:
        pass

#print(ss[:10])



