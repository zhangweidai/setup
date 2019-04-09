import z 
import operator
from random import sample
import util
import dask_help

from collections import OrderedDict
from sortedcontainers import SortedSet
keeping = 40
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

def process(astock, col, saveprices, datesdict):
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
        load = "{}sorteddict{}".format(prefix, final)
        print("loading sorteddict : {}".format(load))
        setSortedDict.prices = z.getp("{}prices{}".format(prefix, final))
        saveEtfPrices.prices = z.getp("etfprices")
        if prices_only:
            return
        setSortedDict.sorteddict = z.getp(load)
        if setSortedDict.sorteddict:
            return
    print ('rebuilding sorted dict')

    stocks = z.getStocks(reset=True)
    setSortedDict.sorteddict = defaultdict(dict)
    setSortedDict.prices = defaultdict(dict)

    for i,mode in enumerate(dask_help.getModes()):
        print("mode : {}".format( mode ))
        for astock in stocks:
            try:
                process(astock, mode, bool(i==0), setSortedDict.sorteddict[mode])
            except:
                continue

    print("saving")
    z.setp(setSortedDict.sorteddict, "{}sorteddict{}".format(prefix, final))
    z.setp(setSortedDict.prices, "{}prices{}".format(prefix, final))
    print("done saving")
setSortedDict.final = ""
setSortedDict.sorteddict = None
setSortedDict.prices = defaultdict(dict)

def getSortedStocks(date, mode, howmany = 2, 
        getall = False, typed=None, reportprob = True):
    if not typed:
        typed = getSortedStocks.get
    try:
        alist = setSortedDict.sorteddict[mode][date]
    except Exception as e:
        if reportprob:
            print("dates: {}".format(len(setSortedDict.sorteddict[mode])))
            print("date: {}".format( date))
            print("mode: {}".format( mode))
            z.trace(e)
            raise SystemExit
#        setSortedDict(usepkl=True, etf=z.getStocks.devoverride)
#        alist = setSortedDict.sorteddict[mode][date]

    if not typed and getall:
        return alist

    if typed == "both":
        ret = sample(alist,howmany)
        return ret
    if typed == "high":
        ret = sample(alist[-1*discardlocation:],howmany)
        return ret
    if typed == "low":
        if getall:
            ret = alist[:discardlocation]
        else:
            ret = sample(alist[:discardlocation],howmany)
        return ret
getSortedStocks.get = "both"

def getEtfPrice(astock, date):
    try:
        return saveEtfPrices.prices[date][astock]
    except:
        try:
            saveEtfPrices()
            return saveEtfPrices.prices[date][astock]
        except Exception as e:
            z.trace(e)
            print("problem etf date: {}".format( date))
#            print("astock: {}".format( astock))
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

def getLatestPrices(astock):
    try:
        getPrice.latest = z.getp("latestprices")
        if getPrice.latest and astock in getPrice.latest:
            return
    except:
        pass
#    z.getStocks.devoverride = None
    if getLatestPrices.done:
        return
    getLatestPrices.done = True

    stocks = z.getStocks(reset=True)
    print ("regenerating latest prices")
    getPrice.latest = dict()
    for astock in stocks:

        path = z.getPath("csv/{}.csv".format(astock))

        if not os.path.exists(path):
            print("astock: {}".format( astock))
            try:
                dask_help.historicalToCsv(astock)
            except Exception as e:
                continue

        if not os.path.exists(path):
            continue

        for row in csv.DictReader(open(path)):
            pass
        getPrice.latest[astock] = float(row['Close'])
    z.setp(getPrice.latest, "latestprices")
getLatestPrices.done = False            

def getPrice(astock, date = None, value = 1, orlatest = False):
    if not date:
        try:
            return getPrice.latest[astock]
        except:
            try:
                getLatestPrices(astock)
                return getPrice.latest[astock]
            except:
                pass
        return None

#    print("astock: {}".format( astock))
#    print("date: {}".format( date))
#    print ("how many prices {}".format(len(setSortedDict.prices[date])))
#    print ("how many prices {}".format(len(setSortedDict.prices[date][astock])))
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

