import z
import math
import csv
from collections import defaultdict
import table_print
import statistics
import os
from sortedcontainers import SortedSet
from rows import *

ordering = False
sortcats = ["wc", "bc", "avg", "avg8", "ivvb", "ly"]
#table_print.accurate = 2

# mc 30.00B to 1.54T
# mc 7.5B to 30.00B 
# mc 2.7B to 7.5B
# mc 0 to 2.7B 
def addSorted(title, val, astock, keeping = 60):
    discardlocation = int(keeping/2)
    addSorted.dic[title].add((val, astock))
    if len(addSorted.dic[title]) > keeping:
        addSorted.dic[title].discard(addSorted.dic[title][discardlocation])

def addSortedLow(title, val, astock, keeping = 30):
    addSorted.dic[title].add((val, astock))
    if len(addSorted.dic[title]) > keeping:
        addSorted.dic[title].pop()

def addSortedHigh(title, val, astock, keeping = 30, savingall = False):
    addSorted.dic[title].add((val, astock))

    if savingall:
        addSorted.dic2[astock] = val

    if len(addSorted.dic[title]) > keeping:
        addSorted.dic[title].pop(0)


addSorted.dic2 = dict()
addSorted.dic = defaultdict(SortedSet)

def getapd(values):
    count = len(values)
    change = values[-1]/values[0] if count < 15 else min(values[-5:]) / max(values[:5])
    return change**(1/count)

def getapds(changes):
    half = math.ceil(len(changes)/2)
    half1 = changes[:half]
    half2 = changes[-1*half:]
    apd1 = getapd(half1)
    apd2 = getapd(half2)
    apd = getapd(changes)
    return apd1, apd2, round(apd2/apd1,3), apd

def clearSorted(title):
    addSorted.dic[title] = SortedSet()

def getSorted(title):
    return addSorted.dic[title]

def saveSorted(title):
    z.setp(list(addSorted.dic[title]), title, True)

    if addSorted.dic2:
        z.setp(addSorted.dic2, "{}dic".format(title))

#for b in range(100):
#    addSorted("blah", b, "KO")
#    addSortedHigh("blahh", b, "KO")
#    addSortedLow("blahl", b, "KO")
#bar = getSorted("blah")
#print("bar : {}".format( bar ))
#bar = getSorted("blahh")
#print("bar : {}".format( bar ))
#bar = getSorted("blahl")
#print("bar : {}".format( bar ))
#exit()

#start = 37
start = 107
istart = 107 * -1
thirty = start - 25
ten_from_start = start - 10
five_from_start = start - 5
dates = z.getp("dates")

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

def getLongProbDown(astock):
    try:
        return round(getLongProbDown.dic[astock],2)
    except:
        try:
            getLongProbDown.dic = z.getp("prob_down")
            return round(getLongProbDown.dic[astock],2)
        except Exception as e:
            pass
    return "NA"
getLongProbDown.dic = None

def sortedSetToRankDict(saveas, sset, reverse=False, printdata = False):
    sort = dict()
    if reverse:
        for i, pair in enumerate(reversed(sset)):
            astock = pair[1]
            sort[astock] = i + 1
    else:
        for i, pair in enumerate(sset):
            astock = pair[1]
            sort[astock] = i + 1
    z.setp(sort, saveas, printdata=printdata)


#    sortedSetToRankDict("bar", sset, True, True)

#bar = SortedSet()
#bar.add((123,"astock"))
#bar.add((13,"bstock"))
#bar.add((213,"cstock"))
#sortedSetToRankDict("bar", bar, True, True)
#sortedSetToRankDict("bar", bar, False, True)
#exit()

def getMCDiv(astock):
    try:
        return getMCDiv.dic[astock]
    except:
        try:
            getMCDiv.dic = z.getp("mcdivdict")
            return getMCDiv.dic[astock]
        except:
            pass
    return ["NA", 3999, "NA"]

