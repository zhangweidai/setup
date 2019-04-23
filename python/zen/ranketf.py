import z 
from collections import defaultdict, deque
from sortedcontainers import SortedSet
import random
import zen
import csv
stocks = zen.getLongEtfList()

#problems = z.getp("etfproblems")
#dics = defaultdict(dict)
#for astock in stocks:
#    if astock in problems:
#        continue
#    path = z.getPath("ETF/{}.csv".format(astock))
#    for row in csv.DictReader(open(path)):
#        date = row['Date']
#        dics[astock][date] = float(row['Close'])
#
#z.setp(dics, "etfdics")
dics = z.getp("etfdics")

testpoints = 2000

dates = z.getp("dates")
num_days = len(dates)
endi = (num_days-49)-1
starti = dates.index("2013-04-16")

vals = defaultdict(list)
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
        vals[astock].append(change)
print("problems : {}".format( problems ))

#z.setp(problems, "etfproblems")

ss = SortedSet()
for key,value in vals.items():
    avg = z.avg(value)
    ss.add((avg, key))

path = z.getPath("analysis/etfanalysis.csv")
with open(path, "w") as f:
    for item in ss:
        f.write("{},{}\n".format(item[1], item[0]))


save = ss[-15:]
z.setp(save, "ranketf")
#print(ss[-15:])
#print(ss[:10])



