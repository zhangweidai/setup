import z
import csv
from collections import defaultdict
import table_print
import statistics
import os
from sortedcontainers import SortedSet
# mc 30.00B to 1.54T
# mc 7.5B to 30.00B 
# mc 2.7B to 7.5B
# mc 0 to 2.7B 


#start = 37
start = 107
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
        return getLongProbDown.dic[astock]
    except:
        try:
            getLongProbDown.dic = z.getp("prob_down")
            return getLongProbDown.dic[astock]
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
    return ["NA", 3999]

def getMCRank(astock):
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
    sortedSetToRankDict("voldic", sset, reverse=True)
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

def getFiles(astock, date = "2000"):
#    yield z.getPath("historical/{}.csv".format(astock))
#    return
    added = False
    for year in getYears(date):
        apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
        if os.path.exists(apath):
            added = True
            yield apath

    if not added:
        apath = z.getPath("historical/{}.csv".format(astock))
        print("apath : {}".format( apath ))
        if os.path.exists(apath):
            yield apath

def getYears(date):
    away_year = int(date.split("-")[0])
    dates = z.getp("dates")
    date_away = dates[-1]
    now_year = int(date_away.split("-")[0])
    while int(away_year)  != now_year:
        yield away_year
        away_year += 1
    yield away_year

def getRows(astock, date = "2000"):
    date_year = date.split("-")[0]
    for apath in getFiles(astock, date):

        started = False
        for row in csv.DictReader(open(apath)):
            if date_year not in apath:
                yield row
            elif started:
                yield row
            elif row['Date'] == date:
                started = True
                yield row

def updateDates():
    dates = z.getp("dates")
    new = list()
    for row in getRows("IVV", dates[0]):
        new.append(row['Date'])
    z.setp(new, "dates")

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
    ret = "{}{}".format(dayone, z.percentage(round(minc,4)))
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

def getYearly2(astock):
    try:
        one, two, three, four = getYearly2.dic[astock]
        return z.percentage(one), z.percentage(two), three, four
    except:
        getYearly2.dic = z.getp("annuals")
        try:
            one, two, three, four = getYearly2.dic[astock]
            return z.percentage(one), z.percentage(two), three, four
        except:
            return "NA", "NA", "NA", "NA"
getYearly2.dic = None

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
    return orders[astock][0]

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
    return round(100-(100/(1+ (m1/m2))),1)