def getDropScore(astock, percent = True):
    df = z.getCsv(astock)
    if df is None:
        return
    start = "2018-07-11"
    days = 64
    dates = df["Date"].tolist()
    starti = dates.index(start)
    minc = 10
    for idx in range(starti, len(dates)-days):
        close = df.at[idx + days,"Close"]
        opend = df.at[idx,"Open"]
        change = close/opend
        if change < minc:
            minc = change
    if percent:
        return z.percentage(minc)
    return round(minc,4)

#z.getStocks.devoverride = "ITOT"
#print (getPricedStocks("2017-01-11", 3))
#raise SystemExit
def getProbSale(astock):
#    for astock in z.getEtfList():
    path = z.getPath("csv/{}.csv".format(astock))
    count = 0
    downs = 0
    avgl = list()
    avgD = list()
    avgG = list()
    firstopen = None
    if not os.path.exists(path):
        dask_help.historicalToCsv(astock)

    if not os.path.exists(path):
        raise SystemExit

    for row in csv.DictReader(open(path)):
        opend = float(row['Open'])

        if not firstopen:
            firstopen = opend

        close = float(row['Close'])
        change = close/opend
        if change < 1:
            downs += 1
            avgD.append(change)
        else:
            avgG.append(change)
        count += 1
        avgl.append(change)

    if not avgl:
        return
    avgC = z.avg(avgl)
    avgD = z.avg(avgD)
    avgG = z.avg(avgG)
    probD = round(downs/count,2)
    return avgC, probD, avgD, avgG, z.percentage(close/firstopen)

def saveEtfPrices():
    saveEtfPrices.prices = defaultdict(dict)
    for astock in z.getEtfList() + ["SPY"]:
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
    print ("you can now use more_strat with setSortedDict")

def setDropRanking():
    label = ""
    if type(z.getStocks.devoverride) is str:
        label = z.getStocks.devoverride
    latestdrop = z.getp("{}latestdrop".format(label))

    setDropRanking.latestdropdic = dict()
    for i,item in enumerate(latestdrop):
        setDropRanking.latestdropdic[item[1]] = i
    z.setp(setDropRanking.latestdropdic, "{}latestdropdic".format(label))
setDropRanking.latestdropdic = None

def setVolumeRanking():
    label = ""
    if type(z.getStocks.devoverride) is str:
        label = z.getStocks.devoverride
    latestvolume = z.getp("{}latestvolume".format(label))

    setVolumeRanking.latestvolumedic = dict()
    for i,item in enumerate(latestvolume):
        setVolumeRanking.latestvolumedic[item[1]] = i
    z.setp(setVolumeRanking.latestvolumedic, "{}latestvolumedic".format(label))
setVolumeRanking.latestvolumedic = None

def poolQuery():
    z.getStocks.devoverride = "IUSG"
    setSortedDict(usepkl = True)
    modes = dask_help.getModes()
    dates = z.getp("dates")
#    dic = defaultdict(set)
    for mode in modes:
        print("\nmode : {}".format( mode ))
        cmode = set()
        for date in dates:
            try:
                stocks = getSortedStocks(date, mode, 
                    typed = "low", getall=True, reportprob=False)
            except:
                continue
            for astock in stocks:
                cmode.add(astock[1])
        print (len(cmode))
        


def getCol():
    #        stock   vol   $price  avgC   probD  avgD   drop  change live etfs
    return " {0:<5} {1:<4}  {2:>7} {3:>7} {4:<4} {5:>7} {6:>7} {7:>7} {8:>7} {9:>7} {10:3}"
def whatAboutThese(stocks, count = 40, lowprice = False, sell=False):
    print(getCol().format("stock", "vol", "price", "avgC", "probD", "avgD ", "avgG" ,"drop ", "change ", "live ", "etf"))

    sorts = SortedSet()
    sells = list()
    for i,value in enumerate(stocks):
        astock = value
        vrank = i+1
        try:
            if type(value) is tuple:
                astock = value[1]
                vrank = getVolumeRanking(astock)

            try:
                price = round(getPrice(astock),2)
            except:
                print("no astock: {}".format( astock))
                continue

            cprice = price
            try:
                avgC, probD, avgD, avgG, change = getProbSale(astock)
            except Exception as e:
