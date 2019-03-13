import util 

end = util.getNumberOfDates()
start = end - 201
vals = [start, end]
stocks = util.getStocks()
util.loadUSMV_dict(start=vals[0], end=vals[1])
util.writeStrategyReport(stocks, start=vals[0], end=vals[1], "main_")
