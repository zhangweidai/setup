import z
from collections import defaultdict, deque
from threading import Lock
from sortedcontainers import SortedSet
import csv
import numpy as np
import os

modes = [ 'Volume', 'Price', "C24", "C50", "CAvg", "Avg50", "Var50", "Drops"]

def getModes():
    if getModes.useRandom:
        return ['r'] + modes
    return modes
getModes.useRandom = False

keeping = 60
discardlocation = int(keeping/2)

sdict = None
ydict = None
pdict = None
pdict2 = None
closekey = z.closekey

import random
aset = set()
def saveDates(astock):
    global ydict
    path = z.getPath("historical/{}.csv".format(astock))
    try:
        for row in csv.DictReader(open(path)):
            date = row['Date']
            tokens = date.split("-")
            year = int(tokens[0])
            if year < 2013:
                continue

            close = round(float(row[closekey]),2)
            if random.randint(0, 85) == 1:
                ydict[date].append((close, astock))
                aset.add(astock)

            if astock in aset:
                pdict2[astock][date] = close
    except:
        pass

def doone(astock, directory = "historical", complete = False):
    path = z.getPath("{}/{}.csv".format(directory, astock))
    volumes = deque([])
    closes = deque([])
    changes = deque([])
    opens = deque([])
    drops = deque([])
    prevyear = None
    firstdate = None

    for row in csv.DictReader(open(path)):
        date = row['Date']
        tokens = date.split("-")
        year = int(tokens[0])

        if (year > 2012) or (year == 2012 and int(tokens[1]) > 8):
            c = float(row[closekey])
            closes.append(c)

            if not firstdate:
                firstdate = c
                if firstdate < 2.00:
                    return

            volumes.append(int(row['Volume']))

            o = float(row['Open'])
            opens.append(o)

            change = round(c/o,3)
            changes.append(change)
            if change < 1.0:
                drops.append(1-change)

            if len(volumes) > 5:
                volumes.popleft()

            if len(drops) > 51:
                drops.popleft()

            if len(closes) > 51:
                closes.popleft()
                opens.popleft()
                changes.popleft()

        ydict[date].append(astock)
        if year < 2013:
            continue

        changel = list(changes)

        if not prevyear:
            prevyear = year

        close = float(row[closekey])

        pdict[astock][date] = close

        if year != prevyear:
            prevyear = year

        if len(closes) < 25:
            continue

        for mode in modes:
            if mode == "C5":
                value = round(close/closes[-5],3)

            elif mode == "C24":
                value = round(close/closes[-24],3)

            elif mode == "C50":
                try:
                    value = round(close/closes[-50],3)
                except:
                    continue

            elif mode == "CAvg":
                value = round(close/z.avg(opens),3)

            elif mode == "Avg20":
                value = z.avg(changel[:20], p=5)

            elif mode == "Avg50":
                value = z.avg(changel, p=5)

            elif mode == "Var50":
                value = round(np.var(changel)*1000,3)

            elif mode == "Drops":
                value = round(sum(drops),3)

            elif mode == "Volume":
                try:
                    value = z.avg(volumes)
                except:
                    value = int(row['Volume'])
                value = round(value/10000,3)
            else:
                value = close
            try:
                sdict[mode][date].add((value, astock))
            except Exception as e:
                try:
                    sdict[mode][date] = SortedSet([(value, astock)])
                except Exception as e:
                    z.trace(e)
                    raise SystemExit                    

            if not complete:
                if len(sdict[mode][date]) > keeping:
                    sdict[mode][date].discard(sdict[mode][date][discardlocation])

def regenerate(stocks, code, directory):
    global sdict, pdict, ydict
    ydict = defaultdict(list)
    sdict = defaultdict(dict)
    pdict = defaultdict(dict)
    problems = z.getp("problems")
    for idx,astock in enumerate(stocks):

        if type(astock) != str:
            astock = astock[1]

        if not idx % 100:
            print("idx : {}".format( idx ))

        try:
            doone(astock, directory)
        except Exception as e:
            print("problem astock: {}".format( astock))
            z.trace(e)
            pass

    z.setp(ydict, "{}_Y".format(code))
    z.setp(sdict, "{}_SS".format(code))
    z.setp(pdict, "{}_P".format(code))

def regenerateBEtfs():
    import update_history
    import zen

    stocks = zen.getLongEtfList()
    download = False
    if download:
        for astock in stocks:
            try:
                df = update_history.getDataFromYahoo(astock, "2010-01-05")
            except:
                continue
            if df is not None:
                path = z.getPath("ETF/{}.csv".format(astock))
                df.to_csv(path)
    regenerate(stocks, "ETF", "ETF")

def regenerateBUY():
    print ("regenerating BUY2 from ITOT_total_mcsorted")
    stocks = z.getp("ITOT_total_mcsorted")
    stocks = stocks[-1048:]
    regenerate(stocks, "BUY2", "historical")

def doit_buys():
    global sdict, pdict, ydict
    ydict = defaultdict(list)
    sdict = defaultdict(dict)
    pdict = defaultdict(dict)
    stocks = z.getStocks("IUSG|IWB", reset=True)
    for astock in stocks:
        try:
            doone(astock)
        except Exception as e:
            print("astock: {}".format( astock))
            z.trace(e)
            pass
    z.setp(ydict, "BUY_Y")
    z.setp(sdict, "BUY_SS")
    z.setp(pdict, "BUY_P")

def doit(etf):
    global sdict, pdict, ydict
    ydict = defaultdict(list)
    sdict = defaultdict(dict)
    pdict = defaultdict(dict)
    stocks = z.getStocks(etf, reset=True)
    for astock in stocks:
        try:
            doone(astock)
        except Exception as e:
            print("astock: {}".format( astock))
            z.trace(e)
            pass
    z.setp(ydict, "{}_Y".format(etf))
    z.setp(sdict, "{}_SS".format(etf))
    z.setp(pdict, "{}_P".format(etf))

def genSortedSets():
#    for etf in ["ITOT"]:
    for etf in z.getEtfList(forEtfs = True):
        print("etf : {}".format( etf ))
        doit(etf)

if __name__ == '__main__':
    regenerateBUY()
#    regenerateBEtfs()
    raise SystemExit
#    genSortedSets()

    stocks = z.getStocks("ITOT", reset=True)
    ydict = defaultdict(list)
    pdict2 = defaultdict(dict)
    for astock in stocks:
        try:
            saveDates(astock)
        except Exception as e:
            print("astock: {}".format( astock))
            z.trace(e)
            pass
    print("aset : {}".format( len(aset)))
    z.setp(ydict, "ITOT_Y")
    z.setp(pdict2, "ITOT_P2")

