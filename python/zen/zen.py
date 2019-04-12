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

def getPrice(astock, date = None, value = 1, orlatest = False):
    if not date:
        try:
            return getPrice.latest[astock]
        except:
            try:
                getLatestPrices(astock)
                return getPrice.latest[astock]
            except:
                path = z.getPath("historical/{}.csv".format(astock))
                for row in csv.DictReader(open(path)):
                    closep = float(row['Close'])
                return closep
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

    savedname = "{}sorteddict{}".format(prefix, final)
    z.setp(setSortedDict.sorteddict, savedname)
    z.setp(setSortedDict.prices, "{}prices{}".format(prefix, final))
    print("done saving {}".format(savedname))
setSortedDict.final = ""
setSortedDict.sorteddict = None
setSortedDict.prices = defaultdict(dict)

def getSortedStocks(date, mode, howmany = 2, getall = False, typed=None, reportprob = True):
#    stocks = z.getStocks()
#    return sample(stocks, howmany)

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
            return None
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

def getLatestPrices(astock, force=False):
    try:
        getPrice.latest = z.getp("latestprices")
        if getPrice.latest and astock in getPrice.latest:
            return
    except:
        pass

    if not force:
        return

#    z.getStocks.devoverride = None
    if getLatestPrices.done:
        return

    getLatestPrices.done = True
    regenerateLatestPrices()
getLatestPrices.done = False            

def regenerateLatestPrices():
    stocks = z.getStocks(reset=True)
    print ("regenerating latest prices")
    getPrice.latest = dict()
    for astock in stocks:
        path = z.getPath("csv/{}.csv".format(astock))
        if not os.path.exists(path):
            continue
        for row in csv.DictReader(open(path)):
            pass
        getPrice.latest[astock] = float(row['Close'])
    z.setp(getPrice.latest, "latestprices")

downs = 0
total = list()
bought = list()
order = list()
def getBounceProb(astock, startd = "2016-07-11"):
    global downs, total
    df = z.getCsv(astock)
    if df is None:
        return
    try:
        dates = df["Date"].tolist()
        starti = dates.index(startd)
    except:
        return

    for idx in range(starti, len(dates)-2):
        opend = df.at[idx,"Open"]
        close = df.at[idx,"Close"]
        change = close/opend
        if change < 0.90:
#            opend = df.at[idx,"Close"]
            bought.append(close)
            order.append(astock)

            close2 = df.at[idx+1,"Close"]
            change = close2/close
            if change < 1.0:
                downs += 1
            total.append(round(change,4))

def getDropScore(astock, startd = "2018-07-11", days = 64):
    df = z.getCsv(astock)
    if df is None:
        return
    dates = df["Date"].tolist()
    starti = dates.index(startd)
    minc = 10
    for idx in range(starti, len(dates)-days):
        close = df.at[idx + days,"Close"]
        opend = df.at[idx,"Open"]
        change = close/opend
        if change < minc:
            minc = change
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
        if change < 1.000:
            downs += 1
            avgD.append(change)
        else:
            avgG.append(change)
        count += 1
        avgl.append(change)

    if not avgl:
        return
    avgC = z.avg(avgl, p=5)
    avgD = z.avg(avgD)
    avgG = z.avg(avgG)
    probD = round(downs/count,2)
    return avgC, probD, avgD, avgG, round(close/firstopen,3)

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
    #        stock  $price avgC  probD   avgD   avgG   drop   change live   etfs  recov
    return " {0:<5} {1:>7} {2:>7} {3:<4} {4:>7} {5:>7} {6:>7} {7:>7} {8:>7} {9:>7} {10:>3} {11:<5}"

def whatAboutThese(stocks, count = 40, lowprice = False, sell=False):
    print(getCol().format("stock", "price", "avgC", "probD", "avgD ", "avgG " ,"d1 ", "d2 ", "change ", "live ", "etf ", "recov"))

    sorts = SortedSet()
    sells = list()
    if not stocks:
        return
    noprices = list()
    for i,value in enumerate(stocks):

        astock = value
        try:
            if type(value) is tuple:
                astock = value[1]
            try:
                price = round(getPrice(astock),2)
            except:
                noprices.append(astock)
                continue

            cprice = price
            try:
                avgC, probD, avgD, avgG, change = getProbSale(astock)
            except Exception as e:
#                print (z.trace(e))
#                print("astock: {}".format( astock))
#                raise SystemExit
                continue
            try:
                d1 = getDropScore(astock, "2018-01-12", 43)
                d2 = getDropScore(astock)
                if not d2:
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
                    live, price, d2, astock, change)

            recov = "NA"
            if d2 > 1.00:
                recov = "WOW"
            elif avgC > 1.00:
                recov = round(d2/(avgC-1.0),2)

            etfc = util.getEtfQualifications(astock, count=True)
            try:
                msg = getCol().format(astock, price, 
                    z.percentage(avgC, accurate=True), 
                    probD, 
                    z.percentage(avgD),
                    z.percentage(avgG),
                    z.percentage(d1),
                    z.percentage(d2),
                    z.percentage(change),
                    z.percentage(live),
                    etfc, 
                    recov)
            except:
                continue
            sorts.add((value,msg))

        except Exception as e:
            print (z.trace(e))
            raise SystemExit
            continue

    for astock in reversed(sorts):
        print(astock[1])

    if noprices:
        print("noprices: {}".format( noprices))
    if sell:
        print("sells")
        print(sells)