#print (getPrice("KO", "2019-01-09"))
#
#exit()
HIGHEST = 10000
dict2 = None
def single(value, avgOneYear):
    global torys, mine, tory, prob_discount, dict2

    if type(value) is tuple:
        astock = value[1]
    else:
        astock = value

    seen = list()
    daysAgo5 = 5
    avg5Change = list()
    firstPrice = None
    values = list()
    lowFromHigh = HIGHEST
    high = 0
    mins = list()
    c_close = None
    rup = list()
    rdown = list()
    prev = None

    for i, row in enumerate(getRows(astock, dates[-1*start])):
        try:
            c_open = float(row['Open'])
        except:
            return

        if not firstPrice:
            firstPrice = c_open
        c_close = float(row[z.closekey])

        if i < start - 10:
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

        if i > start - 13:
            change = round(c_close/prev,5)
            if change > 1.0:
                rup.append(change)
            else:
                rdown.append(change)

        prev = c_close

        seen.append(c_close)
        if len(seen) >= daysAgo5:
            daysAgoValue = seen[i-daysAgo5]
            change5 = c_close/daysAgoValue
            avg5Change.append(change5)
            if change5 < 1:
                mins.append(change5)

    if not c_close:
        return

    rsi = getRsi(rup, rdown)

    y1w2, y1m2, y1l, y1l2 = getYearly2(astock)

    if y1l != "NA":
        avgOneYear.append(y1l)
        y1l = z.percentage(y1l)

    if y1l2 != "NA":
        y1l2 = z.percentage(y1l2)

    mc = "NA"
    try:
        both = getMCDiv(astock)
        mc = both[1]
        div = round(both[0]*100,3)
    except:
        div = "NA"

    prev_close = c_close
    if args.live:
        try:
            live = util.getLiveData(astock, key = "price")
            if not live:
                print("NO LIVE astock: {}".format( astock))
            c_close = live if live else c_close
        except Exception as e:
            z.trace(e)
            exit()

    mindrop = "NA"
    maxdrop = "NA"
    if mins:
        mindrop = round(statistics.mean(mins) * c_close,2)
        maxdrop = round(min(mins) * c_close,2)

    d13_30 = getDropScore(astock, "2013-03-19", 30)
    d17_45 = getDropScore(astock, "2017-05-25", 45)
    d18_64 = getDropScore(astock, "2018-07-11", 64)

    lastchange = "{}chg".format(start)
    fromtop = "{}drop".format(start)
    fromtopgain = "{}gain".format(start)
    try:
        name = companies[astock][0][0:17]
    except:
        name = ""
        
    order = getOrder(astock)
    orderstr = ""
    orderchange = 0
    if order != "NA":
        orderstr = round(order[0])
        orderchange = order[1]/c_close
        if astock in torys:
            name += "_T"
    if astock in mine:
        name = "(m)" + name
    if astock in tory:
        name = "(t)" + name

    try:
        disc = prob_discount[astock] 
    except:
        disc = ""

    try:
        y1wm2 = round(dict2[astock],2)
    except:
        y1wm2 = "NA"

    try:
        volr = single.voldic[astock]
    except:
        try:
            single.voldic = z.getp("voldic")
            volr = single.voldic[astock]
        except:
            volr = "NA"

    values = [
        ("Stock", inPortfolio(astock)),
        ("Name", name),
        ("Price", c_close),
        ("avg5", z.avg(avg5Change)),
        ("min5", min(avg5Change)),
        ("last5", avg5Change[-1]),
        (lastchange, (c_close/firstPrice)),
        (fromtop, (lowFromHigh/high)),
        (fromtopgain, (c_close/lowFromHigh)),
        ("d13_30", d13_30),
        ("d18_64", d18_64),
        ("rsi", rsi),
        ("rsiid", getFrom("rsi_indicator_dic", astock)),
        ("fcf", getFrom("fcfdic", astock)),
        ("mc", getFrom("latestmc", astock, "")),
        ("volr", volr),
        ("div", div),
        ("y1w", y1w2),
        ("y1m", y1m2),
        ("y1l2", y1l2),
        ("y1l", y1l),
        ("probup", getLongProbDown(astock)),
        ("discount", disc),
        ("MeanDrop", mindrop),
        ("MaxDrop", maxdrop),
        ("Owned", portFolioValue(astock)),
        ("Orders", orderstr),
        ("OrderChange", orderchange)
        ]

    if args.live:
        values.append(("Last", (c_close/prev_close)))
    else:
        values.append(("Last", (c_close/seen[-2])))

    table_print.store(values)
    table_print.use_percentages = ["avg5", "min5", "last5", fromtop, lastchange, fromtopgain, "OrderChange"]

#    if args.live:
    table_print.use_percentages.append("Last")

#single("IVV")
#exit()

problems = set()
def multiple(stocks, title = None):
    global problems

    if type(stocks) is str:
        if not title:
            title = stocks
        stocks = z.getp(stocks)

    avgOneYear = list()
    for idx, value in enumerate(stocks):
        if args.helpers:
            if type(value) is tuple:
                astock = value[1]
            else:
                astock = value
            if not astock.startswith(args.helpers):
                continue

        try:
            single(value, avgOneYear)
        except Exception as e:
            z.trace(e)
            if type(value) is tuple:
                astock = value[1]
            else:
                astock = value
            problems.add(astock)
            continue

    table_print.printTable(title)
    table_print.clearTable()

    try:
        yearone = z.avgp(avgOneYear)
    except:
        yearone = "NA"
    print ("Annual Change {}".format(yearone))
    print ("Problems {}".format(", ".join(problems)))

