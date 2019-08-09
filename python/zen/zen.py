from random import sample, randint
from functools import lru_cache
from collections import defaultdict, deque
from sortedcontainers import SortedSet
import matplotlib.pyplot as plt
import readchar
import csv
import dask_help
import math
import statistics
import os
import threadprep
import portfolio
import util
import z 
#
#import atexit
#import curses
#stdscr = curses.initscr()  # initialise it
#stdscr.clear()  # Clear the screen
#@atexit.register
#def goodbye():
#    """ Reset terminal from curses mode on exit """
#    curses.nocbreak()
#    if stdscr:
#        stdscr.keypad(0)
#    curses.echo()
#    curses.endwin()
closekey = z.closekey
keeping = 60
discardlocation = int(keeping/2)

def getPriceFromCsv(astock, date = None, openp=None):
    field = "Open"
    path = z.getPath("historical/{}.csv".format(astock))
    if not os.path.exists(path):
        path = z.getPath("ETF/{}.csv".format(astock))

    try:
        for row in csv.DictReader(open(path)):
            cdate = row['Date']
            if cdate == date:
                if not openp:
                    return float(row[field])
                return float(row["Open"]), float(row[closekey])

    except:
        return None
    

def getPrice(astock, date = None, openp=False):
    if not date:
        date = getLastDate()

    if openp == "both":
        try:
            return getPrice.pricedict[astock][date]
        except:
            try:
                getPrice.pricedict = z.getp("buydics52")
                return getPrice.pricedict[astock][date]
            except:
                pass

    idx = 0 if openp else 1
    try:
        return getPrice.pricedict[astock][date][idx]
    except:
        try:
            getPrice.pricedict = z.getp("buydics52")
            return getPrice.pricedict[astock][date][idx]
        except:
            pass
    try:
        return getPrice.pdict[astock][date]
    except Exception as e:
        try:
            name= "{}_P".format(loadSortedEtf.etf)
            getPrice.pdict = z.getp("{}_P".format(loadSortedEtf.etf))
            return getPrice.pdict[astock][date]
        except:
            return getPriceFromCsv(astock, date, openp=openp)
    print ("need more data")


def getPrice3(astock, date = None, openp=False):

    if not date or date == today():
        if not getPrice.latest:
            getPrice.latest = z.getp("latestprices")
        idx = 1 if openp else 0
        return getPrice.latest[astock][idx]
        
        if not getPrice.today:
            dates = z.getp("dates")
            getPrice.today = dates[-1]
        date = getPrice.today

    if openp:
        return getPriceFromCsv(astock,date)
    
    try:
        return getPrice.pdict[astock][date]
    except Exception as e:
        try:
            name= "{}_P".format(loadSortedEtf.etf)
            getPrice.pdict = z.getp("{}_P".format(loadSortedEtf.etf))
            return getPrice.pdict[astock][date]
        except:
            return getPriceFromCsv(astock, date, closekey)

    print("date : {}".format( date ))
    print("astock: {}".format( astock))
    raise SystemExit


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
            try:
                alist = getSortedStocks.cdict[mode][date]
            except:
                return None
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

def regenerateLatestPrices():
    print ("regenerating latest prices")
    getPrice.latest = dict()
    path = z.getPath("historical")
    listOfFiles = os.listdir(path)
    for entry in listOfFiles:  
        cpath = "{}/{}".format(path, entry)
        for row in csv.DictReader(open(cpath)):
            pass
        astock = os.path.splitext(entry)[0]
        getPrice.latest[astock] = ( float(row['Open']), float(row[closekey]) )

    path = z.getPath("ETF")
    listOfFiles = os.listdir(path)
    for entry in listOfFiles:  
        cpath = "{}/{}".format(path, entry)
        for row in csv.DictReader(open(cpath)):
            pass
        astock = os.path.splitext(entry)[0]
        getPrice.latest[astock] = ( float(row['Open']), float(row[closekey]) )

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
        close = df.at[idx,closekey]
        change = close/opend
        if change < 0.90:
            bought.append(close)
            order.append(astock)

            close2 = df.at[idx+1,closekey]
            change = close2/close
            if change < 1.0:
                downs += 1
            total.append(round(change,4))

