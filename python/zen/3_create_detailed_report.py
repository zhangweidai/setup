from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import math
import os
import util 
import scipy 

stocks = ["GOOG"]
directory = "all"

def getVector(values, dividend, name, astock, last):
    score, dipScore = util.getScore(values)
    discount = util.getDiscount(values)
    distrange, vari = util.getRangedDist(values)
    dipScore = round(dipScore,3)

    pointsabove = 0
    pointsbelow = 0
    if not astock == "USMV":
        pointsabove, pointsbelow = util.getPointsAbove(values)

    changes = util.getChanges(values)
    factor = "NotEnoughData"
    fd = 1
    if changes:
        factor = round(np.prod(changes),3)
        fd = round(float(factor)/float(discount), 3)

#    discount = util.formatDecimal(discount)

    new = round((((pointsabove-(pointsbelow/3.1415))* fd)/dipScore) + 
            math.sqrt(score), 3)

    wc, probup, wcb = util.getWC(values)
#    for i,b in enumerate(changes):
#        changes[i] = util.formatDecimal(b)

    target = util.getTargetPrice(astock)

    if name in sub:
        name = name + "*"

    return [name, new, discount, dipScore, target, last, dividend, 
    distrange, vari, pointsabove, pointsbelow, wc, probup, wcb] + changes

port = dict()
def writeDropCsv(stocks, directory = "analysis"):
    global sub
    util.loadUSMV_dict()

    name_idx = 1
    etfs = util.getFromHoldings()

    #global percent_list, notinvested
    percent_list = {}
    json_dict = util.getData("gg_json")
    if json_dict is None:
        return

    port = util.getPortfolio()
    portkeys = port.keys()
    for astock in stocks:

        path = util.getPath("csv/{}.csv".format(astock))
        try:
            df = pandas.read_csv(path)
        except:
            try:
                df = util.saveProcessedFromYahoo(astock)
            except:
                continue

        values = df['Avg'].tolist()
        last = df['Close'].iloc[-1]

#        values = values[:-46]

        dividend = util.getDividend(astock, values[-1], json_dict)

        try:
            name = json_dict[astock][name_idx]
        except:
            name = ""
            if astock in etfs:
                name = "ETF"

        if astock in portkeys:
            value = round(port[astock] * float(last),3)
            port[astock] = [name, value]

        percent_list[astock] = getVector(values, dividend, name, astock, last)

    headers = ["Name", "Score", "Discount", "Dip", 
               "Target", "Last", "Dividend", "DistRange", "Variance", 
               "PointsAbove", "PointsBelow", "WC", 
               "ProbUp", "WCBad", 
               "3", "6", "12", "24", "48", "96", "192", "384"]
    
    util.writeDict(port, "Portfolio")
    util.writeFile(percent_list, headers, directory, name = "main_report")

stocks = util.getStocks()
sub = util.getIVVStocks()
writeDropCsv(stocks)
#writeMinimizedReport(util.getStocks("IVV", andEtfs = True), directory = "analysis")
#writeMinimizedReport(util.getStocks("IVV", andEtfs = True))