def getMCRank(astock):
    return getFrom("latestmc", astock, 3999)
    try:
        return getMCDiv(astock)[1]
    except:
        return 3999


def setVolRankDict():
    stocks = z.getp("listofstocks")
#    stocks = ["BA", "AMD", "KO"]
    dates = z.getp("dates")
    sset = SortedSet()
    sset1 = SortedSet()
    for astock in stocks:
#        try:
#            rank = getMCRank(astock)
#            if rank > 1000:
#                continue
#        except:
#            continue

        avg = list()
        for i, arow in enumerate(getRows(astock, dates[-117])):
            try:
                avg.append(int(arow['Volume']))
                if i > 10:
                    break
            except:
                break
        try:
            avgv = round(statistics.mean(avg))
#            if avgv > 100099:
#                sset1.add((avgv, astock))
#                if len(sset1) > 30:
#                    sset1.remove(sset1[-1])
            sset.add((avgv, astock))
#            if len(sset) > 30:
#                sset.remove(sset[0])
        except:
            pass

#    z.setp(sset, "hvollrank", True)
#    sortedSetToRankDict("voldic", sset, reverse=True)
#    z.setp(sset1, "hvollrank1", True)
#    for pair in reversed(sset):
#        print("pair : {}".format( pair ))

def getPrice(astock, date = dates[-1], openp=False):
    year = date.split("-")[0]
    filename = "{}_{}".format(astock, year)

    if getPrice.last != filename:
        getPrice.last = filename
        path = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
        for row in csv.DictReader(open(path)):
            getPrice.recent[row['Date']] = float(row['Open']), float(row[z.closekey])

    if openp == 'both':
        return getPrice.recent[date]

    idx = 0 if openp else 1
    return getPrice.recent[date][idx]
getPrice.last = None
getPrice.recent = dict()

#def getFiles(astock, date = "2000"):
#    yield z.getPath("historical/{}.csv".format(astock))
#    return
#    added = False
#    for year in getYears(date):
#        apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
#        if os.path.exists(apath):
#            added = True
#            yield apath

#def getYears(date):
#    away_year = int(date.split("-")[0])
#    dates = z.getp("dates")
#    date_away = dates[-1]
#    while int(away_year) != z.YEAR:
#        yield away_year
#        away_year += 1
#    yield away_year
#
#def getRows(astock, date = "2000"):
#    date_year = date.split("-")[0]
#    for apath in getFiles(astock, date):
#
#        started = False
#        for row in csv.DictReader(open(apath)):
#            if date_year not in apath:
#                yield row
#            elif started:
#                yield row
#            elif row['Date'] == date:
#                started = True
#                yield row

def updateDates():
    dates = z.getp("dates")
    new = list()
    for row in getRows("IVV", dates[0]):
        new.append(row['Date'])
    z.setp(new, "dates")
    z.getp.cache_clear()

#for afile in getFiles("KO", date_away):
#    print("afile : {}".format( afile ))


#def processYears(astock, days_ago):
#    path = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
#    for row in csv.DictReader(open(path)):
#        getPrice.recent[row['Date']] = row['Open'], row[z.closekey]

def getDropScore(astock, startd, length):
    try:
        return getDropScore.cache[astock][startd]
    except:
        pass

    seen = list()
    changes = list()
    dayone = "*"
    for i, row in enumerate(getRows(astock, startd)):
        if i == 0 and startd == row['Date']:
            dayone = ""
        c_open = float(row['Open'])
        c_close = float(row[z.closekey])

        seen.append(c_close)
        if len(seen) >= length:
            daysAgoValue = seen[i-length]
            change5 = c_close/daysAgoValue
            changes.append(change5)

    if not changes:
        return ""
    minc = min(changes)
    ret = "{}{}".format(dayone, z.percentage(round(minc,3)))
    getDropScore.cache[astock][startd] = ret
    return ret

def getLastYearChange(astock, dated = None):
    if not dated:
        dates = z.getp("dates")
        dated = dates[-1]

    yearlydic = z.getp("latestAnnual")
    try:
        return yearlydic[astock]
    except:
        pass
    return "NA"