def getDropScore(astock, startd = "2018-07-11", days = 64):
    try:
        return getDropScore.cache[astock][startd]
    except:
        pass

    recovery = -1
    df = z.getCsv(astock)
    if df is None:
        return "NA", recovery
    dates = df["Date"].tolist()

    try:
        starti = dates.index(startd)
    except:
        starti = 0

    minc = 10
    minp = None
    dayc = 0
    lastrecovday = None
    recovPrice = None
    for idx in range(starti, len(dates)-days):
        close = df.at[idx + days,closekey]
        opend = df.at[idx,"Open"]
        change = close/opend
        if change < minc:
            minc = change
            minp = close
            dayc = 0
            recovPrice = opend
            recovery = -1
        else:
            dayc += 1

            if recovPrice and close > recovPrice :
                recovery = dayc
                lastrecovday = df.at[idx, "Date"]
                recovPrice = None

    if minc > 1.00:
        return round(minc,4), "WOW"

    if recovery < 0:
        recovery = z.percentage(close / recovPrice,1)

    getDropScore.cache[astock][startd] = (round(minc,4), recovery)
    return round(minc,4), recovery


#z.getStocks.devoverride = "ITOT"
#print (getPricedStocks("2017-01-11", 3))
#raise SystemExit

def getProbSale(astock, dated = None):

    if not dated:
        dated = today()

    path = z.getPath("historical/{}.csv".format(astock))
    if not os.path.exists(path):
        path = z.getPath("ETF/{}.csv".format(astock))
        if not os.path.exists(path):
            print("DOES NOT EXIST: {}".format( path))
            raise SystemExit

    dates = z.getp("dates")
    startidx = dates.index(dated)-52
    startd = dates[startidx]

    downs = 0
    avgl = list()
    avgD = list()
    avgG = list()
    firstopen = None
    countidx = 0
    started = False
    largest = 1.00
    prevclose = None
    for row in csv.DictReader(open(path)):

        if not started:
            cdate = row['Date']
            if cdate == startd:
                started = True
                firstopen = float(row['Open'])
            else:
                continue
        elif countidx >= 52:
            break
        else:
            countidx += 1

        close = float(row[closekey])
        if not prevclose:
            prevclose = float(row['Open'])

        change = close/prevclose
        if change < largest:
            largest = change

        prevclose = close

        if change < 1.000:
            downs += 1
            avgD.append(change)
        else:
            avgG.append(change)
        avgl.append(change)

    if not avgl:
        print ("no avgl")
        print("path: {}".format( path))
        return

    avgC = z.avg(avgl, p=5)
    avgD = z.avg(avgD)
    probD = round(downs/len(avgl),2)
    live = util.getLiveData(astock, key = "price")
    live = live if live else close
    change = round(close/firstopen,3)

    return avgC, probD, avgD, statistics.median(avgG), change, statistics.median(avgl), largest

