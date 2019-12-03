
from collections import defaultdict
from sortedcontainers import SortedSet
with open("openorders", "r") as f:
    bar = f.readlines()

import z
import zen

orders = defaultdict(list)
tory = False
torys = list()
for aline in bar:
    if "Z03895009" in aline:
        tory = True
    tokens = aline.split("\t")
    for token in tokens:
        if "Buy " not in token:
            continue
        items = token.split(" ")
        count = int(items[1])
        astock = items[4]
        price = float(items[7][1:].replace(",", ""))
        value = count * price
        orders[astock].append((value, price))
        if tory:
            torys.append(astock)
        
z.setp(torys, "torys")
z.setp(orders, "orders", printdata=True)
exit()

sorteds = SortedSet()
dics = defaultdict(int)
total = 0
probdics = defaultdict(int)
orders = defaultdict(list)
for aline in bar:
    tokens = aline.split("\t")
    for token in tokens:
        if "Buy " not in token:
            continue
        items = token.split(" ")
        count = int(items[1])
        astock = items[4]
        try:
            price = float(items[7][1:])
            cprice = z.getPrice(astock)
            value = count * price
            total += value
            percent = round(round(1-(price / cprice),3),3)
            percentile = round(percent/0.05)
            dics[percentile] += value
            sorteds.add(percentile)

            targets = zen.getTargets(astock, asint = True)
            cat = "RARE"
            if price < targets[0]:
                cat = "RARE"
            elif price < targets[1]:
                cat = "MEDIUM_RARE"
            else:
                splitter = (targets[1] + cprice)/2
                if price < splitter:
                    cat = "LESS_LIKELY"
                else:
                    cat = "MORE_LIKELY"
            probdics[cat] += value
            print("stock : {:>7} percent away:{:>7}  investment:{:>7}  cprice:{:>7}  buy:{:>7}  low:{:>7} high:{:>7} {:>7} {}".format( astock , percent , value, cprice, price, targets[0], targets[1], percentile, cat))
        except Exception as e:
            print("\tdidnt have something astock: {} {} {}".format( astock, value, price))
            pass
#print("dics: {}".format( dics))
#print("sorteds: {}".format( sorteds))
print("total : {}".format( total ))

for per in sorteds:
    print("\t{} : {}".format(per, dics[per] ))

print ("\nCATEGORIZED")
for per in probdics.keys():
    print("\t{} : {}".format(per, probdics[per] ))