def portFolioValue(astock):
    if astock in portFolioValue.dict:
        return round(portFolioValue.dict[astock])
    return ""

def inPortfolio(astock):
    if (portFolioValue(astock)):
        return "*{}".format(astock)
    return astock

def getOrder(astock):
    global orders
    if astock not in orders:
        return "NA"
    try:
        return orders[astock][0]
    except Exception as e:
        return "NA"

dic = dict()
def getFrom(name, astock, default=0):
#    if astock == "MSFT":
#        bar =  dic[name][astock]
#        print("bar : {}".format( bar ))
    try:
        return dic[name][astock]
    except:
        if name not in dic.keys():
            dic[name] = z.getp(name)
            try:
                return dic[name][astock]
            except:
                pass
    return default

def getRsi(ups, downs):
    total = len(ups) + len(downs) + 1
    m1 = sum(ups)/total
    m2 = sum(downs)/total
    if m2 == 0:
        return 100
    return round(100-(100/(1+ (m1/m2))),1)

lastosDate = None
lastosDate2 = None
#def getOSChange(astock):
#    global lastosDate, lastosDate2
#    try:
#        datez = getFrom("wlp_dict", astock)
#        if not lastosDate:
#            datezl = list(datez)
#            lastosDate = datezl[-1] 
#            lastosDate = datezl[-400] 
#        mc, dr, out, ebit = datez[lastosDate]
#    except:


#print (getPrice("KO", "2019-01-09"))
#
#exit()
HIGHEST = 10000
daysAgo5 = 5
#recentStats = dict()
def genRecentStat(astock):
#    global recentStats

    seen = list()
    avg5Change = list()
    firstPrice = None
    lowFromHigh = HIGHEST
    high = 0
    mins = list()
    c_close = None
    daysAgoValue = None
    wc_highs = list()
    wc_lows = list()
    daysup = list()

    c_maxups = 0 
    maxup = 0 
    c_maxdown = 0 
    maxdown = 0 
    upd = ""

    prices = list()
    bchanges = list()

    for i, row in enumerate(getRows(astock, dates[istart])):
        c_open = float(row['Open'])

        if len(wc_highs) < 5:
            wc_highs.append(float(row['High']))

        if not firstPrice:
            firstPrice = c_open

        c_close = float(row[z.closekey])
        prices.append(c_close)

        try:
            change = round(c_close / prev_close,3)
            bchange = (change) if (change > 1) else round(prev_close/c_close,3)
            bchanges.append(bchange)
        except:
            prev_close = c_close

        upchange = (c_open <= c_close)
        if upchange:
            c_maxups += 1
            c_maxdown = 0 
            if c_maxups > maxup:
                maxup = c_maxups
        else:
            c_maxups = 0 
            c_maxdown += 1
            if c_maxdown > maxdown:
                maxdown = c_maxdown

        daysup.append(1 if upchange else 0)

        if i >= five_from_start:
            dchange = c_close / c_open

        if i < ten_from_start:
            if c_open > high:
                high = c_open
                lowFromHigh = HIGHEST

            if c_open < lowFromHigh:
                lowFromHigh = c_open

            if c_close > high:
                high = c_close
                lowFromHigh = HIGHEST

            if c_close < lowFromHigh:
                lowFromHigh = c_close

        else:   
            wc_lows.append(float(row['Low']))

        seen.append(c_close)
        if len(seen) >= daysAgo5:
            daysAgoValue = seen[i-daysAgo5]
            change5 = c_close/daysAgoValue
            avg5Change.append(change5)
            if change5 < 1:
                mins.append(change5)

    try:
        wcc = round(min(wc_lows)/ max(wc_highs),3)
        lchange = round(c_close / firstPrice,3)
        diff = round(wcc / lchange,2)
    except:
        wcc = "NA"
        lchange = "NA"
        diff = "NA"

    min5 = round(min(avg5Change),3)
    last5 = round(avg5Change[-1],3)

    meandrop = "NA"
    if mins:
        mean = statistics.mean(mins)
        meandrop = round(( mean + mean + min(mins))/3 * c_close, 2)

    dayup = "NA"
    lengs = len(daysup)
    bar = lengs-start 
    if lengs-start < 2:
        dayup = round(sum(daysup)/lengs,2)
    last = round(c_close/seen[-2],3)

    be = round(sum(bchanges)/len(bchanges),2)
    ravg = round(statistics.mean(prices[-20:]),2)
    return c_close, wcc, lchange, diff, min5, last5, meandrop, dayup, maxup, maxdown, lowFromHigh, high, last, prices, be, ravg

