from random import sample, randint
from collections import defaultdict
from sortedcontainers import SortedSet
import csv
import dask_help
import math
import statistics
import os
import threadprep
import portfolio
import util
import z 

keeping = 40
discardlocation = int(keeping/2)

def getPrice(astock, date = None, openp=False):
    try:
        if not date:
            if not getPrice.latest:
                getPrice.latest = z.getp("latestprices")
            idx = 1 if openp else 0
            return getPrice.latest[astock][idx]
            
            if not getPrice.today:
                dates = z.getp("dates")
                getPrice.today = dates[-1]
            date = getPrice.today
        try:
            return getPrice.pdict[astock][date]
        except:
            try:
                getPrice.pdict = z.getp("{}_P".format(loadSortedEtf.etf))
                return getPrice.pdict[astock][date]
            except:
                getPrice.pdict = z.getp("ITOT_P2")
                return getPrice.pdict[astock][date]
    except Exception as e:
#        z.trace(e)
#        print("astock: {}".format( astock))
#        print("date : {}".format( date ))
#        print (loadSortedEtf.etf)
#        raise SystemExit

        path = z.getPath("historical/{}.csv".format(astock))
        for row in csv.DictReader(open(path)):
            closep = float(row['Close'])
        return closep

getPrice.today = None
getPrice.pdict = None
getPrice.latest = dict()


def loadSortedEtf(etf = None):
    if etf:
        loadSortedEtf.etf = etf
    loaded = "{}_SS".format(loadSortedEtf.etf)
    print("loaded : {}".format( loaded ))
    getSortedStocks.cdict = z.getp(loaded)
loadSortedEtf.etf = "IUSG"

def getSortedStocks(date, mode, typed="low", get=10, reportprob = True):
    if mode == "r":
        try:
            return sample(getSortedStocks.ydict[date], get)
        except:
            try:
                getSortedStocks.ydict = z.getp("{}_Y".format(loadSortedEtf.etf))
                return sample(getSortedStocks.ydict[date], get)
            except Exception as e:
                print ("problem {} ".format(e))
                print("mode: {}".format( loadSortedEtf.etf))
                print("mode: {}".format( mode))
                print("len: {}".format( getSortedStocks.ydict))
                print("len: {}".format( getSortedStocks.ydict.keys()))
                print("date: {}".format( date))
                raise SystemExit

    try:
        alist = getSortedStocks.cdict[mode][date]
#        print("alist : {}".format( alist ))
#        print("date: {}".format( date))
#        print("huhmode: {}".format( mode))
    except:
        try:
            loadSortedEtf()
            alist = getSortedStocks.cdict[mode][date]
        except Exception as e:
            if reportprob:
                print("dates: {}".format(len(getSortedStocks.cdict[mode])))
                print("date: {}".format( date))
                print("mode: {}".format( mode))
                z.trace(e)
                return None

    ret = None
    if typed == "both":
        ret = sample(alist,get)
    elif typed == "high":
        if get == "all":
            ret = alist[-1*discardlocation:]
        else:
            ret = sample(alist[-1*discardlocation:], get)
    elif typed == "low":
        if get == "all":
            ret = alist[:discardlocation]
        else:
            ret = sample(alist[:discardlocation], get)
    return ret

getSortedStocks.highlight_score = None
getSortedStocks.get = "both"
getSortedStocks.cdict = None
getSortedStocks.ydict = None

def getPricedStocks(idxdate, price):
    stocks = z.getStocks()
    minprice = price * 10
    maxprice = (price+1) * 10
    ret = list()
    for astock in stocks:
        try:
            cprice = getPrice(astock, idxdate)
        except:
            pass

        if not cprice or randint(3, 6) != 5:
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

    if getLatestPrices.done:
        return

    getLatestPrices.done = True
    regenerateLatestPrices()
getLatestPrices.done = False            

