import util

stocks = util.getStocks("IVV", andEtfs=True)
for astock in stocks:
    try:
        util.saveProcessedFromYahoo(astock)
    except Exception as e:
        print (str(e))
        print ("problem with {}".format(astock))
        continue
