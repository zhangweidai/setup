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

#print ("startreading")
#util.getCsv.savedReads = util.getp("allcsvs")
#print ("endreading")

spdf = util.getCsv("SPY")
stocks = util.getStocks()
print("stocks : {}".format( len(stocks)))

totalfee = 0
oneofeach = False

#maxp = None
#maxd = None
#maxv = 0

lastcount = len(spdf)-1

ayear = 252
years = 3.5
duration = years * ayear

tracks = 25
original = 1000
spend = original
minthresh = 400 
negt = 0.70
fee = 5
interval = 20
miniport = dict()

gethigh = False
getrandom = False
def getBuyStocks(spcdate = None):
    thedayh = dict()
    thedayl = dict()
#    tstocks = sample(stocks,400)
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
        changeh = None
        changel = None
        try:
            close = df.at[starti,"Close"]
            if close < 2:
                continue

            changeh = round(close/df.at[starti-3,"Open"],3) 
            changel = round(close/df.at[starti-3,"Open"] - 
                     close/df.at[starti-8,"Open"], 4)

        except Exception as e:
            continue

#        if change > 1:
#            continue
        if changeh > 1:
            thedayh[astock] = round(changeh,4)
        if changel < 1:
            thedayl[astock] = round(changel,4)

    sorted_xl = sorted(thedayl.items(), key=operator.itemgetter(1))
    sorted_xh = sorted(thedayh.items(), key=operator.itemgetter(1))

    return [sample(sorted_xh[-12:],6), sample(sorted_xl[:12],6)]

#    if gethigh:
#        return sample(sorted_x[-6:],2)
#
#    return sample(sorted_x[:6],2)

#getrandom = True
#print (getBuyStocks("2019-03-22"))
#raise SystemExit

def doit(start, end):
    lastdate = None
    spend = original
    for idx in spdf.index:

        if idx < start or idx > end:
            continue

        if idx % interval or idx == 0:
            continue

        spcdate = spdf.at[idx,"Date"]

        buyme = getBuyStocks(spcdate)

        stock_count = len(miniport)
        if stock_count < tracks:

            for item in buyme:
                lowstock = item[0]

                if lowstock not in miniport and stock_count < tracks:
                    something = buySomething(spdf.at[idx+1, "Date"], 
                                             lowstock, spend)
                    if something:
                        miniport[lowstock] = something
                        stock_count = len(miniport)
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
    for b in range(25):
        miniport = dict()
        start = random.randrange(lastcount-duration)
        end = start + duration
        changes.append(doit(start, end))

    changes.remove(max(changes))

    vari = np.var(changes)
    average = round(sum(changes)/len(changes),3)
    return vari, average
#doits()

import matplotlib.pyplot as plt
def getSpread():
    global negt, gethigh, getrandom, tracks, minthresh
    x1list = list()
    x2list = list()
    ylist = [1,2,3,4,5,6]

    negt = 0.77

    x1, x2 = doits()
    x1list.append(x1)
    x2list.append(x2)
    print(x1list)
    print(x2list)

    x1, x2 = doits()
    x1list.append(x1)
    x2list.append(x2)
    print(x1list)
    print(x2list)

    x1, x2 = doits()
    x1list.append(x1)
    x2list.append(x2)
    print(x1list)
    print(x2list)
 
    minthresh = 800 
    original = 2000
    tracks = 13

    x1, x2 = doits()
    x1list.append(x1)
    x2list.append(x2)
    print(x1list)
    print(x2list)

    x1, x2 = doits()
    x1list.append(x1)
    x2list.append(x2)
    print(x1list)
    print(x2list)

    x1, x2 = doits()
    x1list.append(x1)
    x2list.append(x2)
    print(x1list)
    print(x2list)


    plt.scatter(ylist, x1list, color="red")
    plt.scatter(ylist, x2list, color="blue")

#    saved = [ylist, x1list, x2list]
#    util.setp(saved, "sellstrat_4")

    plt.show()
#    util.setp(util.getPrice.noprice, "noprices")


getSpread()