import math
def getDisplaySortValue(probD,avgC,avgD,live,price, dropScore, astock, change):
    if live == "NA":
        live = 1
    ret = round((((avgC**math.e + dropScore + (change/3)) / (live+avgD+probD))),2)
    return ret

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
            try:
                return setVolumeRanking.latestvolumedic[astock]
            except:
#                print("no volume data for astock: {}".format( astock))
                pass
    elif type(astock) is int:
        latestvolume = z.getp("{}latestvolume".format(label))
        whatAboutThese(latestvolume, count=astock)

cats = ["Price", "AvgC", "ProbD", "Drop", "Volume", "Change", "C50"]
import os
def longlists(etf, date):
    print ("long lists")
    z.getStocks.devoverride = etf
    z.getStocks.extras = (etf == "IUSG")

    stocks = z.getStocks(etf, reset=True)
    cdics = defaultdict(SortedSet)
    print("stocks: {}".format( len(stocks)))

    for astock in stocks:
        path = z.getPath("{}/{}.csv".format(dask_help.createRollingData.dir, astock))

        if not os.path.exists(path):
            print("problem with : {}".format( path ))
            continue

        for row in csv.DictReader(open(path)):
            pass
        try:
            cdics["C30"].add(( float(row['C30']) , astock))
            cdics["Volume"].add(( float(row['Volume']) , astock))
            cdics["Price"].add(( float(row['Close']) , astock))
            cdics["Drop"].add((getDropScore(astock), astock))
            avgC, probD, avgD, avgG, change = getProbSale(astock)
            cdics["AvgC"].add((avgC, astock))
            cdics["ProbD"].add((probD, astock))
            cdics["Change"].add((change, astock))

        except Exception as e:
#            cdate = row['Date']
#            z.trace(e)
#            print("astock : {}".format( astock ))
#            print("cdate : {}".format( cdate ))
            continue

    print ("written {}cdics".format(etf))
    z.setp(cdics, "{}cdics".format(etf))

def yesterday():
    return str(datetime.date.today() - datetime.timedelta(days=3))

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
        import update_history
        try:
            z.getStocks.devoverride = "ITOT"
            if update_history.update():
                dask_help.historicalToCsv()
                setSortedDict(usepkl = False)
                regenerateLatestPrices()

                z.getStocks.devoverride = "IUSG"
                setSortedDict(usepkl = False)
            else:
                z.getStocks.devoverride = args.etf.upper()
                setSortedDict(usepkl = True)

        except Exception as e:
            z.trace(e)
            exit()
    else:
        setSortedDict(usepkl = True)

    z.getStocks.devoverride = args.etf.upper()
    for mode in modes:
        print("\nmode : {}".format( mode ))
        stocks = getSortedStocks(args.date, mode, getall=True, typed="low")
        whatAboutThese(stocks)

def etfsf(args):
    for etf in [ z.getStocks.devoverride ]:
        print("etf : {}".format( etf ))
        z.getStocks.devoverride = etf
        setSortedDict(etf=etf, usepkl = False)

import portfolio
def generateSellPrice():
    stocks = portfolio.getPortfolio(aslist=True)
    sell_list = z.getp("sell_list")
#    for astock in stocks:


def sells(args):
    z.getStocks.sells = True
    stocks = portfolio.getPortfolio(aslist = True)
    whatAboutThese(stocks, sell=True)

def getEtfScore(cuttoff):
    etfd = defaultdict(list)
    for i in range(5,50,3):
        etfq(i, etfd, cuttoff)

    average = list()
    for i,vals in etfd.items():
        avg = z.avg(vals)
        average.append(avg)

    if not average:
        print ("problem with number : {}".format(cuttoff))
        return None

    return z.avg(average)


def getEtfScore2():
    z.getStocks.devoverride = "ITOT"
    stocks = z.getStocks("ITOT", reset=True)
    sorts = SortedSet()
    for astock in stocks:
        try:
            latest = getPrice(astock)
            if not latest:
                continue
        except:
            continue
        sorts.add((latest, astock))

    currentlist = list()
    tally = dict()
    idx = 0
    for apair in sorts:
        currentlist.append(apair)
        if len(currentlist) >= 50:
            tally[idx] = scoreList(currentlist)
            currentlist = list()
            idx += 1
#    print("tally: {}".format( tally))
    import matplotlib.pyplot as plt
    for key, value in tally.items():
        plt.scatter(key, value)
        print("key: {}".format( key))
    plt.show()