#                print (z.trace(e))
                print("astock: {}".format( astock))
#                raise SystemExit
                continue
            try:
                dropScore = getDropScore(astock, percent=False)
                if not dropScore:
                    continue
            except Exception as e:
                continue

            live = "NA"
            try:
                live = util.getLiveChange(astock)
                if not live:
                    live = "NA"
                else:
                    cprice = live * price
            except Exception as e:
                pass

            if sell:
                basis = portfolio.getBasis(astock)
                if (cprice / basis) < .8:
                    sells.append(astock)

            value = getDisplaySortValue(probD,avgC,avgD,
                    live, price, dropScore, astock)

            etfc = util.getEtfQualifications(astock, count=True)

            msg = getCol().format(astock, vrank, price, 
                    z.percentage(avgC), 
                    probD, 
                    z.percentage(avgD),
                    z.percentage(avgG),
                    z.percentage(dropScore),
                    change,
                    z.percentage(live),
                    etfc)
            sorts.add((value,msg))

        except Exception as e:
            print (z.trace(e))
            raise SystemExit
            continue

    if sell:
        print("sells")
        print(sells)

    for astock in reversed(sorts):
        print(astock[1])

import math
def getDisplaySortValue(probD,avgC,avgD,live,price, dropScore, astock):
    if live == "NA":
        live = 1
    ret = round((((avgC**math.e + dropScore) / (live+avgD+probD))),2)
    return ret

def getDropRanking(astock = None):
    label = ""
    if type(z.getStocks.devoverride) is str:
        label = z.getStocks.devoverride

    if type(astock) is str: 
        try:
            return setDropRanking.latestdropdic[astock]
        except:
            setDropRanking.latestdropdic = z.getp("{}latestdropdic".format(label))
            try:
                return setDropRanking.latestdropdic[astock]
            except:
                setDropRanking()
            return setdropRanking.latestdropdic[astock]

    elif type(astock) is int:
        latestdrop = z.getp("{}latestdrop".format(label))
        whatAboutThese(latestdrop, count=astock)


def getVolumeRanking(astock = None):
    label = ""
    if type(z.getStocks.devoverride) is str:
        label = z.getStocks.devoverride

    if type(astock) is str: 
        try:
            return setVolumeRanking.latestvolumedic[astock]
        except:
            setVolumeRanking.latestvolumedic = z.getp("{}latestvolumedic".format(label))
            try:
                return setVolumeRanking.latestvolumedic[astock]
            except:
                setVolumeRanking()
            return setVolumeRanking.latestvolumedic[astock]

    elif type(astock) is int:
        latestvolume = z.getp("{}latestvolume".format(label))
        whatAboutThese(latestvolume, count=astock)

import os
def longlists(etf, date):
    z.getStocks.extras = (etf == "IUSG")
    stocks = z.getStocks(etf, reset=True)

    latestvolume = SortedSet()
    latestdrop = SortedSet()

    for astock in stocks:
        path = z.getPath("{}/{}.csv".format(dask_help.createRollingData.dir, astock))

        if not os.path.exists(path):
            print("problem with : {}".format( path ))
            continue

        for row in csv.DictReader(open(path)):

            cdate = row['Date']
            if cdate == date:

                try:
                    val = float(row['Volume'])
                except Exception as e:
                    z.trace(e)
                    print("astock : {}".format( astock ))
                    print("cdate : {}".format( cdate ))
                    continue

                latestvolume.add((val, astock))
                try:
                    latestdrop.add((getDropScore(astock, percent = False), astock))
                except:
                    continue

    print ("saved latestvolume")
    z.setp(latestvolume, "{}latestvolume".format(etf))
    z.setp(latestdrop, "{}latestdrop".format(etf))

