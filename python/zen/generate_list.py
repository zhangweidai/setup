import z 
import operator
from random import sample
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

def getSortedStocks(date, mode, howmany = 2, getall = False, typed=None):
    if not typed:
        typed = getSortedStocks.get
    try:
        alist = setSortedDict.sorteddict[mode][date]
    except Exception as e:
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
    stocks = z.getStocks(reset=True)
    print ("regenerating latest prices")
    getPrice.latest = dict()
    for astock in stocks:
        path = z.getPath("historical/{}.csv".format(astock))
        for row in csv.DictReader(open(path)):
            pass
        getPrice.latest[astock] = float(row['Close'])
    z.setp(getPrice.latest, "latestprices")

def getPrice(astock, date = None, value = 1, orlatest = False):
    if not date:
        try:
            return getPrice.latest[astock]
        except:
            getLatestPrices(astock)
            return getPrice.latest[astock]
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

def whatAboutThese(stocks, count = 40, lowprice = False):
    print(" {0:<6} {1:<4} $ {2:<7} {3:<7} {4:<7} {5:<7} {6:<5} {7:<5}".format(\
                "stock", "vol", "price", "avgC", "probD", "avgD", "drop", "live"))
    for i,value in enumerate(stocks):
        astock = value
        vrank = i+1
        try:
            if type(value) is tuple:
                astock = value[1]
                vrank = getVolumeRanking(astock)

            price = round(getPrice(astock),2)
            if lowprice and price > 50:
                continue
            try:
                avgC, probD, avgD = getProbSale(astock)
            except Exception as e:
                print (z.trace(e))
                print("astock: {}".format( astock))
                raise SystemExit
                continue

            try:
                dropScore = getDropScore(astock)
                if not dropScore:
                    continue
            except Exception as e:
                continue

            live = "NA"
            try:
                live = util.getLiveChange(astock)
            except Exception as e:
                pass

            print(" {0:<6} {1:<4} $ {2:<7} {3:<7} {4:<7} {5:<7} {6:<5} {7:<5}".format(astock, \
                                   vrank, price, avgC, probD, avgD, dropScore, live))

            if i > count:
                break

        except Exception as e:
            print (z.trace(e))
            raise SystemExit
            continue

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
            print ("getting volumedic for {}".format(label))
            setVolumeRanking.latestvolumedic = z.getp("{}latestvolumedic".format(label))
            try:
                return setVolumeRanking.latestvolumedic[astock]
            except:
                setVolumeRanking()
            return setVolumeRanking.latestvolumedic[astock]

    elif type(astock) is int:
        latestvolume = z.getp("{}latestvolume".format(label))
        whatAboutThese(latestvolume, count=astock)


def longlists(etf, date):
    z.getStocks.extras = (etf == "IUSG")
    stocks = z.getStocks(etf, reset=True)

    latestvolume = SortedSet()
    latestdrop = SortedSet()

    for astock in stocks:
        path = z.getPath("{}/{}.csv".format(dask_help.createRollingData.dir, astock))
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
    return str(datetime.date.today() - datetime.timedelta(days=3))

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('main')
    parser.add_argument('--mode', default="all")
    parser.add_argument('--etf', default="IUSG")
    parser.add_argument('--date', default=yesterday())
    args = parser.parse_args()

    z.getStocks.devoverride = args.etf.upper()

    modes = dask_help.getModes()
    if args.mode != "all":
        modes = [args.mode]

    z.getStocks.extras = z.getStocks.devoverride == "IUSG"
 
    print("date : {}".format( args.date ))

    import util
    dask_help.convertToDask.directory = "csv"
    import zprep
    try:
        if len(sys.argv) > 1:
            # show drop ranking
            if sys.argv[1] == "dropranking":
                setDropRanking()
                latestdrop = z.getp("{}latestdrop".format(z.getStocks.devoverride))
                print(latestdrop[-10:])
                print(latestdrop[:10])

            if sys.argv[1] == "volumeranking":
                latestvolume = z.getp("{}latestvolume".format(z.getStocks.devoverride))
                print(latestvolume[-10:])
                print(latestvolume[:10])

            # what to buy tomorrow
            if sys.argv[1] == "query":
                setSortedDict(usepkl = True)

                for mode in modes:
                    print("\nmode : {}".format( mode ))
                    stocks = getSortedStocks(args.date, mode, getall=True)
                    whatAboutThese(stocks)

            # generate buy list which is ISUG + EXTRAS
            if sys.argv[1] == "buy" or sys.argv[1] == 'gbuy':
                dask_help.convertToDask.directory = "csv"
                dask_help.createRollingData.dir = "csvCalculated"

                setSortedDict.final = "w_extra"
                if z.getStocks.devoverride == "IUSG":
                    z.getStocks.extras = True

                if sys.argv[1] == 'gbuy':
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


            # generated setSortedDict
            if sys.argv[1] == "etfs":
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

            if sys.argv[1] == "longlists":
                for etf in z.getEtfList():
                    print("etf : {}".format( etf ))
                    z.getStocks.devoverride = etf
                    longlists(etf, yesterday())
                    setVolumeRanking()


    except Exception as e:
        z.trace(e)
        pass