def plotProbSale(astock):

    path = z.getPath("historical/{}.csv".format(astock))
    if not os.path.exists(path):
        path = z.getPath("ETF/{}.csv".format(astock))
        if not os.path.exists(path):
            print("DOES NOT EXIST: {}".format( path))
            raise SystemExit

    dated = "2013-03-19"
    dates = z.getp("dates")
    startidx = dates.index(dated)
    startd = dates[startidx]

    downs = 0
    avgl = list()
    avgD = list()
    avgG = list()
    firstopen = None
    countidx = 0
    started = False
    droplist = deque([])

    for idx,row in enumerate(csv.DictReader(open(path))):

        if not started:
            cdate = row['Date']
            if cdate == startd:
                started = True
            else:
                continue

        if idx == 3930:
            cdate = row['Date']
            print("cdate : {}".format( cdate ))

        if idx == 4080:
            cdate = row['Date']
            print("cdate : {}".format( cdate ))

        if len(droplist) > 120:
            droplist.popleft()
            value = round(sum(droplist)/len(droplist),3)
            plt.scatter(idx, value)

        opend = float(row['Open'])
        close = float(row[closekey])

        change = close/opend
        if change < 1.000:
            downs += 1
            avgD.append(change)
            droplist.append(1)
        else:
            droplist.append(0)
            avgG.append(change)
        avgl.append(change)
    plt.show()


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
        

def getMCRank(astock):
    try:
        return getMCRank.dic.index(astock)
    except:
        try:
            getMCRank.dic = z.getp("ITOT_total_mcsorted_idx")
            return getMCRank.dic.index(astock)
        except:
            pass
    return "NA"

#skipss = ['CVET']
savedSort = SortedSet()
def whatAboutThisOne(value, sorts, noprices, avgChanges, avgchanget, avgOneYear, sellsl, lowprice = False, sell=False, ht=None, dated = None):
    global savedSort

    dates = z.getp("dates")
    astock = value

    if type(value) is tuple:
        astock = value[1]

    try:
        oprice, price = getPrice(astock, dated, openp = 'both')
        try:
            oprice = round(getPrice(astock, dates[-2]),3)
        except:
            pass
    except Exception as e:
        print("1no price dated: {}".format( dates[-2]))
        print("1no price dated: {}".format( dated))
        print("1no price astock : {}".format( astock ))
        noprices.append(astock)
#        raise SystemExit
        return

    try:
        idx4 = -5 if not dated else dates.index(dated)-5
        o3price = round(getPrice(astock, dates[idx4]),3)
    except:
        print("no price dated: {}".format( dated))
        print("no price astock : {}".format( astock ))
        noprices.append(astock)
        return

    chg3 = None
    chg1 = None
    cprice = price

    try:
        avgC, probD, avgD, avgG, chgT, median, largest = getProbSale(astock, dated)
    except Exception as e:
        z.trace(e)
        print("problem with astock: {}".format( astock))
        return

    mcrank = getMCRank(astock)

    try:
        beta, pe, mcchg, div = getChangeStats(astock)
    except Exception as e:
        beta, pe, mcchg, div = None, None, None, None
        pass

    recov = None

    try:
        d0, temp = getDropScore(astock, "2013-03-19", 30)
    except Exception as e:
        z.trace(e)
        print("probleme: {}".format( e))
        d0 = "NA"
        raise SystemExit

    try:
        d1, recov = getDropScore(astock, "2017-05-25", 45)
    except Exception as e:
        d1 = "NA"

    try:
        d2, temp = getDropScore(astock)
    except Exception as e:
        print("problem with astock: {}".format( astock))
        return

    live = "NA"
    try:
        live = util.getLiveChange(astock)
        if not live:
            live = "NA"
            chg1 = z.percentage(price/oprice,1)
            chg3 = z.percentage(price/o3price,1)
        else:
            cprice = live * price
            savedSort.add((live, astock))
            chg1 = z.percentage(cprice/oprice,1)
            chg3 = z.percentage(cprice/o3price,1)

    except Exception as e:
        print("astock: {}".format( astock))
        z.trace(e)
        raise SystemExit
        pass

    if sell:
        basis = portfolio.getBasis(astock)
        if (cprice / basis) < .8:
            sellsl.append(astock)

    try:
        avgds = z.avg([d0,d1,d2])
    except:
        try:
            avgds = z.avg([d1,d2])
        except:
            avgds = d2

    try:
        dscore = getDisplaySortValue(probD,avgC, avgD, live, avgds, astock, chgT)
    except:
        print("live: {}".format( live))
        print("avgds: {}".format( avgds))
        print("avgD: {}".format( avgD))
        print("avgC: {}".format( avgC))
        print("probD: {}".format( probD))
        return