args = None
import util
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default="default")
    parser.add_argument('--live', default=False)
    parser.add_argument('helpers', type=str, nargs='?', default = [])
    args = parser.parse_args()
    savedhelper = None
    if args.helpers:
        savedhelper = args.helpers
        args.helpers = args.helpers[0].upper()

    portFolioValue.dict = z.getp("ports")
    companies = z.getp("company")
    orders = z.getp("orders")
    torys = z.getp("torys")
    tory = z.getp("tory")
    mine = z.getp("mine")
    prob_discount = z.getp("prob_down_5_10")
    dict2 = z.getp("y1wm2");
    getDropScore.cache = z.getp("newdropcache")
    if getDropScore.cache is None:
        getDropScore.cache = defaultdict(dict)
    getDropScore.cache = defaultdict(dict)

    z.online.online = args.live

    if args.mode == "special":
#        setVolRankDict()
#        multiple("y1wm2_big")
#        multiple("y1wm2_small")

        multiple("worst_smallcalp")
        multiple("best_smallcalp")
#        multiple("y1l2_big")
#        multiple("y1l2_small")
        table_print.initiate()
        exit()

    if args.mode == "single":
        multiple([savedhelper.upper()], "single")
#        table_print.initiate()
        exit()

    if args.mode == "owned":
        multiple(portFolioValue.dict.keys(), "owned")
        z.setp(problems, "problems")
        table_print.initiate()
        exit()

    if "order" in args.mode:
        multiple(orders.keys(), title = "Orders")
#        table_print.initiate()
        exit()

    if "benchmark" in args.mode:
        multiple(z.getEtfList(forEtfs=True), title = "Standard ETFS")
        table_print.initiate()
        exit()

    if "rand" in args.mode:
        bar = z.getp("listofstocks")
        import random
        multiple([bar[random.randint(1,len(bar))] for b in range(0,10)])
        table_print.initiate()
        exit()
        
    if "notes" in args.mode:
#        multiple(['NVMI', 'CASS', 'SP', 'RILY', 'GTY', "CKH", "CMCO", "CNXN", "BFS", "WMK", "KOP", "CENT", "LORL", "TTEC", "MTSC"], title = "fidelity_s1")
#        multiple(['ADES', 'MNLO', 'QTRX', 'REGI', 'SRRK'])
        multiple(['DHI'])
#        multiple(['CLX', 'MTN', 'NOW', 'SGEN', 'TGT', "IBB", "IDA", "IGM", "IHI", "MTUM", "PEP", "PLCE"], title = "notes")
#        multiple("newstuff")
#        multiple("probs_added_up")
#        table_print.initiate()
        exit()

    if "mc" in args.mode:
        wlp_sorted_mc = z.getp("wlp_sorted_mc")
        items = wlp_sorted_mc[dates[-252]]
        items = sorted(items, reverse=True)
        multiple(items[:30], title = "MC1")
        multiple(items[30:60], title = "MC2")
        multiple(items[210:240], title = "MC1")
        multiple(items[240:270], title = "MC2")
        multiple(items[270:300], title = "MC3")
        table_print.initiate()
        exit()

    try:
        multiple(z.getEtfList(forEtfs=True), title = "Standard ETFS")

        multiple("avg30c")
        multiple("best30c")
        multiple("worst30c")
    except:
        pass

    m1 = ["COST", "WMT", "NKE", "FB", "MSFT", "TGT", "BABA", "NFLX", "AMZN", "GOOG", "AMD", "ADBE", "DIS", "KO", "TSLA", "WM", "BA", "JNJ", "BLK", "VMW"]
    multiple(m1, title="Other")

    try:
        multiple("gained_discount")
        multiple("low_high_sort")

        multiple(orders.keys(), title = "Orders")
        z.setp(problems, "problems")

#        multiple(portFolioValue.dict.keys(), "owned")
        print (SortedSet(portFolioValue.dict.keys()))
    except:
        pass

    print ("{} days ago was : {} \tLatest {}".format(start, dates[-1*start], dates[-1]))
    z.setp(getDropScore.cache, "newdropcache")

    table_print.initiate()

