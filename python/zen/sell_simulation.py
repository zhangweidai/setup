import z 
import matplotlib.pyplot as plt

import operator
import random
import sys
from random import sample
import numpy as np
from collections import defaultdict

dates = z.getp("dates")
interval = 20
num_days = len(dates)
print("num_days : {}".format( num_days ))

stocks = z.getStocks("IVV")

ayear = 252
years = 3
duration = int (years * ayear)

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)

tracks = 25
original = 1000
spend = original
minthresh = 400 
fee = 5
miniport = dict()

def getBuyStocks(idxdate, mode):
    thedayh=dict()
    thedayl=dict()
    for astock in stocks:

        df = z.getCsv(astock)
        if df is None:
            continue

        try:
            starti = dates.index(idxdate)
            if not starti:
                continue
        except Exception as e:
            print ('po: '+ str(e))
            continue

        try:
            close = df.at[starti,"Close"]
            if close < 2:
                continue

            changeh = round(close/df.at[starti-3,"Open"],3) 
            changel = round(close/df.at[starti-3,"Open"] - 
                     (close/df.at[starti-8,"Open"])/2,3)

        except Exception as e:
            print("starti: {}".format( starti))
            print("astock: {}".format( astock))
            print ('pxort: '+ str(e))
            raise SystemExit
            continue

        if changeh > 1:
            thedayh[astock] = round(changeh,4)
        if changel < 1:
            thedayl[astock] = round(changel,4)

    sorted_xl = sorted(thedayl.items(), key=operator.itemgetter(1))
    sorted_xh = sorted(thedayh.items(), key=operator.itemgetter(1))

    try:
        if mode == "high":
            return sample(sorted_xh[-6:],2)
        elif mode == "low":
            return sample(sorted_xl[:6],2)
    except:
        print("sorted_xl: {}".format( sorted_xl))
        print("sorted_xh: {}".format( sorted_xh))
        raise SystemExit

    try:
        return [sample(sorted_xh[-6:],1)[0], sample(sorted_xl[:6],1)[0]]
    except:
        print("sorted_xl: {}".format( sorted_xl))
        print("sorted_xh: {}".format( sorted_xh))
        raise SystemExit

def buySellSim(droppage, start, end, mode):
    spend = original
    for idx, idxdate in enumerate(dates[start:end]):

        if idx % interval or idx == 0:
            continue

        buyme = getBuyStocks(idxdate, mode)

        stock_count = len(miniport)
        if stock_count < tracks:

            for item in buyme:
                astock = item[0]
                if astock not in miniport and stock_count < tracks:
                    something = buySomething(dates[idx+1], astock, spend)
                    if something:
                        miniport[astock] = something
                        stock_count = len(miniport)
        else:
            try:
                spend = sell(spend, idxdate, droppage)
            except:
                nextdate = dates[idx+1]
                spend = sell(spend, nextdate, droppage)
    try:
        port_value = portvalue(idxdate)
    except:
        try:
            nextdate = dates[idx+1]
            port_value = portvalue(nextdate)
        except Exception as e:
            print ('port: '+ str(e))
            print("nextdate : {}".format( nextdate ))
            raise SystemExit

    print("port_value: {}".format( port_value))
    return port_value

def portvalue(cdate):
    total = 0
    for astock in miniport:
        cprice = z.getPrice(astock, cdate)
        item = miniport[astock]
        if cprice:
            cvalue = round((cprice * item[0])-fee)
            total += cvalue
        else:
            total += item[1]

    print("{} {}".format( cdate, total))
    return round(total/(tracks*original),3)

def sell(spend, cdate, droppage):
    sold = None
    sells = []
    for astock,item in miniport.items():
        try:
            cprice = z.getPrice(astock, cdate)
        except Exception as e:
            print("astock: {}".format( astock))
            continue

        if not cprice:
            continue

        cvalue = (cprice * item[0])-fee
        if (cvalue/item[1]) < droppage and cvalue > minthresh:
            spend += cvalue
            sells.append(astock)
        else:
            miniport[astock] = [item[0], cvalue]

    if sells:
        spend = round(spend/len(sells),2)
        for sell in sells:
            del miniport[sell]
    return spend

def buySomething(cdate, astock, spend):
    try:
        cprice = z.getPrice(astock, cdate)
        if not cprice:
            return None
        count = round((spend-fee)/cprice,3)

        if spend == 0 or spend-fee <= 0:
            print("spend : {}".format( spend ))
            print("astock: {}".format( astock))
            print("df : {}".format(len(df)))
            raise SystemExit

    except Exception as e:
        print ('failedBuys: '+ str(e))
        print("astock: {}".format( astock))
        print("df : {}".format(len( df)))
    return [count, spend-fee]

def calcPortfolio(droppage, alist, mode):
    global miniport
    changes = list()
    for b in range(25):
        miniport = dict()
        start = random.randrange(num_days-duration)
        end = start + duration
        changes.append(buySellSim(droppage, start, end, mode))
        print("changes: {}".format( changes))
        raise SystemExit
        

    changes.remove(max(changes))

    vari = np.var(changes)
    average = round(sum(changes)/len(changes),3)
    alist.append(average)
    
#    return vari, average
#calcPortfolio()

def getSpread():
    global tracks, minthresh
#    x1list = list()
#    x2list = list()

    tlist = list()
    ulist = list()
    dlist = list()

    ylist = [i/100 for i in range(75,84)]
    for droppage in ylist:
        print("droppage : {}".format( droppage ))

        calcPortfolio(droppage, tlist, mode="both")
        raise SystemExit
        calcPortfolio(droppage, ulist, mode="up")
        calcPortfolio(droppage, dlist, mode="down")
#        x1list.append(x1)
#        x2list.append(x2)
#        print(x1list)
#        print(x2list)

    plt.scatter(ylist, tlist, color="blue")
    plt.scatter(ylist, ulist, color="green")
    plt.scatter(ylist, dlist, color="red")

    plt.show()


getSpread()