#    ddscore = dscore
#    if getSortedStocks.highlight_score and dscore >= getSortedStocks.highlight_score:
#        ddscore = colored(ddscore, "green")  


#    if d2 > 1.00:
#        recov = "WOW"
#    elif avgC > 1.00:
#        recov = round(d2/(avgC-1.0),1)

    avgChanges.append(avgC)
    avgchanget.append(chgT)

    if mcchg and mcchg < 5.00:
        mcchg = z.percentage(mcchg)
    else:
        mcchg = "NA"

    if type(beta) == float:
        beta = round(beta,2)
    else:
        beta = "NA"
        
    if type(pe) == float:
        pe = round(pe,1)
    else:
        pe = "NA"

    if type(div) == float:
        div = round(div,3)
    else:
        div = "NA"


    # above etf rank
    try:
        etfrank = z.getp("ranklist").index(astock)
    except Exception as e:
#        print("astock: {}".format( astock))
#        print("astock: {}".format( len(z.getp("ranklist"))))
        etfrank = "NA"


    etfc = util.getEtfQualifications(astock, count=True)
    y1w, y1m = getYearly(astock)
    y1l = getLastYearChange(astock)
    if y1l != "NA":
        avgOneYear.append(y1l)
        y1l = z.percentage(y1l)
    ultrank = getUltRank(astock)
    try:
        if astock in myportlist:
            astock = "*{}".format(astock)
        else:
            astock = " {}".format(astock)
    except:
        pass

    try:
        values = [astock, price, 
            z.percentage(avgC, accurate=2), 
            z.percentage(median),
            probD, 
            z.percentage(avgD),
            z.percentage(avgG),
            z.percentage(d0),
            z.percentage(d1),
            z.percentage(d2),
            z.percentage(chgT),
            z.percentage(chg1),
            z.percentage(chg3),
            z.percentage(live),
            etfc, 
            recov,
            mcchg,
            beta,
            pe,
            z.percentage(largest),
            etfrank,
            div,
            mcrank,
            y1w,
            y1m,
            y1l,
            ultrank]

        msg = getCol().format(*values)
    except Exception as e:
        z.trace(e)
        return

    sorts.add((dscore,msg))
    return dscore, values

def getUltRank(astock):
    ultdict = z.getp("ultdict")
    try:
        return ultdict[astock]
    except:
        return "NA"
    return 

def getLastYearChange(astock):
    yearlydic = z.getp("latestAnnual")
    try:
        return yearlydic[astock]
    except:
        pass
    return "NA"

def getYearly(astock):
    yearlydic = z.getp("yearlydic")
    try:
        one, two = yearlydic[astock]
    except:
        return "NA", "NA"
    return z.percentage(one), z.percentage(two)

def getCol():
    #        astock $price avgC   median probD  avgD  avgG    d0     d1     d2     
    return " {0:<6} {1:>7} {2:>7} {3:>6} {4:>4} {5:>7} {6:>7} {7:>8} {8:>8} {9:>8} "\
           " {10:>7} {11:>6} {12:>6} {13:>7} {14:>4} {15:>6} {16:>6} {17:>5} {18:>6} {19:>8} {20:>7} {21:>8} {22:>7} {23:>8} {24:>8} {25:>8} {26:>5}"
           # chgT    chg1    chg3    live    etfc    recov   mcchg   beta    pe      largest etfrank div     mcrank  y1w     y1m     y1l     ultrank