def regenerateLatestPrices():
#    print ("regenerating latest prices")
    getPrice.latest = dict()
    path = z.getPath("historical")
    listOfFiles = os.listdir(path)
    for entry in listOfFiles:  
        cpath = "{}/{}".format(path, entry)
        for row in csv.DictReader(open(cpath)):
            pass
        astock = os.path.splitext(entry)[0]
        getPrice.latest[astock] = (float(row['Close']), float(row['Open']))

    print (len(z.getStocks("ITOT", reset=True)))
    print (len(getPrice.latest))

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
        print("astock: {}".format( astock))
        return "NA"
    dates = df["Date"].tolist()

    try:
        starti = dates.index(startd)
    except:
        starti = 0

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
def getProbSale(astock, dated):
#    for astock in z.getEtfList():
#    path = z.getPath("csv/{}.csv".format(astock))
    findate = None
    startdate = None
    startidx = None

    path = z.getPath("historical/{}.csv".format(astock))
    dates = z.getp("dates")
    startidx = dates.index(dated)-51
    finidx = dates.index(dated)

    count = 0
    downs = 0
    avgl = list()
    avgD = list()
    avgG = list()
    firstopen = None

    if not os.path.exists(path):
        raise SystemExit

    for row in csv.DictReader(open(path)):
        if dated:
            dates = z.getp("dates")
            cdate = row['Date']
            cidx = dates.index(cdate)
            if cidx < startidx or cidx > finidx:
                continue
#            print("dated: {}".format( dated))
#            print("cdate: {}".format( cdate))
#            print("cidx : {}".format( cidx ))
#            print("startidx : {}".format( startidx ))
#            print("finidx: {}".format( finidx))


        opend = float(row['Open'])

        if not firstopen:
            firstopen = opend
#            print("firstopen : {}".format( firstopen ))
#            print("astock: {}".format( astock))

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
        print ("no avgl")
        print("path: {}".format( path))
        return

    avgC = z.avg(avgl, p=5)
    avgD = z.avg(avgD)

    avgG = z.avg(avgG)
    probD = round(downs/count,2)

    live = util.getLiveData(astock, key = "price")

    change = None
    if live:
        change = round(live/firstopen,3)
    else:
        change = round(close/firstopen,3)

    return avgC, probD, avgD, avgG, change, statistics.median(avgl)


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
                stocks = getSortedStocks(date, mode, reportprob=False)
            except:
                continue
            for astock in stocks:
                cmode.add(astock[1])
        print (len(cmode))
        


def getCol():
    #        stock  $price avgC   median probD   avgD  avgG   d0     d1     d2     change  live   letfs   recov   mcchg   score
    return " {0:<5} {1:>7} {2:>7} {3:>6} {4:>4} {5:>7} {6:>7} {7:>8} {8:>8} {9:>8} {10:>7} {11:>7} {12:>3} {13:>7} {14:>7} {15:<5}"

def whatAboutThese(stocks, count = 40, lowprice = False, sell=False, ht=None, dated = None):
    print(getCol().format("stock", "price", "avgC", "median", "probD", "avgD ", "avgG ", "d0" ,"d1 ", "d2 ", "change ", "live ", "etf ", "recov  ", "oschg  ", "mcchg  ", "dscore   "))

    sorts = SortedSet()
    sells = list()
    if not stocks:
        return

    noprices = list()
    avgChanges = list()
    avgchanget = list()
    highdscore = 0
    for i,value in enumerate(stocks):

        astock = value
        try:
            if type(value) is tuple:
                astock = value[1]

            price = 0
            if dated:
                price = round(getPrice(astock, dated),3)
            else:
                try:
                    price = round(getPrice(astock),3)
                except:
                    noprices.append(astock)
                    continue

            cprice = price
            try:
                avgC, probD, avgD, avgG, change, median = getProbSale(astock, dated)
            except Exception as e:
                z.trace(e)
                print("problem with astock: {}".format( astock))
#                raise SystemExit
                continue

            try:
                oschg, mcchg = getChangeStats(astock)
            except:
                pass

            try:
                d0 = getDropScore(astock, "2013-03-19", 30)
            except Exception as e:
                print("e: {}".format( e))
                d0 = "NA"

            try:
                d1 = getDropScore(astock, "2017-05-25", 45)
            except Exception as e:
                d1 = "NA"

            try:
                d2 = getDropScore(astock)
            except Exception as e:
                print("problem with astock: {}".format( astock))
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

            try:
                avgds = z.avg([d0,d1,d2])
            except:
                try:
                    avgds = z.avg([d1,d2])
                except:
                    avgds = d2

            try:
                dscore = getDisplaySortValue(probD,avgC, avgD, live, avgds, astock, change)
            except:
                print("live: {}".format( live))
                print("avgds: {}".format( avgds))
                print("avgD: {}".format( avgD))
                print("avgC: {}".format( avgC))
                print("probD: {}".format( probD))

            if dscore > highdscore:
                highdscore = dscore

            ddscore = dscore
            if getSortedStocks.highlight_score and dscore >= getSortedStocks.highlight_score:
                ddscore = colored(ddscore, "green")  

            if ht and dscore < float(ht):
                continue

            recov = "NA"
            if d2 > 1.00:
                recov = "WOW"
            elif avgC > 1.00:
                recov = round(d2/(avgC-1.0),1)

            avgChanges.append(avgC)
            avgchanget.append(change)

            if mcchg:
                mcchg = z.percentage(mcchg)
            else:
                mcchg = "NA"
