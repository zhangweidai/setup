import util

stocks = util.getStocks(ivv=True)
for astock in stocks:
    try:
        util.saveProcessedFromYahoo(astock, csvdir="historical")
    except Exception as e:
        print (str(e))
        print ("problem with {}".format(astock))
        continue
removed = util.getRemovedStocks()
util.setp(removed, "removedstocks")
