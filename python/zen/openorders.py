import datetime
from collections import defaultdict
from sortedcontainers import SortedSet

with open("openorders", "r") as f:
    bar = f.readlines()

import z
import re
def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

orders = defaultdict(list)
tory = False
torys = list()
stocks = z.getp("listofstocks")
total = 0
dates = None
next1 = False
account_orders = defaultdict(int)
num = None
for aline in bar:
    if "Z03895009" in aline:
        tory = True
    tokens = aline.split("\t")
    for x, token in enumerate(tokens):
        if token == '\n':
            continue

        if token:
            try:
                dates = datetime.datetime.strptime(token.strip(),"%m/%d/%Y")
            except ValueError as err:
                dates  = None
                pass


        if next1:
            account = token
            if hasNumbers(account):
                num = account.strip().split(" ")[-1][-5:]
                dates = None
                next1 = None

        if dates:
            next1 = True


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
                total += value
                account_orders[num] += value
                orders[astock].append((value, price))
                if tory:
                    torys.append(astock)
        
print("cash total : {}".format( total ))
print("account_orders: {}".format( account_orders))

z.setp(account_orders, "account_orders")
z.setp(torys, "torys")
z.setp(orders, "orders", printdata=True)

accounts = z.getp("accounts")
print("accounts: {}".format( accounts))
mapped = dict()
mapped["33615"] = "mine_b"
mapped["02560"] = "mine_t"
mapped["46278"] = "mine_r"
mapped["65133"] = "brokel"
mapped["65134"] = "broker"
mapped["60432"] = "health"
mapped["95009"] = "tory_b"
mapped["91881"] = "tory_t"
mapped["73208"] = "tory_r"

for account in accounts:
    last5 = account[-5:]

    if last5 not in accounts:
        continue

    one = accounts[last5]
    two = account_orders[last5] 
    try:
        print("last5 : {:>5} \tcash : {:>8} \torders {:>8} \tratio {:>3}".format( mapped[str(last5)], one, two, round(two/one,2)))
    except Exception as e:
        pass

import current
import table_print
current.procs(orders.keys(), "orders")
table_print.initiate()
