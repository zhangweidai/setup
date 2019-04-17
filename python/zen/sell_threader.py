import z 

import operator
import random
import sys
from random import sample
import zen
from collections import defaultdict
from threading import Lock

z.listen()

mutex = Lock()
dates = z.getp("dates")
interval = 7
num_days = len(dates)
etfsource = "IUSG"
highestValue = 0
lowestValue = 10
savedHigh = None
savedLow = None
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
etfcollector = defaultdict(int)
etfcollectort = defaultdict(int)
#allowStocks = z.getStocks()
etfwins = 0
#temp = z.getp("deletes")
skips = ["WTW", "INGN", "NBR", "XOG", "SWN", "RIG", "MRO"]

def buySellSim(args):
    global etfwins, highestValue, savedHigh, savedLow, lowestValue
    droppage, start, end, mode, typed = args[0], args[1], args[2], args[3], args[4]

    current_transcript = list()
    miniport = dict()

    spend = original
    sub = dates[start:end]
    startd = str(sub[0])
    current_transcript.append(setTranscript("start on {} {} {} {}".format(startd, mode, droppage, typed)))
    maxl = len(sub)-2
    for idx, idxdate in enumerate(sub, start=1):

        stocks_owned = len(miniport)

        delay = 2 if stocks_owned >= buySellSim.tracks else 1
        if idx % int(interval*delay) or idx >= maxl:
            continue
#        print("idxdate : {}".format( idxdate ))
#        print("2idxdate : {}".format( sub[idx]))
#        raise SystemExit

        if stocks_owned < buySellSim.tracks:

            buyme = zen.getSortedStocks(idxdate, mode, get=20, typed=typed)

            if not buyme :
                continue

            for item in buyme:
                astock = item
                if mode != 'r':
                    astock = item[1]

                useme = None
#                if mode == 'r':
#                    useme = item[0]
#                    print("item: {}".format( item))
#                    raise SystemExit

                if astock not in miniport and stocks_owned < buySellSim.tracks and astock not in skips:

                    try:
                        something = buySomething(idxdate, astock, spend, current_transcript, usep=useme)
                    except Exception as e:
                        print("sub: {}".format( len(sub)))
                        print("idx: {}".format( idx))
                        print('problem')
                        print(args)
                        z.trace(e)
                        raise SystemExit
                        continue

                    if something:
                        miniport[astock] = something
                        stocks_owned = len(miniport)
        else:
            try:
                spend, soldc = sell(spend, idxdate, droppage, miniport, current_transcript)
            except:
                pass

        port_change, port_value = getPortValue(idxdate, miniport, current_transcript, spend)
        current_transcript.append(setTranscript("\tcvalue {} {} on {} ".format(port_change, port_value, idxdate)))

    try:
        port_change, port_value = getPortValue(idxdate, miniport, 
                current_transcript, spend)

        etfEnd = zen.getEtfPrice("SPY", idxdate) 
        etfStart = zen.getEtfPrice("SPY", startd)

        etfChange = round(etfEnd/etfStart,3)

    except Exception as e:
        print ('problem getting cprices: '+ str(e))
        return

    modestr = "{}/{}".format(mode, typed)

    tupp = (droppage, modestr)
    collector[tupp].append(port_change)
    etfcollectort[modestr] += 1
    if etfChange > port_change:
        etfwins += 1
        etfcollector[modestr] += 1

    mutex.acquire()
    try:
        if port_change < lowestValue and ("2018-09" in idxdate):
            lowestValue = port_change
            msg = "etf change {} start {} end {}".format(etfChange, etfStart, etfEnd)
            current_transcript.append(setTranscript(msg))
            msg = "finish on {} change {} value {}".format(idxdate, port_change, port_value)
            current_transcript.append(setTranscript(msg))
            z.setp( miniport, "lowest")
            savedLow = current_transcript

        elif port_change > highestValue and ("2019-01" in idxdate or "2018-12" in idxdate):
            msg = "etf change {} start {} end {}".format(etfChange, etfStart, etfEnd)
            current_transcript.append(setTranscript(msg))
            msg = "finish on {} change {} value {}".format(idxdate, port_change, port_value)
            current_transcript.append(setTranscript(msg))
            highestValue = port_change
            savedHigh = current_transcript
            z.setp( miniport, "highest")

    finally:
        mutex.release()

    if not etfwins % 100:
        print (tupp)

buySellSim.tracks = 16

def setTranscript(msg):
    return msg
#    if not setTranscript.enabled:
#        return
#
#    buySellSim.transcript.append(msg)
#    if droppage:
#        path = z.getPath("transcript/{}_{}".format(droppage, mode))
#        print("path: {}".format( path))
#        with open(path, "w") as f:
#            f.write("\n".join(buySellSim.transcript))
#setTranscript.enabled = True

def getEtfWins():
    global etfwins
    return etfwins

def getCollector():
    return collector

def getTranscript():
    return savedHigh, savedLow

def getEtfCollector():
    return etfcollector
def getEtfCollectorT():
    return etfcollectort

def getPortValue(cdate, miniport, current_transcript, spend = 0):
    total = 0
    for astock in miniport:
        cprice = zen.getPrice(astock, cdate)
        item = miniport[astock]
        if cprice:
            cvalue = round((cprice * item[0])-fee,3)
            current_transcript.append(setTranscript("\t\t{} @ {} {}".format(astock, cprice, cvalue)))
            total += cvalue
        else:
            print ("this a problem {} {} ".format(astock, cdate))
            total += item[1]

    added = (((buySellSim.tracks) - len(miniport)) * spend)
    if added > 0:
        total = total + added

    startedwith = buySellSim.tracks*original
    return round(total/startedwith, 3), round(total,4)

def sell(spend, cdate, droppage, miniport, current_transcript):
    sold = None
    sells = []
    spend = 0
    for astock,item in miniport.items():
        try:
            cprice = zen.getPrice(astock, cdate)
        except Exception as e:
            print("selling problem astock: {}".format( astock))
            continue

        if not cprice:
            continue

        cvalue = (cprice * item[0])-fee
        change = round(cvalue/item[1],3)
        if change < droppage and cvalue > minthresh \
                and len(sells) <= 5:

            current_transcript.append(setTranscript("sold {} @ {} on {} change {}".format(
                        astock, cprice, cdate, change )))

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

def buySomething(cdate, astock, spend, current_transcript, usep=None):

    try:
        cprice = usep

        if not cprice:
            cprice = zen.getPrice(astock, cdate)

        if not cprice:
            return None

        if cprice < 5.00:
            return None

        count = round((spend-fee)/cprice,3)

        if spend == 0 or spend-fee <= 0:
            return None

    except Exception as e:
        print ('failedBuys: '+ str(e))
        print("cdate: {}".format( cdate))
        print("astock: {}".format( astock))
        return None

    current_transcript.append(setTranscript("bought {} @ {} on {} (how many {})".format(astock, \
                cprice, cdate, count)))
    return [count, spend-fee]

if __name__ == '__main__':
#    z.getStocks.devoverride = "IUSG"
#    zen.getSortedStocks.get = "low"
#    zen.setSortedDict()
    zen.loadSortedEtf(etf="ITOT")
    buySellSim([.76, 3919, 4473, "r", "low"])
#    buySellSim([.76, 1800, 1800 + 400, "Volume", -1])
    print("etfwins : {}".format( etfwins ))
    print(collector)
    print("savedLow : {}".format( savedLow ))
#getSpread()
