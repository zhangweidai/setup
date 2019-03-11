def getRanges(count):
    ret = []
    minimum = 30
    minrequired = 200
    i = 1
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

stocks = util.getStocks()
ranges = getRanges(util.getNumberOfDates())
for vals in ranges:
    util.loadUSMV_dict(start=vals[0], end=vals[1])
    util.writeStrategyReport(stocks, start=vals[0], end=vals[1])
    break
