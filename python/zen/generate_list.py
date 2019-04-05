import z 
import operator
from random import sample
import dask_help

from collections import OrderedDict
from sortedcontainers import SortedSet
keeping = 12
discardlocation = int(keeping/2)
import csv

def getScore(idxstart, df):
    minid = 10
    realstart = idxstart-15
    dips = 0 
    gains = 0 
    for idx in range(realstart, idxstart):
        bought = df.at[idx,"Close"]
        now = df.at[idx+1,"Close"]
        change = now/bought
        if change < 1:
            dips += 1-change
        else:
            gains += change

    bought = df.at[realstart,"Close"]
    now = df.at[idxstart,"Close"]
    change = now/bought
    s1 = -1
    if change > 1 and dips:
        s1 = ((change-1)*100)/dips

    bought = df.at[idxstart-4,"Close"]
    now = df.at[idxstart-2,"Close"]
    change = now/bought

    s2 = -1
    if change < 1:
        s2 = round((1-change)*gains,3)

    return s1,s2

volumelist = SortedSet()
def process(astock, col, saveprices, datesdict, yesterday):
    global volumelist
    path = z.getPath("{}/{}.csv".format(dask_help.createRollingData.dir, astock))
    for row in csv.DictReader(open(path)):

        cdate = row['Date']
        if saveprices:
            openp = float(row['Open'])
            closep = float(row['Close'])
            setSortedDict.prices[cdate][astock] = [openp, closep]

        try:
            val = float(row[col])
        except Exception as e:
            continue

        try:
            datesdict[cdate].add((val, astock))
            if col == "Volume" and cdate == yesterday:
                volumelist.add((val, astock))
        except:
            datesdict[cdate] = SortedSet([(val, astock)])

        if len(datesdict[cdate]) > keeping:
            datesdict[cdate].discard(datesdict[cdate][discardlocation])

import datetime
from collections import defaultdict
def setSortedDict(usepkl=True, prices_only=False, etf = None):
    print ('setting sorted dict')

    prefix = ""
    final = setSortedDict.final
    if etf:
        prefix = etf
    if type(z.getStocks.devoverride) == str:
        prefix = z.getStocks.devoverride

    if usepkl:
        print("setSortedDict: {}".format(prefix))
        setSortedDict.prices = z.getp("{}prices{}".format(prefix, 
                                                          final))
        saveEtfPrices.prices = z.getp("etfprices")
        if prices_only:
            return
        setSortedDict.sorteddict = z.getp("{}sorteddict{}".format(
            prefix, final))
        return

    stocks = z.getStocks()
    print("stocks : {}".format( len(stocks)))
    raise SystemExit
    setSortedDict.sorteddict = defaultdict(dict)
    setSortedDict.prices = defaultdict(dict)

    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))

    for i,mode in enumerate(dask_help.getModes()):
        print("mode : {}".format( mode ))
        for astock in stocks:
            process(astock, mode, bool(i==0), setSortedDict.sorteddict[mode], yesterday)

    print("saving")
    z.setp(setSortedDict.sorteddict, "{}sorteddict{}".format(prefix, final))
    z.setp(setSortedDict.prices, "{}prices{}".format(prefix, final))
    print("done saving")

setSortedDict.final = ""
setSortedDict.sorteddict = None
setSortedDict.prices = defaultdict(dict)

def getSortedStocks(date, mode, howmany = 2, getall = False):
    alist = setSortedDict.sorteddict[mode][date]
    if getall:
        return alist
    if getSortedStocks.get == "both":
        return sample(alist,howmany)
    if getSortedStocks.get == "high":
        return sample(alist[-1*discardlocation:],howmany)
    if getSortedStocks.get == "low":
        return sample(alist[:discardlocation],howmany)
getSortedStocks.get = "both"
#    return [alist[0], alist[1]]

def getEtfPrice(astock, date):
    try:
        return saveEtfPrices.prices[date][astock]
    except:
        print("problem etf date: {}".format( date))
        print("astock: {}".format( astock))
        return None

import random
from random import shuffle
def getPricedStocks(idxdate, price):
    stocks = z.getStocks()
    minprice = price * 10
    maxprice = (price+1) * 10
#    shuffle(stocks)
    ret = list()
    for astock in stocks:
        try:
            cprice = getPrice(astock, idxdate)
        except:
            pass

        if not cprice or random.randint(3, 6) != 5:
            continue

        if minprice < cprice < maxprice:
            ret.append((cprice, astock))

        if len(ret) >= 3:
            return ret

    print("price: {}".format( price))
    print("idxdate: {}".format( idxdate))
    print (len(ret))
    return None
#    raise SystemExit

def getLatestPrices():
    try:
        getPrice.latest = z.getp("latestprices")
        if getPrice.latest:
            return
    except:
        pass
#    z.getStocks.devoverride = None
    stocks = z.getStocks("IUSG")
    for astock in stocks:
        path = z.getPath("csv/{}.csv".format(astock))
        for row in csv.DictReader(open(path)):
            pass
        getPrice.latest[astock] = float(row['Close'])
    z.setp(getPrice.latest, "latestprices")