def genRecentStats():
    recentStats = dict()
    stocks = z.getp("listofstocks")
    for idx, astock in enumerate(stocks):
        try:
            recentStats[astock] = genRecentStat(astock)
        except Exception as e:
            print("no astock: {}".format( astock))
            pass
    z.setp(recentStats, "recentStats")

#genRecentStats()
#exit()

lastchange = "{}chg".format(start)
fromtop = "{}drop".format(start)
wcchange = "{}wc".format(start)
diffS = "{}diff".format(start)

#genRecentStat("ANSS")
#exit()

def single(value, avgOneYear, retval = None, lots = True):
    global torys, mine, tory

    if type(value) is tuple:
        astock = value[1]
    else:
        astock = value

#    try:
#        c_close, wcc, lchange, diff, min5, last5, meandrop, dayup, maxup, maxdown, lowFromHigh, high, last, prices, be, ravg = getFrom("recentStats", astock)
#    except Exception as e:
    try:
        c_close, wcc, lchange, diff, min5, last5, meandrop, dayup, maxup, maxdown, lowFromHigh, high, last, prices, be, ravg = genRecentStat(astock)
    except:
        print("problem astock: \"{}\"".format( astock))
        return retval

#    if be > 1.10:
#        return False

    mc = "NA"
    pe = "NA"
    try:
        both = getMCDiv(astock)
        mc = both[1]
        pe = both[2]
        div = round(both[0]*100,2)
    except:
        div = "NA"

    prev_close = c_close
    if args.live:
        try:
            live = z.getLiveData(astock, key = "price")
            if not live:
                print("NO LIVE astock: {}".format( astock))
                z.breaker(2)
            c_close = live if live else c_close
#            change = c_close/daysAgoValue
        except Exception as e:
            z.trace(e)
            exit()

#    d13_30 = getDropScore(astock, "2013-03-19", 30)
#    d17_45 = getDropScore(astock, "2017-05-25", 45)
    d18_64 = getDropScore(astock, "2018-07-11", 64)


    name = ""
        
    order = getOrder(astock)

    if order != "NA":
        name = "_TO" if astock in torys else "_PO"
    if astock in mine:
        name = "(m)" + name
    if astock in tory:
        name = "(t)" + name

#    downs = ""
    owned = portFolioValue(astock)
#    if owned:
#        try:
#            downs = getFrom("downps", astock)
#            b = [ str(i) for i in downs ]
#            downs = ",".join(b)
#        except:
#            downs = ""
#
    score = 0

    try:
        y1pu, ivvb, wc, bc, avg, ly, l2y, avg8 = getFrom("probs", astock)
    except Exception as e:
        z.trace(e)
        exit()

    val = 0
    try:
        val += div if div < .7 else .7
    except:
        pass
    try:
        val += .2 if pe < 100 else 0 
    except:
        pass

    try:
        score = round(val + y1pu + dayup, 2)
    except Exception as e:
#        print("astock: {}".format( astock))
#        print("val : {}".format( val ))
#        z.trace(e)
#        print("dayup: {}".format( dayup))
#        print("y1pu : {}".format( y1pu ))
#        print ("no score")
#        z.breaker(5)
        
        score = 0

    try:
        med9, tgt9, often, adl, avgtgt = getFrom("low_target", astock)
        often = round(often, 2)
    except:
        med9, tgt9, often, adl = "NA", "NA", "NA", "NA"


