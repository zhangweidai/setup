import z 

import operator
import random
import sys
from random import sample
import generate_list
from collections import defaultdict
from filelock import FileLock

z.listen()

dates = z.getp("dates")
interval = 7
num_days = len(dates)
etfsource = "IUSG"

ayear = 252
years = 2
duration = int (years * ayear)

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)

original = 1000
#spend = original
minthresh = 350 
fee = 5

collector = defaultdict(list)
#allowStocks = z.getStocks()
etfwins = 0
def buySellSim(args):
    global etfwins
    droppage, start, end, mode, price = args[0], args[1], args[2], args[3], args[4]
    buySellSim.transcript = list()

    miniport = dict()
    spend = original
    sub = dates[start:end]
    startd = sub[0]
    setTranscript("start on {}".format(startd))
    for idx, idxdate in enumerate(sub):

        stocks_owned = len(miniport)

        delay = 2 if stocks_owned >= buySellSim.tracks else 1
        if idx % int(interval*delay) or idx == 0:
            continue

        if stocks_owned < buySellSim.tracks:

            buyme = None
            if generate_list.getSortedStocks.get == "price":
                buyme = generate_list.getPricedStocks(idxdate, price)
            else:
                buyme = generate_list.getSortedStocks(idxdate, mode, \
                                                      howmany=4)

            if not buyme :
                continue

            for item in buyme:
                astock = item[1]
                myprice = None
                if generate_list.getSortedStocks.get == "price":
                    myprice = item[0]
                if astock not in miniport and stocks_owned < \
                                              buySellSim.tracks:

                    try:
                        something = buySomething(sub[idx+1], 
                                astock, spend, idxdate, myprice)
                    except:
                        print('problem')
                        print(args)
                        continue

                    if something:
                        miniport[astock] = something
                        stocks_owned = len(miniport)
        else:
            try:
                spend, soldc = sell(spend, idxdate, droppage, miniport)
            except:
                pass

        port_change, port_value = getPortValue(idxdate, miniport)
        setTranscript("\tcvalue {} {} on {} ".format(port_change, 
                    port_value, idxdate))

    try:
        port_change, port_value = getPortValue(idxdate, miniport, spend)
        etfChange = generate_list.getEtfPrice("IVV", idxdate) / \
                generate_list.getEtfPrice("IVV", startd)

    except Exception as e:
        print ('problem getting cprices: '+ str(e))
        return

    with FileLock("sell_threader.lck"):
        if etfChange > port_change:
            etfwins += 1
        collector[(droppage, mode, price)].append(port_change)
#        print("port_change: {}".format( port_change))

    msg = "finish on {} change {} value {}".format(idxdate, 
        port_change, port_value)
    setTranscript(msg, droppage, mode)
buySellSim.tracks = 4

def setTranscript(msg, droppage = None, mode = None):
    if not setTranscript.enabled:
        return

    buySellSim.transcript.append(msg)
    if droppage:
        path = z.getPath("transcript/{}_{}".format(droppage, mode))
        print("path: {}".format( path))
        with open(path, "w") as f:
            f.write("\n".join(buySellSim.transcript))
setTranscript.enabled = True

def getEtfWins():
    global etfwins
    return etfwins

def getCollector():
    return collector

def getPortValue(cdate, miniport, spend = 0):
    total = 0
    for astock in miniport:
        cprice = generate_list.getPrice(astock, cdate)
        item = miniport[astock]
        if cprice:
            cvalue = round((cprice * item[0])-fee,3)
            total += cvalue
        else:
            print ("this a problem")
            total += item[1]

    added = (((buySellSim.tracks) - len(miniport)) * spend)
    if added > 0:
        total = total + added

    startedwith = buySellSim.tracks*original
    return round(total/startedwith, 3), round(total,4)

def sell(spend, cdate, droppage, miniport):
    sold = None
    sells = []
    spend = 0
    for astock,item in miniport.items():
        try:
            cprice = generate_list.getPrice(astock, cdate)
        except Exception as e:
            print("astock: {}".format( astock))
            continue

        if not cprice:
            continue

        cvalue = (cprice * item[0])-fee
        change = round(cvalue/item[1],3)
        if change < droppage and cvalue > minthresh \
                and len(sells) <= 5:

            setTranscript("sold {} @ {} on {} change {}".format(
                        astock, cprice, cdate, change ))

            spend += cvalue
            sells.append(astock)
        else:
            newcvalue = max(cvalue, item[1])
            miniport[astock] = [item[0], newcvalue]

    if sells:
        spend = round(spend/len(sells),2)
        for sell in sells:
            del miniport[sell]
        return spend, len(sells)

    return 0, len(sells)

def buySomething(cdate, astock, spend, idxdate, myprice = None):
    try:
        if myprice:
            cprice = myprice
        else:
            cprice = generate_list.getPrice(astock, cdate)
            if not cprice:
                return None

        count = round((spend-fee)/cprice,3)

        if spend == 0 or spend-fee <= 0:
            return

    except Exception as e:
        print ('failedBuys: '+ str(e))
        print("cdate: {}".format( cdate))
        print("astock: {}".format( astock))
        return

    setTranscript("bought {} @ {} on {} (how many {})".format(astock, \
                cprice, cdate, count))
    return [count, spend-fee]

def calcPortfolio(droppage, alist, mode):
    print("mode: {}".format( mode))
    changes = list()
    for tries in range(13):
        start = random.randrange(num_days-duration)
        end = start + duration
        changes.append(buySellSim(droppage, start, end, mode))

    changes.remove(max(changes))
    changes.remove(max(changes))
    changes.remove(max(changes))

    average = round(sum(changes)/len(changes),3)
    alist.append(average)
    
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

if __name__ == '__main__':
    z.getStocks.devoverride = "IVV"
    generate_list.setSortedDict()
    buySellSim([.85, 1800, 1800 + 100, "Volume", -1])
    print("etfwins : {}".format( etfwins ))
    print(collector)
#getSpread()
