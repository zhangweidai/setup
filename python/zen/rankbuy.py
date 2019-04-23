import z 
from collections import defaultdict, deque
from sortedcontainers import SortedSet
import random
import zen
import os
import csv
stocks = zen.getLongEtfList()

reloadd = False
startd = "2013-04-16"
if reloadd:
    path = z.getPath('historical')  
    listOfFiles = os.listdir(path)
    dics = defaultdict(dict)
    for idx,entry in enumerate(listOfFiles):
        if not idx % 100:
            print("idx: {}".format( idx))
        tpath = "{}/{}".format(path,entry)
        start = False
        astock = os.path.splitext(entry)[0]
        for row in csv.DictReader(open(tpath)):
            date = row['Date']
            if date == startd:
                start = True
            if start:
                dics[astock][date] = float(row['Close'])
    z.setp(dics, "buydics")

dics = z.getp("buydics")
print ("loadeD")

testpoints = 4000
dates = z.getp("dates")
num_days = len(dates)
endi = (num_days-100)-1
starti = dates.index(startd)

vals = defaultdict(list)
vals2 = defaultdict(int)
problems = set()
for test in range(testpoints):
    first = random.randrange(starti, endi)
    second = random.randrange(first, endi)
    fd = dates[first]
    sd = dates[second]
    for astock in dics.keys():
        try:
            change = round(dics[astock][sd] / dics[astock][fd],4)
        except:
            problems.add(astock)
            continue

        if change > 1.07:
            vals2[astock] += 1

        vals[astock].append(change)
print("problems : {}".format( problems ))

#z.setp(problems, "etfproblems")

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
#print(ss[-30:])
#print(ss[:10])

path = z.getPath("analysis/stockanalysis2.csv")
with open(path, "w") as f:
    for item in ss:
        f.write("{},{}\n".format(item[1], item[0]))




