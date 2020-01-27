import z 
from random import sample
from collections import defaultdict
from sortedcontainers import SortedSet
import random
import zen
import os
import csv
stocks = zen.getLongEtfList()

reloadd = False
startd = "2014-04-01"
dics = None
dics52 = None

working = z.getp("working")

dics = z.getp("buydics")
if dics is None or reloadd:
    zen.reloaddic(False)
#raise SystemExit

testpoints = 10000
dates = z.getp("dates")
num_days = len(dates)
halfp = int(num_days/2)
endi = (num_days-32)-1
starti = dates.index(startd)

vals = defaultdict(list)
vals2 = defaultdict(int)
problems = set()
working = set()
total = 0
etfwins = 0
print ("len(dics.keys())")
print (len(dics.keys()))
keys = list(dics.keys())
#keys.remove("AIPT")

tally = defaultdict(int)
tallyt = defaultdict(int)

for dsize in range(30, 70, 1):
    print("dsize : {}".format( dsize ))
    for test in range(testpoints):

        first = random.randrange(starti, endi)
        second = random.randrange(max((first, halfp)), endi)
        fd = dates[first]
        sd = dates[second]
        etfchange = round(dics["SPY"][sd][1] / dics["SPY"][fd][1],4)
    
        samples = sample(keys, dsize*2)
        cum = 0
        added = 0
        for astock in samples:
            try:
                startv = dics[astock][sd][1]
                if startv < 20.00 :
                    continue
                working.add(astock)
#                if startv < 200.00 or startv > 300.00:
#                    continue
                change = round(startv / dics[astock][fd][1],4)
                added += 1
            except:
#                print("astock: {}".format( astock))
#                raise SystemExit
                continue
            cum += change
    
    #        if etfchange > change:
    #            etfwins += 1
    #        total += 1
            if change > 1.07:
                vals2[astock] += 1

            if added == dsize:
                break

#        vals[astock].append(change)
        if added < 30:
            continue
        try:
            change = round(cum/added,3)
            if etfchange > change:
                tally[added] += 1
            tallyt[added] += 1
        except:
            continue

import matplotlib.pyplot as plt
count_vs_etf = dict()
for count,total in tallyt.items():
    answer = round(tally[count]/total,3)
    print("count: {} {} {} ".format( count, answer, total))
    count_vs_etf[count] = answer
    plt.scatter(count, answer)
plt.show()


#print("tallyt: {}".format( tallyt))
#print("tally: {}".format( tally))

print("problems : {}".format( problems ))
#print ("etf wins")
#print (round(etfwins/total,3))

#z.setp(problems, "etfproblems")
z.setp(working, "working")
#raise SystemExit

ss = SortedSet()
for key,value in vals.items():
    avg = z.avg(value)
    ss.add((avg, key))

#path = z.getPath("analysis/stockanalysis.csv")
#with open(path, "w") as f:
#    for item in ss:
#        f.write("{},{}\n".format(item[1], item[0]))
#print(ss[-10:])
#print(ss[:10])

ss = SortedSet()
for key,value in vals2.items():
    ss.add((value, key))

save = ss[-30:]
z.setp(save, "rankstock")

ranklist = list()
for item in reversed(ss):
    ranklist.append(item[1])

z.setp(ranklist, "ranklist")
#print("ranklist: {}".format( ranklist))
z.setp(count_vs_etf, "count_vs_etf")
#print(ss[-30:])
#print(ss[:10])

path = z.getPath("analysis/stockanalysis2.csv")
with open(path, "w") as f:
    for item in ss:
        f.write("{},{}\n".format(item[1], item[0]))