#    hld, hlr = getFrom("hldic", astock, ("",""))
    apd1, apd2, apdc, apd = getapds(prices)

#        ("maxu", maxup),
#        ("maxd", maxdown),
#        ("mcc", mcc),
#        ("upd", upd),
#        ("1apd", apd1),
#        ("2apd", apd2),


    try:
        tgtchg = avgtgt/med9
    except:
        tgtchg = "NA"

    gain, drop = getFrom("prob_drop", astock, ("NA", "NA"))
    values = [
        ("stock", inPortfolio(astock)),
        ("price", c_close),
        ("avg20", ravg),
        ("change", c_close/ravg),
        ("beta", be),
        ("min5", min5),
        ("last5", last5),
        (lastchange, lchange),
        (wcchange, wcc),
        (diffS, diff),
        ("mc", getFrom("latestmc", astock, "")),
        ("d18_64", d18_64),
        ("score", score),
        ("y1pu", y1pu),
        ("daily", dayup),
        ("ivvb", ivvb), 
        ("apdc", apdc),
        ("apd", apd),
        ("div", div),
        ("ly", ly),
        ("l2y", l2y),
        ("bc", bc),
        ("wc", wc),
        ("avg", avg),
        ("avg8", avg8),
        (fromtop, (lowFromHigh/high)),
        ("meandrop", meandrop),
        ("tgt9", tgt9),
        ("med9", med9),
        ("often", often),
        ("avgtgt", avgtgt),
        ("tgtchg", tgtchg),
        ("gain", gain),
        ("drop", drop),
        ("beta21", getFrom("beta21dic", astock)),
        ("adl", adl),
        ("owned", portFolioValue(astock)),
        ("name", name) ]
#        ("down", downs),
#        ("hldic", hld),
#        ("ratio", hlr),

    if ordering:
        chgchg = 0
        try:
            orderchange = order[1]/c_close
            chgchg = round(med9/ orderchange,3)
        except:
            pass

        orderstr = round(order[0])
        values.append(("order", orderstr))
        values.append(("orderc", orderchange))
        values.append(("chgchg", chgchg))

    if args.live:
        values.append(("last", (c_close/prev_close)))
    else:
        values.append(("last", last))

    table_print.store(values)

#single("IVV")
#exit()

problems = set()
def multiple(stocks, title = None, helpers = True, runinit = False, retval=None, cleartable=True):
    if args == None:
        init()

    global problems
    if runinit:
        init()

    if type(stocks) is str:
        if not title:
            title = stocks
        stocks = z.getp(stocks)

    lots = len(stocks) > 15
    avgOneYear = list()
#    if args.drop:
#        print ("droppping")
#        print (args.drop)
#
#        for idx, astock in enumerate(stocks):
#            print("astock : {}".format( astock ))
#
#            if type(astock) is tuple:
#                astock = astock[0] if type(astock[0]) is str else astock[1]
#
#            live = z.getLiveData(astock, key = "price")
#            prev = getFrom("last_prices", astock)
#            try:
#                change = live/prev
#                addSortedLow("show_these", change, astock, keeping = int(args.drop))
#            except:
#                pass
#        stocks = getSorted("show_these")

    for idx, value in enumerate(stocks):
        astock = value 
        if type(value) is tuple:
            astock = value[1]
#            if not astock.startswith(args.helpers) and helpers:
#                print("skipping astock : {}".format( astock ))
#                continue
        try:
            ret = single(astock, avgOneYear, retval=retval, lots=lots)
            if ret == False:
                print("astock : {}".format( astock ))
        except Exception as e:
            z.trace(e)
            if type(value) is tuple:
                astock = value[1]
            else:
                astock = value
            problems.add(astock)
            continue