def getPrice(astock, date = None, value = 1, orlatest = False):
    if not date:
        try:
            return getPrice.latest[astock]
        except:
            getLatestPrices()
            return getPrice.latest[astock]
        return None

    try:
        return setSortedDict.prices[date][astock][value]
    except Exception as e:
        pass
    if astock in z.getEtfList():
        try:
            return saveEtfPrices.prices[date][astock]
        except:
            pass
        return None

    try:
        if len(setSortedDict.prices) == 1:
            setSortedDict(prices_only = True)
            return setSortedDict.prices[date][astock][value]
    except:
        pass

    if orlatest:
        try:
            dates = z.getp("dates")
            return setSortedDict.prices[dates[-1]][astock][value]
        except:
            pass

    return None
getPrice.latest = dict()

#z.getStocks.devoverride = "ITOT"
#print (getPricedStocks("2017-01-11", 3))
#raise SystemExit
def getProbSale(astock):
#    for astock in z.getEtfList():
    path = z.getPath("{}/{}.csv".format(dask_help.convertToDask.directory, astock))
    count = 0
    downs = 0
    avgl = list()
    avgd = list()
    for row in csv.DictReader(open(path)):
        opend = float(row['Open'])
        close = float(row['Close'])
        change = close/opend
        if change < 1:
            downs += 1
            avgd.append(change)
        count += 1
        avgl.append(change)
    avgret = z.avg(avgl)
    avgd = z.avg(avgd)
    change = round(downs/count,3)
    return avgret, change, z.percentage(avgd)

def saveEtfPrices():
    for astock in z.getEtfList():
        path = z.getPath("{}/{}.csv".format(dask_help.convertToDask.directory, astock))
        for row in csv.DictReader(open(path)):
            cdate = row['Date']
            saveEtfPrices.prices[cdate][astock] = float(row['Close'])
    z.setp(saveEtfPrices.prices, "etfprices")
saveEtfPrices.prices = defaultdict(dict)

def regenerateHistorical():
    dask_help.convertToDask.directory = "historical"
    dask_help.createRollingData.dir = "historicalCalculated"

    for etf in z.getEtfList():
        print("etf : {}".format( etf ))
        z.getStocks.devoverride = etf
        z.getStocks(reset=True)
        setSortedDict(usepkl = False)


def setVolumeRanking():
    volumelist = z.getp("latestvolume")
    setVolumeRanking.latestvoldic = dict()
    for i,item in enumerate(volumelist):
        setVolumeRanking.latestvoldic[item[1]] = i
    z.setp(setVolumeRanking.latestvoldic, "latestvolumedic")
setVolumeRanking.latestvoldic = None

def whatAboutThese(volumelist, count = 30, lowprice = False):
    print(" {0:<6} {1:<4} $ {2:<7} {3:<7} {4:<7} {5:<7}".format("stock", "vol", "price", "avgC", "probD", "avgD"))
    for i,value in enumerate(volumelist):
        stock = value
        vrank = i+1
        try:
            if type(value) is tuple:
                stock = value[1]
                vrank = getVolumeRanking(stock)

            price = round(getPrice(stock),2)
            if lowprice and price > 50:
                continue
            avgC, probD, avgD = getProbSale(stock)
            print(" {0:<6} {1:<4} $ {2:<7} {3:<7} {4:<7} {5:<7}".format(stock, \
                                   vrank, price, avgC, probD, avgD))
            if i > count:
                break

        except Exception as e:
            continue

def getVolumeRanking(astock = None):
    if type(astock) is str: 
        try:
            return setVolumeRanking.latestvoldic[astock]
        except:
            setVolumeRanking.latestvoldic = z.getp("latestvolumedic")
        return setVolumeRanking.latestvoldic[astock]
    elif type(astock) is int:
        volumelist = z.getp("latestvolume")
        whatAboutThese(volumelist, count=astock)

if __name__ == '__main__':
    import util
    dask_help.convertToDask.directory = "csv"
#    print (getProbSale("BA"))
#    raise SystemExit
    whatAboutThese(z.getConsider())
    raise SystemExit
#    getVolumeRanking(30)
    import sys
    import zprep
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "query":
                z.getStocks.devoverride = "IUSG"
                setSortedDict.final = "Final"
                setSortedDict(usepkl = True)
                yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
                today = str(datetime.date.today())
                for mode in dask_help.getModes():
                    print("\nmode : {}".format( mode ))
                    stocks = (getSortedStocks(yesterday, mode, getall=True))
                    whatAboutThese(stocks)

            if sys.argv[1] == "buy" or sys.argv[1] == 'gbuy':
                dask_help.convertToDask.directory = "csv"
                dask_help.createRollingData.dir = "csvCalculated"
                z.getStocks.devoverride = "IUSG"
                z.getStocks.extras = True
                if sys.argv[1] == 'gbuy':
                    try:
                        zprep.genBuyList()
                        dask_help.convertToDask()
                    except Exception as e:
                        print (str(e))
                        exit()
                setSortedDict.final = "Final"
                setSortedDict(usepkl = False)
                z.setp(volumelist, "latestvolume")
    except Exception as e:
        print (str(e))
        pass
