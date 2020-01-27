import z
import zen

outname = "ITOT_total_mcsorted"
outd = z.getp(outname)
allowed = list()
for astock in outd[-1000:]:
    allowed.append(astock[1])

buydics = z.getp("buydics")
dates = z.getp("dates")

startd = "2015-04-01"
start = False



changes1 = list()
changes2 = list()
spents1 = list()
spents2 = list()
mchanges1 = list()
mchanges2 = list()
mspents1 = list()
mspents2 = list()
from collections import defaultdict, deque
bought = deque()
mbought = set()
drops = list()
for date in dates:
    if startd == date:
        start = True

    if not start:
        continue

    stock = None
    mstock = None
    buyprices = None
    mbuyprices = None
    minchange = 1
    maxchange = 0
    for astock, items  in buydics.items():
        if astock not in allowed:
            continue
#        print("astock: {}".format( astock))
#        print("items  : {}".format( items  ))
        try:
            change = items[date]
        except:
            continue
        openprice = change[1]

#        if openprice < 90.00:
#            continue

        changed = round(openprice/change[0],3)

        if changed > maxchange and astock not in mbought:
            maxchange = changed
            mstock = astock
            mbuyprices = change

        elif changed < minchange and astock not in bought:
            minchange = changed
#            print("change : {}".format( change ))
#            print("changed: {}".format( changed))
#            print("date: {}".format( date))
            stock = astock
            buyprices = change

#        print("astock: {} {} change {}".format( astock , date, changed))

#        raise SystemExit
    price = zen.getPrice(stock)
    if price:
        bought.append(stock)
        if len(bought) > 30:
            bought.popleft()
#        print("low stock: {}".format( stock))
        change1 = round(price/buyprices[0],3)
        spents1.append(buyprices[0])
        changes1.append(change1)
        drops.append(minchange)
        print("change1: {} {} {} {} ".format( stock, date, round(minchange,3), change1))
        change2 = round(price/buyprices[1],3)
        changes2.append(change2)
        spents2.append(buyprices[1])

    price = zen.getPrice(mstock)
    if price:
        mbought.add(mstock)
        mchange1 = round(price/mbuyprices[0],3)
        mspents1.append(mbuyprices[0])
        mchanges1.append(mchange1)
        mchange2 = round(price/mbuyprices[1],3)
        mchanges2.append(mchange2)
        mspents2.append(mbuyprices[1])

#    print("change1 : {}".format( change1 ))
#    print("change2 : {}".format( change2 ))
s1 = round(sum(spents1),3)
s2 = round(sum(spents2),3)
print("s1 : {}".format( s1 ))
print("s2 : {}".format( s2 ))
print("spents2: {}".format( len(spents2)))
print("changes1: {}".format( z.avg(changes1)))
print("changes2: {}".format( z.avg(changes2)))
print("drops: {}".format( z.avg(drops)))

import statistics
print("drops: {}".format( statistics.median(drops)))
print (statistics.median(changes2))

s1 = round(sum(mspents1),3)
s2 = round(sum(mspents2),3)
print("s1 : {}".format( s1 ))
print("s2 : {}".format( s2 ))
print("spents2: {}".format( len(mspents2)))
print("changes1: {}".format( z.avg(mchanges1)))
print("changes2: {}".format( z.avg(mchanges2)))


