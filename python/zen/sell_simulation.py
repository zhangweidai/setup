import z 

import operator
import random
import sys
from random import sample
import numpy as np
import zen
from collections import defaultdict
from termcolor import colored

z.listen()

dates = z.getp("dates")
interval = 7
num_days = len(dates)
print("num_days : {}".format( num_days ))
etfsource = "IUSG"
zen.getBuyStocks.stocks = z.getStocks(etfsource)
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

collector = dict()

def buySellSim(droppage, start, end, mode, miniport):
    spend = original
    for idx, idxdate in enumerate(dates[start:end]):

        stocks_owned = len(miniport)

        delay = 3 if stocks_owned >= tracks else 1
        if idx % int(interval*delay) or idx == 0:
            continue

        if stocks_owned < tracks:
            buyme = zen.getBuyStocks(idxdate, mode)
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
                    pass
#                    print("why not sell miniport:")
#                    print(miniport)
#                    print("nextdate : {}".format( nextdate ))

    try:
        port_value = portvalue(idxdate, miniport)
    except:
        try:
            nextdate = dates[idx+1]
            port_value = portvalue(nextdate, miniport)
        except Exception as e:
            print ('port: '+ str(e))
            print("nextdate : {}".format( nextdate ))
            raise SystemExit

    return port_value

def portvalue(cdate, miniport):
    total = 0
    for astock in miniport:
        cprice = z.getPrice(astock, cdate)
        item = miniport[astock]
        if cprice:
            cvalue = round((cprice * item[0])-fee,3)
            total += cvalue
        else:
            total += item[1]

    total = round(total,3)
    ret = round(total/((tracks-1)*original),3)
    if ret < 1:
        total = colored(total,"red")
    print("Ending Date {} - total: {}".format( cdate,
                    total,2))

    return ret

def sell(spend, cdate, droppage, miniport):
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
    print("mode: {}".format( mode))
    changes = list()
    for tries in range(13):
        miniport = dict()
        start = random.randrange(num_days-duration)
        end = start + duration
        changes.append(buySellSim(droppage, start, end, mode, miniport))

    changes.remove(max(changes))
    changes.remove(max(changes))
    changes.remove(max(changes))

    vari = np.var(changes)
    average = round(sum(changes)/len(changes),3)
    alist.append(average)
    
#    return vari, average
#calcPortfolio()

def getSpread():
#    x1list = list()
#    x2list = list()

    tlist = list()
    ulist = list()
    dlist = list()
    ddlist = list()
    try:
        ylist = [i/100 for i in range(76,92,2)]
        for droppage in ylist:
            print("droppage : {}".format( droppage ))
            calcPortfolio(droppage, tlist, mode="special2")
            calcPortfolio(droppage, ulist, mode="special1")
            calcPortfolio(droppage, dlist, mode="low")
            calcPortfolio(droppage, ddlist, mode="lowlow")

        print(tlist)
        print(ulist)
        print(dlist)
        print(ddlist)

        for i,droppage in enumerate(ylist):
            tosum=[]
            tosum.append(tlist[i])
            tosum.append(ulist[i])
            tosum.append(dlist[i])
            tosum.append(ddlist[i])
            print("droppage : {} = {} ".format( droppage, z.avg(tosum) ))

        print("averages")
        print(z.avg(tlist))
        print(z.avg(ulist))
        print(z.avg(dlist))
        print(z.avg(ddlist))

        import matplotlib.pyplot as plt
        plt.scatter(ylist, tlist, color="blue")
        plt.scatter(ylist, ulist, color="green")
        plt.scatter(ylist, dlist, color="red")
        plt.scatter(ylist, ddlist, color="black")

        path = z.getPath("plots/{}_special.png".format(etfsource))
        plt.savefig(path)
        plt.show()

    except Exception as e:
        import traceback
        print (traceback.format_exc())
        print ('port: '+ str(e))
        print(tlist)
        print(ulist)
        print(dlist)
        print(ddlist)


getSpread()
