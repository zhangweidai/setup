import util

util.getStocks.totalOverride = True
util.getCsv.csvdir = "historical"

stocks = util.getStocks()
stocks.reverse()
for astock in stocks:
    try:
        util.saveProcessedFromYahoo(astock)
    except Exception as e:
        z.trace(e)
        print ("problem with {}".format(astock))
        continue
removed = util.getRemovedStocks()
util.setp(removed, "removedstocks")
