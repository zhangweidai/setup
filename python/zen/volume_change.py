import z
import buy
import statistics
from sortedcontainers import SortedSet

stocks = z.getp("listofstocks")

# shrinking outstanding shares and increasing marketcap with slight volume

dates = z.getp("dates")
sset = SortedSet()
volcdict = dict()
for idx, astock in enumerate(stocks):

    if not idx % 100:
        print("idx: {}".format( idx))

    try:
        avg = list()


        for i, row in enumerate(buy.getRows(astock, dates[-252])):
            try:
                avg.append(int(row['Volume']))
            except:
                break

        if len(avg) < 250:
            continue

        avgo = round(statistics.mean(avg[:30]))
        avgn = round(statistics.mean(avg[-30:]))
        volch = round(avgn/avgo,3)

        if buy.getFrom("latestmc", astock, None) < 2200:
            buy.addSorted("vol_change", volch, astock)

        volcdict[astock] = volch
    except Exception as e:
        continue
        pass

items = buy.getSorted("vol_change")
print("items : {}".format( items ))
buy.multiple(items[-30:], runinit = True)
buy.multiple(items[:30], runinit = True)
z.setp(volcdict, "volcdict")