#    table_print.printTable(title)
    if cleartable:
        table_print.clearTable()

    try:
        yearone = z.avgp(avgOneYear)
    except:
        yearone = "NA"
    print ("Annual Change {}".format(yearone))
    print ("Problems {}".format(", ".join(problems)))

def multiplep(title):
    bar = z.getp(title)
    barl = int(len(bar)/2)
    multiple(bar[:-barl], helpers=False)
    multiple(bar[barl:], helpers=False)
    table_print.initiate()
    exit()

args = None
def init(live=False):
    import argparse
    global orders, torys, tory, mine, parser, args, savedhelper

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default="default")
    parser.add_argument('--live', nargs='?', const=True, default=False)
    parser.add_argument('--drop', default=None)
    parser.add_argument('--nc', nargs='?', const=True, default=False)
    parser.add_argument('--section', default=None)
    parser.add_argument('helpers', type=str, nargs='?', default = [])
    args = parser.parse_args()
    print("args : {}".format( args ))
    if live:
        args.live = True
    savedhelper = None

    if args.helpers:
        savedhelper = args.helpers
#        args.helpers = args.helpers[0].upper()

    table_print.setArgs(args)

    portFolioValue.dict = z.getp("ports")
#    companies = z.getp("company")
    orders = z.getp("orders")
    torys = z.getp("torys")
    tory = z.getp("tory")
    mine = z.getp("mine")
    getDropScore.cache = z.getp("newdropcache")
    if getDropScore.cache is None:
        getDropScore.cache = defaultdict(dict)
    getDropScore.cache = defaultdict(dict)

    table_print.use_percentages = ["avg5", "min5", "last5", lastchange, "orderc", "mcc", "basisc", fromtop, wcchange, diffS, "med9", "strat", "1apd", "2apd", "apd", "adl", "change", "ly", "bc", "wc", "avg", "avg8", "l2y", "gain", "drop", "avgtgt", "tgtchg"]
    table_print.gavgs = ["107chg", "y1w", "y1pu", "ivvb"]
#    if args.live:
    table_print.use_percentages.append("last")


def testLoop(astock):

    c_maxups = 0 
    maxup = 0 
    upd = ""
    for i, row in enumerate(getRows(astock, dates[-1*start])):
        try:
            c_open = float(row['Open'])
        except:
            return retval

        c_close = float(row[z.closekey])
        upchange = (c_open <= c_close)
        if upchange:
            c_maxups += 1
            c_maxdown = 0 
            if c_maxups > maxup:
                maxup = c_maxups
        else:
            c_maxups = 0 
            c_maxdown += 1
            if c_maxdown > maxdown:
                maxdown = c_maxdown

        if i >= five_from_start:
            upd += "u" if upchange else "d"

def handleDic(mode):
    print("mode: {}".format( mode))
    bar = z.getp(str(mode))
    print("bar : {}".format( bar ))
    try:
        for key, value in bar.items():
            if "ITOT" in key:
                continue
            multiple(value, title = key)
    except:
        try:
            print ("huh")
            multiple(bar, title = mode)
        except:
            pass
    table_print.initiate()
            
if __name__ == '__main__':
    init()
    probms = ['RLGT', 'RNR', 'STLD', 'TCFC', 'TMUS', 'WHLR']
    z.online.online = args.live

    if args.mode == "all":
        stocks = set(z.getp("better_etf"))

        mcs = z.getp("worst")
        stocks |= set([ b for a,b in mcs[0:30] ])

        for cat in sortcats:
            items = z.getp(cat)
            stocks |= set([ b for a,b in items ])

        multiple(list(stocks), title="all")
        table_print.initiate()
        exit()

    if args.mode == "special":
#        multiple("worst_smallcalp")
#        multiple("best_smallcalp")

        multiple(["CMD", "WBA", "MET", "BFAM", "ALGN"])