buySaved = dict()
def whatAboutThese(stocks, lowprice = False, sell=False, ht=None, dated = None, title = None):
    global buySaved
    print(getCol().format("stock", "price", "avgC", "median", "probD", "avgD ", "avgG ", "d0" ,"d1 ", "d2 ", "chgT ", "chg1", "chg3", "live ", "etf ", "recov  ", "mcchg  ", "beta  ", "pe  ", "largest  ",  "erank  ", "div   ", "mcrnk  ","y1w","y1m", "y1l", "ultrank"))

    if not stocks:
        return

    sorts = SortedSet()
    sellsl = list()
    noprices = list()
    avgChanges = list()
    avgchanget = list()
    avgOneYear = list()
    highdscore = 0
    vals = list()
    for idx, value in enumerate(stocks):
        try:
            dscore, values = whatAboutThisOne(value, sorts, noprices, avgChanges, avgchanget, avgOneYear, 
                    sellsl, lowprice = lowprice, sell=sell, dated = dated)
        except:
            continue
        vals.append(values)
        if dscore and dscore > highdscore:
            highdscore = dscore

    if title:
        buySaved[title] = vals

    for astock in reversed(sorts):
        print(astock[1])

    if noprices:
        print("noprices: {}".format( noprices))

    if sell:
        print("sellsl")
        print(sellsl)

    if avgChanges:
        total = z.avgp(avgchanget)
        try:
            yearone = z.avgp(avgOneYear)
        except:
            yearone = "NA"
        print ("Average 52 day change {} - Total change {} - Annual Change {}".format(z.avgp(avgChanges), total, yearone))

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

#    stocks = z.getStocks(etf, reset=True)
    stocks = z.getp("ITOT_total_mcsorted")
    cdics = defaultdict(SortedSet)
    print("stocks: {}".format( len(stocks)))

    for astock in stocks:
        path = z.getPath("historical/{}.csv".format(astock))

        if not os.path.exists(path):
            print("problem with : {}".format( path ))
            continue

        for row in csv.DictReader(open(path)):
            pass
        try:
            cdics["C30"].add(( float(row['C30']) , astock))
            cdics["Volume"].add(( float(row['Volume']) , astock))
            cdics["Price"].add(( float(row[closekey]) , astock))
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

@lru_cache(maxsize=1)
def today(idx = 1):
    dates = z.getp("dates")
    return dates[-1 * idx]


def whatAboutThisMode(mode, typed, usedate, dated):
    scores = z.getp("modeScores")
    modestr = "{}/{}".format(mode, typed)
    msg = "\nmode : {}\ttyped: {}   {}   {}   {}".format( mode, typed, scores[modestr][0], scores[modestr][1], usedate)
    if modestr in goodmodes:
        msg = colored(msg,"green")
    if modestr not in skips:
        print(msg)
        stocks = getSortedStocks(usedate, mode, get="all", typed=typed)
#        if args.save == modestr:
#            z.setp(stocks, "saved")
        whatAboutThese(stocks, dated=dated)


startd = "2014-04-01"
buydics = None
buydics52 = None

def updateDics(listOfFiles, path, buydics52, buydics, date52, latest):

    for idx,entry in enumerate(listOfFiles):

        if not idx % 100:
            print("idx: {}".format( idx))

        tpath = "{}/{}".format(path,entry)
        start = False
        start52 = False
        astock = os.path.splitext(entry)[0]

        for row in csv.DictReader(open(tpath)):
            date = row['Date']

            if date == startd:
                start = True

            if date == date52:
                start52 = True

            if not start52 and latest:
                continue

            ans = (float(row['Open']), float(row[closekey]))

            if start52:
                buydics52[astock][date] = ans

            if not latest and start: 
                buydics[astock][date] = ans


def reloaddic(latest=True):
    global buydics, buydics52

    buydics = defaultdict(dict)
    buydics52 = defaultdict(dict)

    dates = z.getp("dates")
    print ("regenerating buydics52 {}".format(dates[-1]))
    date52 = dates[-52]

    path = z.getPath('historical')  
    listOfFiles = os.listdir(path)
    updateDics(listOfFiles, path, buydics52, buydics, date52, latest)

    path = z.getPath('ETF')  
    listOfFiles = os.listdir(path)
    updateDics(listOfFiles, path, buydics52, buydics, date52, latest)

    if not latest:
        z.setp(buydics, "buydics")

    z.setp(buydics52, "buydics52")

