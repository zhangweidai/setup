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
    for i,value in enumerate(volumelist):
        stock = value
        vrank = i+1
        try:
            if type(value) is tuple:
                stock = value[1]
            else:
                vrank = getVolumeRanking(stock)

            price = getPrice(stock)
            if lowprice and price > 50:
                continue
            print("value : {0:<6} {1:<3} $ {2}".format(stock, vrank, price))
            if i > count:
                break
        except:
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
    whatAboutThese(util.getConsider())
#    getVolumeRanking(30)
    import sys
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "query":
                z.getStocks.devoverride = "IUSG"
                setSortedDict.final = "Final"
                setSortedDict(usepkl = True)
                yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
                today = str(datetime.date.today())
                for mode in dask_help.getModes():
                    print("{:*^30}".format( mode ))
                    stocks = (getSortedStocks(yesterday, mode, getall=True))
                    for astock in stocks:
                        number = astock[0]
                        astock = astock[1]
                        vrank = getVolumeRanking(astock)
                        price = getPrice(astock)
                        if price < 50 or vrank < 100:
                            print("{0:<6} {1:<10} {2:<5} $ {3:<6}".format(astock, number, vrank, price))

            if sys.argv[1] == "buy":
                dask_help.convertToDask.directory = "csv"
                dask_help.createRollingData.dir = "csvCalculated"
                setSortedDict.final = "Final"
                z.getStocks.devoverride = "IUSG"
                setSortedDict(usepkl = False)
                z.setp(volumelist, "latestvolume")
    except Exception as e:
        print (str(e))
        pass

#    regenerateHistorical()

#    getSortedStocks.get = "low"
#    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
#    print("yesterday : {}".format( yesterday ))
#    for i,mode in enumerate(dask_help.getModes()):
#        alist = getSortedStocks(yesterday, mode, getall=True)
#        for item in alist:
#            astock = item[1]
#            value = getPrice(astock, yesterday)
#            if value < 30:
#                print("{} at {}".format(astock, value))
#    z.getStocks.devoverride = "IUSG"
#    setSortedDict()
#    alist = getSortedStocks("2019-03-06", "Volume", howmany = 2)
#    print(alist)
#
#    getSortedStocks.get = "high"
#    setSortedDict()
#    alist = getSortedStocks("2019-03-06", "Volume", howmany = 2)
#    print(alist)