#        multiple("lowbeta")
#        multiple("highbeta")
#        multiple("highscore")
        multiple("highscore_large")

        table_print.initiate()
        exit()

    if args.mode == "single":
        astock = savedhelper.upper()
        try:
            ret = multiple([astock], "single", retval=False)
            print("ret : {}".format( ret ))

            if ret == False:
                import regen_stock
                regen_stock.process(astock)
                ret = multiple([astock], "single")
                if ret == False:
                    exit()

            table_print.initiate()
        except Exception as e:
            z.trace(e)

        exit()

    if args.mode == "multiple":

        print("handleDic: {}".format( args.mode))
        exit()

        print("savedhelper: {}".format( savedhelper))
        if args.section == "b":
            multiplep(savedhelper)
        else:
            multiple(savedhelper, helpers=False)
        table_print.initiate()
        exit()

    if args.mode == "owned":
#        import time
#        start = time.time()

        multiple(portFolioValue.dict.keys(), "owned")

#        end = time.time() - start
#        print("end : {}".format( end ))

        z.setp(problems, "problems")
        table_print.initiate()
        exit()

    if "order" in args.mode:
        ordering = True
        multiple(orders.keys(), title = "Orders")
        table_print.initiate()
        exit()

    if "benchmark" in args.mode or "etfs" in args.mode:
        multiple(z.getEtfList(buys=True), title = "Standard ETFS")
        table_print.initiate()
        exit()

    if "rand" in args.mode:
        multiple(["VUG", "IUSG"])
        multiple(["IVV", "VOO"])
        multiple(["USMV", "VFMV"])
#        multiple(["VUG", "IUSG", "VOO", "IVV", "USMV", "VFMV"])
        stocks = z.getp("listofstocks")
        import random
        multiple([stocks[random.randint(1,len(stocks))] for b in range(0,10)])
        table_print.initiate()
        exit()
        
    if "notes" in args.mode:
#        multiple(['NVMI', 'CASS', 'SP', 'RILY', 'GTY', "CKH", "CMCO", "CNXN", "BFS", "WMK", "KOP", "CENT", "LORL", "TTEC", "MTSC"], title = "fidelity_s1")
#        multiple(['ADES', 'MNLO', 'QTRX', 'REGI', 'SRRK'])
        bar = "AAPL AXP BA CAT CSCO CVX DIS DOW GE GS HD IBM INTC JNJ JPM KO MCD MMM MRK MSFT NKE PFE PG TRV UNH UTX V VZ WMT XOM"
        multiple(bar.split(" "))
        bar = ['NGLOY', 'ABB', 'AEG', 'ADRNY', 'AKZOY', 'AMOV', 'AMX', 'ASML', 'AXAHY', 'AZN', 'BBD', 'BBL', 'BCH', 'BCS', 'BASFY', 'BHP', 'BNPQY', 'BP', 'BTI', 'EBR', 'CAJ', 'CEO', 'CHA', 'CHL', 'CRH', 'TCOM', 'CUK', 'DANOY', 'DEO', 'DTEGY', 'E', 'ERIC', 'FMS', 'FMX', 'GSK', 'HSBC', 'HDB', 'HEINY', 'HMC', 'IBN', 'IFNNY', 'INFY', 'ING', 'ITUB', 'IMBBY', 'IX', 'KB', 'KEP', 'KOF', 'LFC', 'LYG', 'MT', 'MUFG', 'NMR', 'NOK', 'NTES', 'NVO', 'NVS', 'PBR', 'PHG', 'PKX', 'PTR', 'PUBGY', 'PUK', 'REPYY', 'RHHBY', 'VALE', 'RIO', 'RELX', 'RYAAY', 'BSAC', 'SAP', 'SBS', 'SHG', 'SKM', 'SMFG', 'SNE', 'SNN', 'SNP', 'SNY', 'SSL', 'STM', 'EQNR', 'TEF', 'TLK', 'TM', 'TOT', 'TS', 'TSM', 'VIV', 'UL', 'UN', 'VOD', 'WBK', 'WIT', 'WMMVY', 'FERGY', 'WPP', 'BBVA', 'IHG', 'NGG', 'BIDU', 'EDU', 'CS', 'MFG', 'MLCO', 'SAN', 'RBS', 'CHT', 'GLPG', 'EC', 'BUD', 'BSBR', 'HTHT', 'TAL', 'GRFS', 'BBDO', 'WUBA', 'ABEV', 'WB', 'JD', 'BABA', 'LN', 'ZTO', 'BDXA', 'SE', 'IQ', 'ASX', 'PDD', 'TME']
        multiple(bar)