def buyl(args, dated):
    if "gbuy" in args.main:
        import update_history
        try:
            latestprices = dict()
            problems = [] 
            if update_history.update(prices = latestprices, problems = problems):
                if problems:
                    print("problems: {}".format( problems))
                    key = readchar.readkey()
                    if key == "d":
                        for pstock in problems:
                            z.delStock(pstock)
                        return
#                    if key != "c":
#                        return

                print ("finished update history 1")
                update_history.update(where= "ETF", prices=latestprices)
                print ("finished update history 2")
                z.setp(latestprices, "latestprices")
                import ranketf2
                ranketf2.regen()

                if "2" in args.main:
                    import json_util
                    json_util.saveOutstanding(update=True)
                    diffOuts()

                reloaddic()
#                threadprep.regenerateBUY()

                exit()

        except Exception as e:
            print ("problem with gbuy")
            z.trace(e)
            exit()

    loadSortedEtf("BUY2")
    print ("\netfs")

    dscore = whatAboutThese(z.getEtfList(forEtfs=True), dated=dated, title = "Standard ETFS")
    getSortedStocks.highlight_score = dscore

#    return
    
    if not len(modes) == 1:
        print ("\nlowyearly")
#        rankstock = z.getp("lowyear")
#        whatAboutThese(rankstock, dated=dated, title = "Yearly Low")

#        print ("\nranked")
#        rankstock = z.getp("rankstock")
#        whatAboutThese(rankstock, dated=dated, title = "RankStocks")
#
#        print ("\nranked2")
#        rankstock = z.getp("ranked_stocks")
#        whatAboutThese(rankstock, dated=dated, title = "RankStocks2")

        print ("\nranked_ult")
        rankstock = z.getp("ultrank")
        whatAboutThese(rankstock, dated=dated, title="RankUlt")

        print ("\nworst")
        rankstock = z.getp("worstrank")
        whatAboutThese(rankstock, dated=dated, title="WorstRank")

        print ("\nLowest")
        rankstock = z.getp("worstrank")
        whatAboutThese(rankstock, dated=dated, title="LowestRank")
    
        print ("\netf extended")
        rankstock = z.getp("ranketf")
        whatAboutThese(rankstock, dated=dated, title="ETFs")

#        key = readchar.readkey()
#        if key == "q":
#            return
        return

        try:
            print ("\ndiv extended")
            divs = z.getp("divset")[-30:]
            whatAboutThese(divs, dated=dated)
        except:
            pass

    z.setp(buySaved, "buySaved")

    usedate = dated or args.date
    for mode in modes:
        whatAboutThisMode(mode, "low", usedate, dated)
        whatAboutThisMode(mode, "high", usedate, dated)

#        key = readchar.readkey()
#        if key == "q":
#            return

    if savedSort:
        print ("\narranged change")
        whatAboutThese(savedSort[-5:], dated=dated)
        whatAboutThese(savedSort[:5], dated=dated)