def scoreList(currentlist):
    dates = z.getp("dates")
    ret = list()
    for i in range(5,50,3):
        for item in currentlist:
            start = dates[-1 * i]
            latest = item[0]
            startp = getPrice(item[1], start)
            if not startp:
                continue
            change = round(latest/startp,4)
            ret.append(change)
    return z.avg(ret)

def etfq(idx, etfd, cuttoff = 40):
    dates = z.getp("dates")
    start = dates[-1 * idx]
    etfchange = defaultdict(list)
    etfups = defaultdict(int)
    etfcount = defaultdict(int)
    for etf in ["ITOT"]:
        z.getStocks.devoverride = etf
        stocks = z.getStocks(etf, reset=True)
        for astock in stocks:
            try:
                latest = getPrice(astock)
                if not latest:
                    continue

                if latest <= float(cuttoff):
                    continue
                startp = getPrice(astock, start)

                if not startp:
                    continue

                change = round(latest/startp,4)
            except Exception as e:
                z.trace(e)
                print("astock : {}".format( astock ))
                continue

            if change >= 1.0000:
                etfups[etf] += 1
            etfchange[etf].append(change)
            etfcount[etf] += 1

    for etf, vals in etfchange.items():
        up = etfups[etf]
        upc = etfcount[etf]
        avg = z.avg(vals)
        change = round(up/upc, 3)
        tallied = round(avg * change,3)
        etfd[etf].append(tallied)

        if etfq.doonce:
            etfq.doonce = False
            print("etf: {}".format( etf))
            print("upc : {}".format( upc ))


#    print("number : {}".format( number ))
def dropInvestigation():
    stocks = z.getStocks("IUSG")
    print("stocks : {}".format( len(stocks)))
    for astock in stocks:
        getBounceProb(astock, startd = "2017-07-11")
    print(z.avg(total))
    print(len(total))
    print("total: {}".format( downs))
    avgl=list()
    for i,astock in enumerate(order):
        print("astock : {}".format( astock ))
        cprice = getPrice(astock)
        change = cprice/ bought[i] 
        print("change : {}".format( z.percentage(change)))
        avgl.append(change)
    print (z.avg(avgl))

if __name__ == '__main__':
    import argparse
    import sys
    import zprep
    from termcolor import colored

#    poolQuery()
    parser = argparse.ArgumentParser()
    parser.add_argument('main' , nargs='?', default="buy")
    parser.add_argument('--mode', default="default")
    parser.add_argument('--etf', default="IUSG")
    parser.add_argument('--date', default=yesterday())
    parser.add_argument('--live', default=False, action="store_true")
    parser.add_argument('--cat', default="default")
    parser.add_argument('--catcount', default=7)
    args = parser.parse_args()

#    if args.main[0] == "l":
#        args = z.getp("lastArgs_forGenerate_list")
#    else:
#        z.setp(args, "lastArgs_forGenerate_list")

    z.online.online = args.live

    z.getStocks.devoverride = args.etf.upper()

    catl = cats
    if args.cat != "default":
        catl = [args.cat]
    modes = dask_help.getModes()
    if args.mode != "default":
        modes = [args.mode]

    z.getStocks.extras = z.getStocks.devoverride == "IUSG"
 
    print("date : {}".format( args.date ))
    args.catcount = int(args.catcount)

    dask_help.convertToDask.directory = "csv"
    try:
        if args.main:
            if args.main == "ranking":
                name = "{}cdics".format(z.getStocks.devoverride)
                print (name)
                lists = z.getp(name)
                for cat in catl:
                    print ("{} High".format(cat))
                    whatAboutThese(lists[cat][-1 * args.catcount:])
                    print ("{} Low".format(cat))
                    whatAboutThese(lists[cat][:args.catcount])

            # what to buy tomorrow
            if args.main == "query":
                queryh(args)

            # generate buy list which is ISUG + EXTRAS
            if args.main == "buy" or args.main == 'gbuy':
                if args.mode == "default":
                    modes = ["C30", "Volume"]
                buyl(args)
                print ("etfs")
                whatAboutThese(z.getEtfList(forEtfs=True))

            # generate buy list which is ISUG + EXTRAS
            if args.main == "sell":
                sells(args)

            # generated setSortedDict
            if args.main == "etfs":
                if args.mode == "default":
                    modes = ["Volume"]
                    etfsf(args)
                    modes = ["C30"]
                    etfsf(args)
                else:
                    etfsf(args)

            if args.main == "ll":
                longlists("IUSG", args.date)
#                longlists("ITOT", args.date)

            if args.main == "drops":
                import itot_buy
                itot_buy.sortedDropPrice()

            if args.main == "etfq":
                import matplotlib.pyplot as plt
                ys = range(1, 462, 10)
                xs = list()
                for cutt in ys:
                    print("cutt : {}".format( cutt ))
                    etfq.doonce = True
                    xs.append(getEtfScore(cutt))
                plt.scatter(ys, xs)
                plt.show()

            if args.main == "etfq2":
                import matplotlib.pyplot as plt
                getEtfScore2()

                        
    except Exception as e:
        z.trace(e)
        pass
