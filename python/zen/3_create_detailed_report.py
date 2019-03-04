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

def getVector(values, dividend, name, astock):
    length = len(values)

#    try:
#        factor = util.getFactors(values)
#    except:
#        factor = 1

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

    wc, probup = util.getWC(values)
#    for i,b in enumerate(changes):
#        changes[i] = util.formatDecimal(b)

    return [name, new, discount, dipScore, factor, length, dividend, 
    distrange, vari, fd, pointsabove, pointsbelow, wc, probup] + changes

def writeDropCsv(stocks, directory = "analysis"):
    util.setBaselineScores()

    name_idx = 1
    etfs = util.getFromHoldings()

    #global percent_list, notinvested
    percent_list = {}
    json_dict = util.getData("gg_json")
    if json_dict is None:
        return

    for astock in stocks:
        path = util.getPath("csv/{}.csv".format(astock))

        df = pandas.read_csv(path)
        values = df['Avg'].tolist()

        dividend = util.getDividend(astock, values[-1], json_dict)

        try:
            name = json_dict[astock][name_idx]
        except:
            name = ""
            if astock in etfs:
                name = "ETF"

        percent_list[astock] = getVector(values, dividend, name, astock)

    headers = ["Name", "Score", "Discount", "Dip", 
               "Factor", "Length", "Dividend", "DistRange", "Variance", 
               "Factor/Discount", "PointsAbove", "PointsBelow", "WC", "ProbUp",
               "3", "6", "12", "24", "48", "96", "192", "384"]

    util.writeFile(percent_list, headers, directory, name = "main_report")

writeDropCsv(util.getStocks("IVV", andEtfs = True))
#writeMinimizedReport(util.getStocks("IVV", andEtfs = True), directory = "analysis")
#writeMinimizedReport(util.getStocks("IVV", andEtfs = True))
