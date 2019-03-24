import util
import operator
import random
import sys
from random import sample
import numpy as np
from collections import defaultdict

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
#print("Seed was:", seed)
#random.seed(3729851342536597050)

#util.getCsv.csvdir = "historical"
spdf = util.getCsv("SPY")
util.getStocks.totalOverride=True
stocks = util.getStocks(noivv = True)
print("stocks : {}".format( len(stocks)))

totalfee = 0

#maxp = None
#maxd = None
#maxv = 0

lastcount = len(spdf)-1

ayear = 252
years = 2
duration = years * ayear

tracks = 25
original = 1000
spend = original
minthresh = 300 
negt = 0.70
fee = 5
interval = 12
miniport = dict()

def doit(start, end):
    lastdate = None
    spend = original
    for idx,row in spdf.iterrows():

        if idx < start or idx > end:
            continue

        if idx % interval or idx == 0:
            continue

        spcdate = row["Date"]

        theday = dict()
        for astock in stocks:
            df = util.getCsv(astock)
            if df is None:
                continue
    
            try:
                dates = list(df["Date"])
                starti = dates.index(spcdate)
                if not starti:
                    continue
            except:
                continue
    
            try:
                close = df.at[starti,"Close"]
                if close < 5:
                    continue
                change = round(close/df.at[starti-3,"Open"],3) - \
                         round(close/df.at[starti-9,"Open"],3)
            except Exception as e:
                continue
    
            if change > 1:
                continue

            theday[astock] = change

        sorted_x = sorted(theday.items(), key=operator.itemgetter(1))
        buyme = sample(sorted_x[:7],2)

        stock_count = len(miniport)
        if stock_count < tracks:
            for item in buyme:
                lowstock = item[0]
                if lowstock not in miniport:
                    something = buySomething(spdf.at[idx+1, "Date"], lowstock, spend)
                    if something:
                        miniport[lowstock] = something
        else:
            try:
                spend = sell(spend, spcdate)
            except:
                nextdate = spdf.at[idx+1, "Date"]
                spend = sell(spend, nextdate)
    try:
        ret = portvalue(spcdate)
    except:
        try:
            nextdate = spdf.at[idx+1, "Date"]
            ret = portvalue(nextdate)
        except Exception as e:
            print ('port: '+ str(e))
            print("nextdate : {}".format( nextdate ))
            raise SystemExit

#    if ret > maxv:
#        maxp = miniport
#        maxd = spcdate
#        maxv = ret
    return ret

def portvalue(cdate):
    total = 0
    for astock in miniport:
        cprice = util.getPrice(astock, cdate)
        item = miniport[astock]
        if cprice:
            cvalue = round((cprice * item[0])-fee)
            total += cvalue
        else:
            total += item[1]

    print("{} {}".format( cdate, total))
    return round(total/(tracks*original),3)

def sell(spend, cdate):
    sold = None
    sells = []
    for astock,item in miniport.items():
        try:
            cprice = util.getPrice(astock, cdate)
        except Exception as e:
            print("astock: {}".format( astock))
            continue

        if not cprice:
            continue

        cvalue = (cprice * item[0])-fee
        if (cvalue/item[1]) < negt and cvalue > minthresh:
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
#    global totalfee
    try:
        cprice = util.getPrice(astock, cdate)
        if not cprice:
            return None
        count = round((spend-fee)/cprice,3)

        if spend == 0 or spend-fee <= 0:
            print("spend : {}".format( spend ))
            print("astock: {}".format( astock))
            print("df : {}".format(len( df)))
            raise SystemExit

    except Exception as e:
        print ('failedBuys: '+ str(e))
        print("astock: {}".format( astock))
        print("df : {}".format(len( df)))
    return [count, spend-fee]

def doits():
    global miniport
    changes = list()
    for b in range(15):
        miniport = dict()
        start = random.randrange(lastcount-duration)
        end = start + duration
        changes.append(doit(start, end))
    vari = np.var(changes)
    average = round(sum(changes)/len(changes),3)
    return vari, average
#doits()

import matplotlib.pyplot as plt
def getSpread():
    global negt
    x1list = list()
    x2list = list()
    ylist = [0.68, 0.72, 0.75, 0.8, 0.85]

    for percent in ylist:
        negt = percent
        print("negt : {}".format( negt ))
        x1, x2 = doits()
        x1list.append(x1)
        x2list.append(x2)

#    print("maxp : {}".format( maxp ))
#    print("maxd : {}".format( maxd ))
#    print("maxv : {}".format( maxv ))
#
    plt.scatter(ylist, x1list, color="red")
    plt.scatter(ylist, x2list, color="blue")
    plt.show()

    saved = [ylist, x1list, x2list]
    util.setp(saved, "sellstrat_3")
#    util.setp(util.getPrice.noprice, "noprices")


getSpread()