def yesterday():
    return str(datetime.date.today() - datetime.timedelta(days=4))

def queryh(args):
    setSortedDict(usepkl = True)
    for mode in modes:
        print("\nmode : {}".format( mode ))
        stocks = getSortedStocks(args.date, mode, getall=True, typed="low")
        whatAboutThese(stocks)

def buyl(args):
    dask_help.convertToDask.directory = "csv"
    dask_help.createRollingData.dir = "csvCalculated"

    setSortedDict.final = "w_extra"
    if z.getStocks.devoverride == "IUSG":
        z.getStocks.extras = True
        z.getStocks.sells = True

    if args.main == 'gbuy':
        try:
            dask_help.historicalToCsv()
            setSortedDict(usepkl = False)
        except Exception as e:
            z.trace(e)
            exit()
    else:
        setSortedDict(usepkl = True)

    for mode in modes:
        print("\nmode : {}".format( mode ))
        stocks = getSortedStocks(args.date, mode, getall=True, typed="low")
        whatAboutThese(stocks)

def etfsf(args):
    etfs = z.getEtfList()
    try:
        if sys.argv[2]:
            etfs = [sys.argv[2].upper()]
    except:
        pass

    for etf in etfs:
        print("etf : {}".format( etf ))
        z.getStocks.devoverride = etf
        setSortedDict(etf=etf, usepkl = False)

def longlists(args):
    try:
        for etf in z.getEtfList():
            print("etf : {}".format( etf ))
            z.getStocks.devoverride = etf
            longlists(etf, yesterday())
            setVolumeRanking()
    except Exception as e:
        z.trace(e)
        print (colored("Maybe run dask_help.py history", "green"))


import portfolio
def generateSellPrice():
    stocks = portfolio.getPortfolio(aslist=True)
    sell_list = z.getp("sell_list")
#    for astock in stocks:


def sells(args):
    z.getStocks.sells = True
    stocks = portfolio.getPortfolio(aslist = True)
    whatAboutThese(stocks, sell=True)

if __name__ == '__main__':
    import argparse
    import sys
    import zprep
    from termcolor import colored

#    poolQuery()
#    raise SystemExit
    parser = argparse.ArgumentParser()
    parser.add_argument('main' , nargs='?', default="buy")
    parser.add_argument('--mode', default="all")
    parser.add_argument('--etf', default="IUSG")
    parser.add_argument('--date', default=yesterday())
    parser.add_argument('--live', default=True, action="store_false")
    args = parser.parse_args()

    if args.main[0] == "l":
        args = z.getp("lastArgs_forGenerate_list")
    else:
        z.setp(args, "lastArgs_forGenerate_list")

    z.offline.off = args.live

    z.getStocks.devoverride = args.etf.upper()

    modes = dask_help.getModes()
    if args.mode != "all":
        modes = [args.mode]

    z.getStocks.extras = z.getStocks.devoverride == "IUSG"
 
    print("date : {}".format( args.date ))

    dask_help.convertToDask.directory = "csv"
    try:
        if args.main:
            # show drop ranking
            if args.main == "dropranking":
                setDropRanking()
                latestdrop = z.getp("{}latestdrop".format(z.getStocks.devoverride))
                print(latestdrop[-10:])
                print(latestdrop[:10])

            if args.main == "volumeranking":
                latestvolume = z.getp("{}latestvolume".format(z.getStocks.devoverride))
                print(latestvolume[-10:])
                print(latestvolume[:10])

            # what to buy tomorrow
            if args.main == "query":
                queryh(args)

            # generate buy list which is ISUG + EXTRAS
            if args.main == "buy" or args.main == 'gbuy':
                print ("asdfA")
                buyl(args)

            # generate buy list which is ISUG + EXTRAS
            if args.main == "sell":
                sells(args)

            # generated setSortedDict
            if args.main == "etfs":
                etfsf(args)

            if args.main == "longlists":
                longlists(args)

    except Exception as e:
        z.trace(e)
        pass
