
from collections import defaultdict
from sortedcontainers import SortedSet

with open("openorders", "r") as f:
    bar = f.readlines()

import z

orders = defaultdict(list)
tory = False
torys = list()
stocks = z.getp("listofstocks")
for aline in bar:
    if "Z03895009" in aline:
        tory = True
    tokens = aline.split("\t")
    for token in tokens:
        if "Buy " not in token:
            continue
        items = token.split(" ")
        for i,token in enumerate(items):
            if token == 'Buy':
                count = int(items[i+1])
                astock = items[i+4]
                try:
                    price = float(items[i+7][1:].replace(",", ""))
                except:
                    try:
                        price = float(items[i+6][1:].replace(",", ""))
                        astock = items[i+3]
                    except:
                        print("items: {}".format( items))
                        print("items: {}".format( i))
                        exit()

                if astock not in stocks:
                    print("WHAT IS THIS astock : {}".format( astock ))
                    print("WHAT IS THIS astock : {}".format( aline ))
                value = count * price
                orders[astock].append((value, price))
                if tory:
                    torys.append(astock)
        
z.setp(torys, "torys")
z.setp(orders, "orders", printdata=True)
exit()