goodmodes = ["Volume/low", "Price/low", "Var50/high", "Drops/high"]
skips = ["Price/high", "Var50/low", "Drops/low", "Volume/high", "C24/high", "C24/low"]

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
    count = len(stocks)
    count_vs_etf = z.getp("count_vs_etf")

    whatAboutThese(stocks, sell=True, dated=args.date)
    print("stocks : {}".format( len(stocks)))
    try:
        print("prob etf wins : {}".format( count_vs_etf[count]))
    except:
        pass

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
#        print("astock : {}".format( astock ))
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
    print ("regenerating pe/div/mc")
    outs = getOuts()
    out1 = outs[-1]
    print("out1 : {}".format( out1 ))
    out2 = outs[-2]
    print("out2 : {}".format( out2 ))
    out1dic = z.getp(out1)
    out2dic = z.getp(out2)
    divset = SortedSet()
    mcsets = SortedSet()
    mcdiff = dict()
    # out1dict is the newer one
    for astock, values in out1dic.items():
        try:
            changem = round( values[0]/out2dic[astock][0], 6)
    #        if changem == 1:
    #            changem = round( values[2]/out2dic[astock][2], 6)
            mcdiff[astock] = (values[1], values[2], changem, values[3])
            mcsets.add((changem,astock))
            if type(values[3]) is float:
                price = getPrice(astock)
                if price > 40.00:
                    divset.add((values[3],astock))
        except:
            pass
#    print(ossets[-10:])
#    print(ossets[:10])
#    print(mcsets[-10:])
#    print(mcsets[:10])
    z.setp(divset, "divset")
    z.setp(mcdiff, "mcdiff")
    z.setp(mcsets, "mcsets")


def getChangeStats(astock, idx=1):
    try:
        return getChangeStats.outdic[astock]
    except:
        try:
            getChangeStats.outdic = z.getp("mcdiff")
            return getChangeStats.outdic[astock]
        except:
            pass
    return None, None, None, None


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
        pass
    return row['Date']

@lru_cache(maxsize=1)
def getEtfFeeDic():
    path = z.getPath("ProductScreener.csv")
    ret = dict()
    try:
        for row in csv.DictReader(open(path)):
            try:
                ret[row["Ticker"]] = row['Fee1']
            except:
                pass
    except:
        pass
    return ret


def getLongEtfList():
    path = z.getPath("ProductScreener.csv")
    ret = list()
    try:
        for row in csv.DictReader(open(path)):
            try:
                ret.append(row['Ticker'])
            except:
                pass
    except:
        pass
    return ret

def getPrevChange(astock, year):
    dates = z.getp("dates")
    date = dates[-252*year]
    print("date : {}".format( date ))
    return round(getPrice(astock)/ getPrice(astock, date),3)

if __name__ == '__main__':
    import argparse
    import sys
    import zprep
    from termcolor import colored
#    print (getPrevChange("BA", 1))
#    print (getPrevChange("BA", 2))
#    print (getPrevChange("BA", 3))

#    raise SystemExit

    getDropScore.cache = z.getp("dropcache")
    if getDropScore.cache is None:
        getDropScore.cache = defaultdict(dict)

#    raise SystemExit
#    mcchg = getChangeStats("AAPL")
#    print(mcchg )
#    raise SystemExit
#    poolQuery()
#    raise SystemExit
    parser = argparse.ArgumentParser()
    parser.add_argument('main' , nargs='?', default="buy")
    parser.add_argument('--mode', default="default")
    parser.add_argument('--etf', default="IUSG")
    parser.add_argument('--date', default=getLastDate())
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
#    if args.date == "l":
    args.date = getLastDate()
 
    print("date : {}".format( args.date ))
    args.catcount = int(args.catcount)

    dask_help.convertToDask.directory = "csv"

    myportlist = z.getp("myportlist")
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
#                    print("stocks : {}".format( stocks ))
                if args.s == "etfs":
                    stocks = getLongEtfList()
                whatAboutThese(stocks, dated=args.date)


            # what to buy tomorrow
            if args.main == "query":
                queryh(args)

            # generate buy list which is ISUG + EXTRAS
            if "buy" in args.main or args.main == "buy" or args.main == 'gbuy':
                buyl(args, args.date)

            # generate buy list which is ISUG + EXTRAS
            if "sell" in args.main:
                if "r" in args.main:
                   regenerateLatestPrices() 
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

        z.setp(getDropScore.cache, "dropcache")
    except Exception as e:
        z.trace(e)
        pass