#            if not oschg:
#                oschg = "NA"

            etfc = util.getEtfQualifications(astock, count=True)
            try:
                msg = getCol().format(astock, price, 
                    z.percentage(avgC, accurate=True), 
                    z.percentage(median),
                    probD, 
                    z.percentage(avgD),
                    z.percentage(avgG),
                    z.percentage(d0),
                    z.percentage(d1),
                    z.percentage(d2),
                    z.percentage(change),
                    z.percentage(live),
                    etfc, 
                    recov,
                    mcchg,
                    ddscore)
            except:
                continue
            sorts.add((dscore,msg))

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

    if avgChanges:
        total = z.avgp(avgchanget)
        print ("Average 52 day change {} - Total change {}".format(
                    z.avgp(avgChanges), total))

    return highdscore

def getDisplaySortValue(probD,avgC,avgD,live, dropScore, astock, change):
    if live == "NA":
        live = 1
    ret = round((((avgC**math.e + dropScore + (change/3)) / (live+avgD+probD))),2)
    return ret

cats = ["Price", "AvgC", "ProbD", "Drop", "Volume", "Change", "C50"]
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

def today(idx = 1):
    dates = z.getp("dates")
    return dates[-1 * idx]

def buyl(args, dated):
    if args.main == 'gbuy':
        import update_history
        try:
            if update_history.update():
                threadprep.doit_2()
                regenerateLatestPrices()
                exit()

        except Exception as e:
            z.trace(e)
            exit()

    print ("\netfs")
    dscore = whatAboutThese(z.getEtfList(forEtfs=True), dated=dated)
    getSortedStocks.highlight_score = dscore
    usedate = dated or args.date
    scores = z.getp("modeScores")
    for mode in modes:

        modestr = "{}/low".format(mode)
        msg = "\nmode : {}\ttyped: {}   {}   {}".format( mode, "low", scores[modestr][0], scores[modestr][1])
        if modestr in goodmodes:
            msg = colored(msg,"green")
        if modestr not in skips:
            print(msg)
            stocks = getSortedStocks(usedate, mode, get="all", typed="low")
            if args.save == modestr:
                z.setp(stocks, "saved")
            whatAboutThese(stocks, ht=args.ht, dated=dated)

        modestr = "{}/high".format(mode)
        msg = "\nmode : {}\ttyped: {}   {}   {}".format( mode, "high", scores[modestr][0], scores[modestr][1])
        if modestr in goodmodes:
            msg = colored(msg,"green")
        if modestr not in skips:
            print(msg)
            stocks = getSortedStocks(usedate, mode, get="all", typed="high")
            if args.save == modestr:
                z.setp(stocks, "saved")
            whatAboutThese(stocks, ht=args.ht, dated=dated)
goodmodes = ["Volume/low", "Price/low", "Var50/high", "Drops/high"]
skips = ["Price/high", "Var50/low", "Drops/low", "Volume/high"]

def buyl2():
    sets = z.getp("mcsets")
    print("\nmode : {}\ttyped: {}".format( "marketcap", "high"))
    whatAboutThese(sets[-7:])
    print("\nmode : {}\ttyped: {}".format( "marketcap", "low"))
    whatAboutThese(sets[:7])

    sets = z.getp("ossets")
    print("\nmode : {}\ttyped: {}".format( "shares", "high"))
    whatAboutThese(sets[-7:])
    print("\nmode : {}\ttyped: {}".format( "shares", "low"))
    whatAboutThese(sets[:7])


def generateSellPrice():
    stocks = portfolio.getPortfolio(aslist=True)
    sell_list = z.getp("sell_list")
#    for astock in stocks:


def sells(args):
    z.getStocks.sells = True
    stocks = portfolio.getPortfolio(aslist = True)
    whatAboutThese(stocks, sell=True, dated=args.date)
    print("stocks : {}".format( len(stocks)))

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

def getOuts():
    path = z.getPath("pkl")
    listOfFiles = os.listdir(path)
    cfiles = SortedSet()
    for entry in listOfFiles:  
        if "_outstanding.pkl" not in entry:
            continue
        fullpath = "{}/{}".format(path, entry)
        cfiles.add(fullpath)
    return cfiles

