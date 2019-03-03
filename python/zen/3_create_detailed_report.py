from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import math
import os
import util 
import scipy 

#print (norm(data["Open"].tolist()))

#def getEtfList():
#    path = "{}/analysis/ETFList.csv".format(os.getcwd())
#    data = pandas.read_csv(path)
#    return data['Symbol'].tolist()

#util.process(getEtfList())
#raise SystemError

#stocks = getStocks("IWB")
stocks = ["GOOG"]
directory = "all"

def getVector(values, dividend, name, astock):
    length = len(values)

    try:
        factor = util.getFactors(values)
    except:
        factor = 1

    score, dipScore = util.getScore(values)
    discount = util.getDiscount(values)
    distrange, vari = util.getRangedDist(values)

    combined = round(score/dipScore,4)
    final = round((combined / (discount*discount)) * factor, 4)

    dipScore = round(dipScore,3)
    score = round(score,3)

    pointsabove = 0
    pointsbelow = 0
    if not astock == "USMV":
        pointsabove, pointsbelow = util.getPointsAbove(values)

    fd = round(factor/discount, 3)
    new = round((((pointsabove-(pointsbelow/3.1415))*(1+(dividend/2))* fd)/dipScore) + math.sqrt(score), 3)

    return [final, combined, discount, dipScore, score, name, factor, length, dividend, 
    distrange, vari, fd, pointsabove, pointsbelow, new]

def writeDropCsv(stocks, directory):
    util.setBaselineScores()

    name_idx = 1
    dividend_idx = 0
    etfs = util.getFromHoldings()

    #global percent_list, notinvested
    percent_list = {}
    json_dict = util.getData("gg_json")
    if json_dict is None:
        return

    for astock in stocks:
        path = "{}/../new/{}.csv".format(os.getcwd(), astock)

        try:
            dividend = 10*json_dict[astock][dividend_idx]
        except:
            dividend = 0

        try:
            name = json_dict[astock][name_idx]
        except:
            name = ""
            if astock in etfs:
                name = "ETF"

        df = pandas.read_csv(path)
        values = df['Avg'].tolist()
        percent_list[astock] = getVector(values, dividend, name, astock)

    util.writeFile(percent_list, ["Final", "Score(Reg/Dip)", "Discount", "Dip", "Reg", "Name", "Factor", "Length", "Dividend", "DistRange", "Variance", "F/D", "PointsAbove", "PointsBelow", "NewScore"], directory, name = "regular_report")

writeDropCsv(util.getStocks("IVV", andEtfs = True), directory = "analysis")
#writeMinimizedReport(util.getStocks("IVV", andEtfs = True), directory = "analysis")
#writeMinimizedReport(util.getStocks("IVV", andEtfs = True))
