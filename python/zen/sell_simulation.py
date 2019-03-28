import z 
import matplotlib.pyplot as plt

import operator
import random
import sys
from random import sample
import numpy as np
from collections import defaultdict
z.listen()

dates = z.getp("dates")
interval = 7
num_days = len(dates)
print("num_days : {}".format( num_days ))
etfsource = "IUSG"
stocks = z.getStocks(etfsource, preload=True)
#stocks.sort()

ayear = 252
years = 2
duration = int (years * ayear)

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)

tracks = 25
original = 1000
spend = original
minthresh = 350 
fee = 5
miniport = dict()

def getBuyStocks(idxdate, mode):
    thedayh=dict()
    thedayl=dict()
    thedayll=dict()
    for astock in stocks:

        df = z.getCsv(astock)
        if df is None:
            print("problem astock: {}".format( astock))
            continue

        df_dates = df["Date"].tolist() 
        try:
            starti = df_dates.index(idxdate)
            if not starti:
                continue
        except Exception as e:
            continue

        try:
            close = df.at[starti,"Close"]
            if close < 2:
                continue

            changeh = round(close/df.at[starti-3,"Open"],3) 
            changel = round(close/df.at[starti-3,"Open"] - 
                     (close/df.at[starti-8,"Open"])/2,3)
            changell = round(close/df.at[starti-3,"Open"],3) 

        except Exception as e:
            continue

        if changeh > 1:
            thedayh[astock] = round(changeh,4)
        if changel < 1:
            thedayl[astock] = round(changel,4)
        if changell < 1:
            thedayll[astock] = round(changell,4)

    sorted_xl = sorted(thedayl.items(), key=operator.itemgetter(1))
    sorted_xll = sorted(thedayll.items(), key=operator.itemgetter(1))
    sorted_xh = sorted(thedayh.items(), key=operator.itemgetter(1))

    try:
        if mode == "high":
            return sample(sorted_xh[-6:],2)
        elif mode == "low":
            return sample(sorted_xl[:6],2)
        elif mode == "lowlow":
            return sample(sorted_xll[:6],2)
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

        stocks_owned = len(miniport)

        delay = 2.5 if stocks_owned >= tracks else 1
        if idx % int(interval*delay) or idx == 0:
            continue

        if stocks_owned < tracks:
            buyme = getBuyStocks(idxdate, mode)
            for item in buyme:
                astock = item[0]
                if astock not in miniport and stocks_owned < tracks:
                    something = buySomething(dates[idx+start+1], 
                            astock, spend, idxdate)
                    if something:
                        miniport[astock] = something
                        stocks_owned = len(miniport)
        else:
            try:
                spend = sell(spend, idxdate, droppage)
            except:
                try:
                    nextdate = dates[start+idx+1]
                    spend = sell(spend, nextdate, droppage)
                except:
                    print("why not sell miniport:")
                    print(miniport)
                    print("nextdate : {}".format( nextdate ))

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
            newcvalue = max(cvalue, item[1])
            miniport[astock] = [item[0], newcvalue]

    if sells:
        spend = round(spend/len(sells),2)
        for sell in sells:
            del miniport[sell]
        return spend
    return 0

def buySomething(cdate, astock, spend, idxdate):
    try:
        cprice = z.getPrice(astock, cdate)
        if not cprice:
            print("no price cdate: {} {} ".format( cdate, astock))
            print("idxdate: {}".format( idxdate))
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
    for tries in range(10):
        miniport = dict()
        start = random.randrange(num_days-duration)
        end = start + duration
        changes.append(buySellSim(droppage, start, end, mode))

    changes.remove(max(changes))
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
    ddlist = list()
    try:
        ylist = [i/100 for i in range(80,92,4)]
        for droppage in ylist:
            print("droppage : {}".format( droppage ))
#            calcPortfolio(droppage, tlist, mode="both")
            calcPortfolio(droppage, ulist, mode="up")
            calcPortfolio(droppage, dlist, mode="down")
            calcPortfolio(droppage, ddlist, mode="lowlow")

        print(tlist)
        print(ulist)
        print(dlist)
        print(ddlist)

        plt.scatter(ylist, tlist, color="blue")
        plt.scatter(ylist, ulist, color="green")
        plt.scatter(ylist, dlist, color="red")
        plt.scatter(ylist, ddlist, color="red")

        path = z.getPath("plots/{}.png".format(etfsource))
        plt.savefig(path)
        plt.show()

    except Exception as e:
        print ('port: '+ str(e))
        print(tlist)
        print(ulist)
        print(dlist)


getSpread()