#        multiple("newstuff")
#        multiple("probs_added_up")
        table_print.initiate()
        exit()

    if "accounts" in args.mode:
        multiple(["CI", "IGM", "IHI", "IJH", "IJR", "IUSG", "USMV", "VOO"], title = "traditiona_ira_zhang")
        multiple(["GOOGL", "ICLN", "IGM", "IHI", "IUSG", "IVV", "IWB", "MTUM", "PFE", "SAP", "SPGI", "USMV" ], title = "traditiona_ira_zhang")
        multiple(["BDX", "IGM", "IVV", "IYH", "USMV"], title = "brokerage_roth_zhang")
        multiple(["ATO", "BYND", "CDW", "ELS", "EXPO", "FIS", "HDB", "HEI", "MPWR", "NKE", "VFMV", "VPU", "VUG"], title = "traditional_tat")
        multiple(["AYX", "GE", "HQY", "IUSG", "SNAP", "SO", "SOXX", "TNDM", "VTI", "VUG", "WM"], title = "roth_tat")
        multiple(["AYX", "GE", "HQY", "IUSG", "SNAP", "SO", "SOXX", "TNDM", "VTI", "VUG", "WM"], title = "roth_tat")
#        multiple(items[30:60], title = "MC2")
#        multiple(items[210:240], title = "MC1")
#        multiple(items[240:270], title = "MC2")
#        multiple(items[270:300], title = "MC3")
        table_print.initiate()
        exit()

    if "worst" in args.mode:

        mcs = z.getp("worst")
        for i in range(0, 5):
            idx = i * 30
            end = idx + 30
            multiple(mcs[idx:end], title = "Worst {} to {}".format(idx, end))
        table_print.initiate()
        exit()

    if "mc" in args.mode:
        mcdic = z.getp("latestmc")

        mcs = list(mcdic.keys())
        for i in range(0, 5):
            print (i)
            idx = i * 30
            end = idx + 30
            multiple(mcs[idx:end], title = "MC {} to {}".format(idx, end))
        table_print.initiate()
        exit()

    if args.mode == "daily":
        for cat in ["change_1", "change_5", "change_s"]:
            items = z.getp(cat)
            multiple(items[-30:], "{}.top".format(cat))
            multiple(items[:30], "{}.bottom".format(cat))
        table_print.initiate()
        exit()

    print("handleDic2: {}".format( args))
    if args.mode == "sorted":
        for cat in sortcats:
            print("cat: {}".format( cat))
            items = z.getp(cat)
            print("items : {}".format( items ))
            multiple(items[-30:], "{}.top".format(cat))
            multiple(items[:30], "{}.bottom".format(cat))
        table_print.initiate()
        exit()

    if not args.mode == "default":
        handleDic(args.mode)
        exit()

    if args.helpers:
        handleDic(args.helpers)
        exit()

    try:
        multiple("avg30c")
        multiple("best30c")
        multiple("worst30c")
    except:
        pass

    exit()
#
#    m1 = ["COST", "WMT", "NKE", "FB", "MSFT", "TGT", "BABA", "NFLX", "AMZN", "GOOG", "AMD", "ADBE", "DIS", "KO", "TSLA", "WM", "BA", "JNJ", "BLK", "VMW"]
#    multiple(m1, title="Other")
#
#    print ("{} days ago was : {} \tLatest {}".format(start, dates[-1*start], dates[-1]))
#    z.setp(getDropScore.cache, "newdropcache")

#    table_print.initiate()

