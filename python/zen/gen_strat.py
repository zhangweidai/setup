import util
import pyutil

def getRanges(count, forHistory = False):
    ret = []
    minimum = 35
    minrequired = 250
    i = 3 if forHistory else 1
    last = (count % minimum)
    end = 0
    while ((i * minimum) + minrequired < count):
        start = ((i-1) * minimum) 
        
        end = ((i) * minimum) + minrequired
        ret.append([start, end])
        i += 1
    
    start = ((i-1) * minimum)
    tend = start + last + minrequired + minimum
    if tend <= count:
        ret.append([start, tend])
    else:
        ret[-1][-1] = count
    return ret

def standard():
    savedir = "foobar"
    fname = "filename_"
    pyutil.clearDir(savedir, fname)
    util.saveProcessedFromYahoo.download = False

    stocks = util.getStocks(dev=True)
    ranges = getRanges(util.getNumberOfDates())
    for vals in ranges:
        util.report(stocks, start=vals[0], end=vals[1],
            reportname = fname,
            reportdir = savedir)

def historical():
    where = "history"
    pyutil.clearDir(where, "{}_".format(where))

    util.getStocks.totalOverride = True
    stocks = util.getStocks()
    ranges = getRanges(util.getNumberOfDates(), forHistory = True)
    grouping = 0
    for i,vals in enumerate(ranges):
        if i % 15 == 0:
            grouping += 1

        if grouping <= 2:
            continue

        util.report(stocks, start=vals[0], end=vals[1],
                                reportname = "{}_{}_".format(where, grouping),
                                reportdir = where)
    return where
#historical()
