import util 

util.loadUSMV_dict()
stocks = util.getStocks()
util.writeDropCsv(stocks)
