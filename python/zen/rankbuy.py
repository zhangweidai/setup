import z 
from random import sample
from collections import defaultdict, deque
from sortedcontainers import SortedSet
import random
import zen
import os
import csv
stocks = zen.getLongEtfList()

reloadd = False
startd = "2013-04-16"
dics = None
dics52 = None

working = z.getp("working")

def reloaddic():
    global dics

    dates = z.getp("dates")
    date52 = dates[-52]

    path = z.getPath('historical')  
    listOfFiles = os.listdir(path)
    dics = defaultdict(dict)
    dics52 = defaultdict(dict)
    for idx,entry in enumerate(listOfFiles):

        if not idx % 100:
            print("idx: {}".format( idx))

        tpath = "{}/{}".format(path,entry)
        start = False
        start52 = False
        astock = os.path.splitext(entry)[0]


        for row in csv.DictReader(open(tpath)):
            date = row['Date']

            if date == startd:
                start = True

            if date == date52:
                start52 = True

            ans = (float(row['Open']), float(row['Close']))

            if start52:
                dics52[astock][date] = ans

            if astock not in working:
                continue

            if start: 
                dics[astock][date] = ans

    z.setp(dics, "buydics")
    z.setp(dics52, "buydics52")

dics = z.getp("buydics")
if dics is None or reloadd:
    reloaddic()
#raise SystemExit

testpoints = 10000
dates = z.getp("dates")
num_days = len(dates)
endi = (num_days-100)-1
starti = dates.index(startd)

vals = defaultdict(list)
vals2 = defaultdict(int)
problems = set()
working = set()
total = 0
etfwins = 0
print (len(dics.keys()))
keys = list(dics.keys())
#keys.remove("AIPT")

tally = defaultdict(int)
tallyt = defaultdict(int)

for dsize in range(5,121, 5):
    for test in range(testpoints):

        first = random.randrange(starti, endi)
        second = random.randrange(first, endi)
        fd = dates[first]
        sd = dates[second]
        etfchange = round(dics["SPY"][sd][1] / dics["SPY"][fd][1],4)
    
        samples = sample(keys, dsize)
        cum = 0
        added = 0
        for astock in samples:
            try:
                startv = dics[astock][sd][1]
#                if startv < 90.00 :
#                    continue
#                working.add(astock)
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
#        vals[astock].append(change)
        try:
            change = round(cum/added,3)
            if etfchange > change:
                tally[added] += 1
            tallyt[added] += 1
        except:
            continue

import matplotlib.pyplot as plt
for count,total in tallyt.items():
    answer = round(tally[count]/total,3)
    print("count: {} {} {} ".format( count, answer, total))
    plt.scatter(count, answer)
plt.show()


#print("tallyt: {}".format( tallyt))
#print("tally: {}".format( tally))

print("problems : {}".format( problems ))
#print ("etf wins")
#print (round(etfwins/total,3))

#z.setp(problems, "etfproblems")
#z.setp(working, "working")
#raise SystemExit

#ss = SortedSet()
#for key,value in vals.items():
#    avg = z.avg(value)
#    ss.add((avg, key))

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
#print(ss[-30:])
#print(ss[:10])

path = z.getPath("analysis/stockanalysis2.csv")
with open(path, "w") as f:
    for item in ss:
        f.write("{},{}\n".format(item[1], item[0]))