def diffOuts():
    outs = getOuts()
    out1 = outs[-1]
    print("out1 : {}".format( out1 ))
    out2 = outs[-2]
    print("out2 : {}".format( out2 ))
    out1dic = z.getp(out1)
    out2dic = z.getp(out2)
    ossets = SortedSet()
    mcsets = SortedSet()
    mcdiff = dict()
    for astock, values in out1dic.items():
        changes = round( out2dic[astock][0]/ values[0] ,6)
        changem = round( out2dic[astock][2]/ values[2] ,6)
        mcdiff[astock] = (changes,changem)
        mcsets.add((changem,astock))
        ossets.add((changes,astock))
#    print(ossets[-10:])
#    print(ossets[:10])
#    print(mcsets[-10:])
#    print(mcsets[:10])
    z.setp(mcdiff, "mcdiff")
    z.setp(mcsets, "mcsets")
    z.setp(ossets, "ossets")


def getChangeStats(astock, idx=1):
    try:
        return getChangeStats.outdic[astock]
    except:
        try:
            getChangeStats.outdic = z.getp("mcdiff")
            return getChangeStats.outdic[astock]
        except:
            pass
    return None, None


def getStats(astock, idx=1):
    try:
        return getStats.outdic[idx][astock]
    except:
        try:
            outs = getOuts()
            outf = outs[-1*idx]
            getStats.outdic[idx] = z.getp(outf)
            return getStats.outdic[idx][astock]
        except:
            pass
    return 0,0
getStats.outdic = dict()

def getLastDate():
    path = z.getPath("historical/IVV.csv")
    for row in csv.DictReader(open(path)):
        date = row['Date']
    return date

if __name__ == '__main__':
    import argparse
    import sys
    import zprep
    from termcolor import colored

#    diffOuts()
#    mcchg = getChangeStats("WTW")
#    print(mcchg )
#    raise SystemExit
#    poolQuery()
#    raise SystemExit
    parser = argparse.ArgumentParser()
    parser.add_argument('main' , nargs='?', default="buy")
    parser.add_argument('--mode', default="default")
    parser.add_argument('--etf', default="IUSG")
    parser.add_argument('--date', default=today())
    parser.add_argument('--live', default=False, action="store_true")
    parser.add_argument('--cat', default="default")
    parser.add_argument('--catcount', default=7)
    parser.add_argument('--typed', default="low")
    parser.add_argument('--ht', default=None)
    parser.add_argument('--s', default=None)
    parser.add_argument('--save', default=None)
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

    modes = threadprep.getModes()
    if args.mode != "default":
        modes = [args.mode]

#    z.getStocks.extras = z.getStocks.devoverride == "IUSG"
    if args.date == "l":
        args.date = getLastDate()
 
    print("date : {}".format( args.date ))
    args.catcount = int(args.catcount)

    dask_help.convertToDask.directory = "csv"
    try:
        if args.main:
            if args.main == "stat":
                print ("from")
                print (getStats(args.s.upper(), idx=2))
                print ("\nto")
                print (getStats(args.s.upper(), idx=1))

            if args.main == "port":
                vals = portfolio.fidelity()
                print("vals : {}".format( vals ))
                print("vals : {}".format( z.percentage(vals[0])))

            elif args.main == "ranking":
                name = "{}cdics".format(z.getStocks.devoverride)
                print (name)
                lists = z.getp(name)
                for cat in catl:
                    print ("{} High".format(cat))
                    whatAboutThese(lists[cat][-1 * args.catcount:], 
                            dated = args.date)
                    print ("{} Low".format(cat))
                    whatAboutThese(lists[cat][:args.catcount], 
                            dated = args.date)

            elif "wab" in args.main:

                stocks = [args.s.upper()]
                if args.s == "wab":
                    stocks = z.getp("saved")
#                    stocks = z.getConsider()
                if args.s == "highest":
                    stocks = z.getp("highest").keys()
                    print("stocks : {}".format( stocks ))
                whatAboutThese(stocks, dated=args.date)


            # what to buy tomorrow
            if args.main == "query":
                queryh(args)

            # generate buy list which is ISUG + EXTRAS
            if "buy" in args.main or args.main == "buy" or args.main == 'gbuy':

                loadSortedEtf("BUY2")
                buyl(args, args.date)

            # generate buy list which is ISUG + EXTRAS
            if args.main == "sell":
                sells(args)

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
