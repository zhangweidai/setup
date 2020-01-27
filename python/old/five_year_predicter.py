import z
from sortedcontainers import SortedSet
import zen
import random

dics = z.getp("stocks_bigdic")
stocks = dics.keys()
year = 252
numofyears = 3
dur = year * numofyears
req = year * numofyears * 2
print("dur : {}".format( dur ))
median = SortedSet()
perstock = 10
mediancount = 600
for astock in stocks:
    cdict = dics[astock]
    daycount = len(cdict)
    if daycount < req:
        continue

    for i in range(0, perstock):
#        print("daycount : {}".format( daycount ))
        rand = random.randint(0, daycount - req)
#        print("rand : {}".format( rand ))
        thelist = list(cdict)
        start = thelist[rand]
#        print("start : {}".format( start ))
#        print("start : {}".format( cdict[start] ))
        midway = thelist[rand+dur]
#        print("midway : {}".format( midway ))
#        print("midway : {}".format( cdict[midway] ))
        change = round(cdict[midway]  / cdict[start] ,5)
        if change > 3:
            continue
#        print("change : {}".format( change ))
        try:
            end = thelist[rand+req]
        except:
            continue
#        print("end : {}".format( end ))
#        print("end : {}".format( cdict[end] ))
        yes = (float(cdict[midway]) * 1.07 < float(cdict[end]))
        median.add((change, (astock, yes)))
        if len(median) > mediancount:
            median.pop(0)

count = 0
for bbb in median:
    if bbb[1][1]:
        count += 1
print("count : {}".format( count/mediancount ))

#print("median: {}".format( median))
#    for date in dics[astock]:
#        print("date : {}".format( date ))
#    z.breaker(10)

