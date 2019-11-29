import z
import csv
from collections import defaultdict
import table_print
import statistics
import os

start = 57
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

def getFiles(astock, date):
#    yield z.getPath("historical/{}.csv".format(astock))
#    return
    for year in getYears(date):
        yield z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))

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

        if not os.path.exists(apath):
            continue

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
    for i, row in enumerate(getRows(astock, startd)):
        c_open = float(row['Open'])
        c_close = float(row[z.closekey])

        seen.append(c_close)
        if len(seen) >= length:
            daysAgoValue = seen[i-length]
            change5 = c_close/daysAgoValue
            changes.append(change5)

    minc = min(changes)
    getDropScore.cache[astock][startd] = round(minc,4)
    return minc

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

def getYearly(astock):
    try:
        one, two = getYearly.dic[astock]
        return z.percentage(one), z.percentage(two)
    except:
        getYearly.dic = z.getp("yearlydic")
        try:
            one, two = getYearly.dic[astock]
            return z.percentage(one), z.percentage(two)
        except:
            return "NA", "NA"
getYearly.dic = None
def inPortfolio(astock):
    try:
        if astock in myportlist:
            return "*{}".format(astock)
    except:
        pass
    return astock
#print (getPrice("KO", "2019-01-09"))
#
#exit()
HIGHEST = 10000
def single(value, avgOneYear):

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
    for i, row in enumerate(getRows(astock, dates[-1*start])):
        c_open = float(row['Open'])
        if not firstPrice:
            firstPrice = c_open
        c_close = float(row[z.closekey])

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

#    y1w, y1m = getYearly(astock)
#    y1l = getLastYearChange(astock)

    y1w2, y1m2, y1l = getYearly2(astock)

    if y1l != "NA":
        avgOneYear.append(y1l)
        y1l = z.percentage(y1l)
#
#    try:
#        beta, pe, mcchg, div = getChangeStats(astock)
#        div = round(div,3)
#    except Exception as e:
#        beta, pe, mcchg, div = None, None, None, None
#        div = " NA"

    try:
        both = getMCDiv(astock)
        mc = both[1]
        div = both[0]
    except:
        mc = "NA"
        div = "NA"

    mindrop = round(statistics.mean(mins) * c_close,2)
    maxdrop = round(min(mins) * c_close,2)

    d13_30, around = getDropScore(astock, "2013-03-19", 30)
    d17_45, around = getDropScore(astock, "2017-05-25", 45)
    d18_64, around = getDropScore(astock, "2018-07-11", 64)

    values = [
        ("Stock", inPortfolio(astock)),
        ("Price", c_close),
        ("avg5", z.avgp(avg5Change)),
        ("min5", z.percentage(min(avg5Change))),
        ("last5", z.percentage(avg5Change[-1])),
        ("{}chg".format(start), z.percentage((c_close/firstPrice))),
        ("FromHigh", z.percentage((lowFromHigh/high))),
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
        ("MaxDrop", maxdrop)
        ]
    table_print.store(values)

#single("IVV")
#exit()

def multiple(stocks, title = None):

    if type(stocks) is str:
        if not title:
            title = stocks
        stocks = z.getp(stocks)

    avgOneYear = list()
    for idx, value in enumerate(stocks):
        try:
            single(value, avgOneYear)
        except:
            continue

    print ("\n=== " , title , "===")
    table_print.printTable()
    table_print.clearTable()

    try:
        yearone = z.avgp(avgOneYear)
    except:
        yearone = "NA"
    print ("Annual Change {}".format(yearone))

if __name__ == '__main__':
    myportlist = z.getp("myportlist")
    getDropScore.cache = z.getp("newdropcache")
    if getDropScore.cache is None:
        getDropScore.cache = defaultdict(dict)

    multiple(z.getEtfList(forEtfs=True), title = "Standard ETFS")

    multiple("avg30c")
    multiple("best30c")
    multiple("worst30c")
#    multiple("ults30")
#    multiple("consv_ults30")
#    multiple("ultrank")
#    multiple("ultrank2")

    m1 = ["COST", "WMT", "NKE", "FB", "MSFT", "TGT", "BABA", "NFLX", "AMZN", "GOOG", "AMD", "ADBE", "DIS", "KO", "TSLA", "WM", "BA", "JNJ", "BLK"]
    multiple(m1, title="Other")

#    multiple("sortedvolmcbegin")
#
    multiple("gained_discount")
    multiple("low_high_sort")
#
#    multiple("worst30")

    print ("57 days ago was : {} \tLatest {}".format(dates[-1*start], dates[-1]))
    z.setp(getDropScore.cache, "newdropcache")

