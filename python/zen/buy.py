import z
import csv
from collections import defaultdict
import table_print
import statistics
import os

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



def getMCDiv(astock):
    try:
        return getMCDiv.dic[astock]
    except:
        try:
            getMCDiv.dic = z.getp("mcdivdict")
            return getMCDiv.dic[astock]
        except:
            pass
    return ["NA", "NA"]

def getMCRank(astock):
    try:
        return getMCDiv(astock)[1]
    except:
        return "NA"


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

def getRows(astock, date):
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
        one, two, three = getYearly2.dic[astock]
        return z.percentage(one), z.percentage(two), three
    except:
        getYearly2.dic = z.getp("annuals")
        try:
            one, two, three = getYearly2.dic[astock]
            return z.percentage(one), z.percentage(two), three
        except:
            return "NA", "NA", "NA"
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

#print (getPrice("KO", "2019-01-09"))
#
#exit()
HIGHEST = 10000
def single(value, avgOneYear):
    global torys

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
    for i, row in enumerate(getRows(astock, dates[-1*start])):
        c_open = float(row['Open'])
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

        seen.append(c_close)
        if len(seen) >= daysAgo5:
            daysAgoValue = seen[i-daysAgo5]
            change5 = c_close/daysAgoValue
            avg5Change.append(change5)
            if change5 < 1:
                mins.append(change5)

    y1w2, y1m2, y1l = getYearly2(astock)

    if y1l != "NA":
        avgOneYear.append(y1l)
        y1l = z.percentage(y1l)

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
        ("d17_45", d17_45),
        ("d18_64", d18_64),
        ("mc", mc),
        ("div", div),
        ("y1w", y1w2),
        ("y1m", y1m2),
        ("y1l", y1l),
        ("probdown", getLongProbDown(astock)),
        ("MeanDrop", mindrop),
        ("MaxDrop", maxdrop),
        ("Owned", portFolioValue(astock)),
        ("Orders", orderstr),
        ("OrderChange", orderchange)
        ]

    if args.live:
        values.append(("Last", (c_close/prev_close)))

    table_print.store(values)
    table_print.use_percentages = ["avg5", "min5", "last5", fromtop, lastchange, fromtopgain, "OrderChange"]

    if args.live:
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
        try:
            single(value, avgOneYear)
        except Exception as e:
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

    portFolioValue.dict = z.getp("ports")
    companies = z.getp("company")
    orders = z.getp("orders")
    torys = z.getp("torys")

#    myportlist = z.getp("myportlist")
    getDropScore.cache = z.getp("newdropcache")
    if getDropScore.cache is None:
        getDropScore.cache = defaultdict(dict)
    getDropScore.cache = defaultdict(dict)

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default="default")
    parser.add_argument('--live', default=False)

    args = parser.parse_args()

    z.online.online = args.live

    if args.mode == "owned":
        multiple(portFolioValue.dict.keys(), "owned")
        z.setp(problems, "problems")
        exit()

    if "order" in args.mode:
        multiple(orders.keys(), title = "Orders")
        exit()

    if "notes" in args.mode:
        multiple(['CLX', 'MTN', 'NOW', 'SGEN', 'TGT', "IBB"], title = "notes")
#
#        bar = list()
#        single("PLD",bar)
#        table_print.printTable()
#        table_print.clearTable()

        exit()

    if "mc" in args.mode:
        items = z.getp("mcsortedlist")
        multiple(items[:30], title = "MC1")
        multiple(items[30:60], title = "MC2")
        exit()

    try:
        multiple(z.getEtfList(forEtfs=True), title = "Standard ETFS")

        multiple("avg30c")
        multiple("best30c")
        multiple("worst30c")
    except:
        pass

    m1 = ["COST", "WMT", "NKE", "FB", "MSFT", "TGT", "BABA", "NFLX", "AMZN", "GOOG", "AMD", "ADBE", "DIS", "KO", "TSLA", "WM", "BA", "JNJ", "BLK"]
    multiple(m1, title="Other")

    try:
        multiple("gained_discount")
        multiple("low_high_sort")

        multiple(orders.keys(), title = "Orders")
        z.setp(problems, "problems")

#        multiple(portFolioValue.dict.keys(), "owned")
        from sortedcontainers import SortedSet
        print (SortedSet(portFolioValue.dict.keys()))
    except:
        pass

    print ("{} days ago was : {} \tLatest {}".format(start, dates[-1*start], dates[-1]))
    z.setp(getDropScore.cache, "newdropcache")

