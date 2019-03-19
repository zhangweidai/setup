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

import util
import os
def standard():
    path = util.getPath("analysis")
    cmd = "find {} | grep strategy_files_ | xargs rm -rf".format(path)
    os.system(cmd)
    #        )
    stocks = util.getStocks()
    ranges = getRanges(util.getNumberOfDates())
    for vals in ranges:
        util.writeStrategyReport(stocks, start=vals[0], end=vals[1])

def historical():
    path = util.getPath("history")
    cmd = "find {} | grep history_ | xargs rm -rf".format(path)
    os.system(cmd)

    util.getStocks.totalOverride = True
    util.saveProcessedFromYahoo.download = False
    stocks = util.getStocks()
    ranges = getRanges(util.getNumberOfDates(), forHistory = True)
    grouping = 0
    for i,vals in enumerate(ranges):
        if i % 15 == 0:
            grouping += 1

        if grouping == 1:
            continue

        util.writeStrategyReport(stocks, start=vals[0], end=vals[1],
                                reportname = "history_{}_".format(grouping),
                                reportdir = "history")

historical()
