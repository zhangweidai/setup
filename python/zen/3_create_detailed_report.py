import util 

util.saveProcessedFromYahoo.download = False
end = util.getNumberOfDates()
start = end - 201
vals = [start, end]
stocks = util.getStocks()
util.report(stocks, start=vals[0], end=vals[1], reportname = "main_")
