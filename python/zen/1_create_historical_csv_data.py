import util

stocks = util.getStocks("IVV", andEtfs=True)
for astock in stocks:
    util.saveProcessedFromYahoo(astock)
