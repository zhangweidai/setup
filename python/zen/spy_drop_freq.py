import z
import statistics
from collections import defaultdict, deque
import zen
import csv

path = z.getPath("ETF/IHI.csv")
prevclose = None
changes = list()
negs = list()
maxchange = 1
minchange = 1
maxdate = None
mindate =  None
dic = defaultdict(int)
ylist = [i/100 for i in range(90,100,1)]

start = False
daysapart = 0
dayslist = list()
tally = 0
for row in csv.DictReader(open(path)):
#    if "2014" in row["Date"]:
#        start = True
#    if not start:
#        continue

    if not prevclose:
        prevclose = float(row['Open'])

    change = round(float(row['Close']) / prevclose,4)
    if change < 1.00:
        negs.append(change)

    if change < 0.9800:
        dayslist.append(daysapart)
        date = row["Date"]
        print("date : {} {} ".format( date, daysapart ))
        if daysapart > 80:
            tally += 1
        daysapart = 0
    else:
        daysapart += 1

    for i in ylist:
        if change < i:
            dic[z.percentage(i)] += 1

    if change < minchange:
        minchange = change
        mindate = row["Date"]
    elif change > maxchange:
        maxchange = change
        maxdate = row["Date"]

    changes.append(change)
    prevclose = float(row['Close'])

#print("changes: {}".format( negs))
print("dayslist: {}".format( dayslist))
print("len dayslist: {}".format( len(dayslist)))
print("tally : {}".format( tally ))

print (statistics.median(dayslist))
print (statistics.mean(dayslist))
print ("max(dayslist)")
print (max(dayslist))
print ("min(dayslist)")
print (min(dayslist))

print("len: {}".format( len(changes)))
print("dic: {}".format( dic))
print("maxdate : {}".format( maxdate ))
print("mindate : {}".format( mindate ))
print (z.percentage(max(changes)))
print (z.percentage(min(changes)))
print (z.percentage(statistics.median(changes)))
print (z.percentage(statistics.mean(changes)))

print (z.percentage(statistics.median(negs)))
print (z.percentage(statistics.mean(negs)))

print("daysapart : {}".format( daysapart ))
