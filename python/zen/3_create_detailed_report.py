from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import util 

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

def getVector(values, name, dividend):
    length = len(values)

    try:
        factor = util.getFactors(values)
    except:
        factor = 1

    score, dipScore = util.getScore(values)
    discount = util.getDiscount(values)
    combined = round(score/dipScore,4)
    final = round((combined / (discount*discount)) * factor, 4)

    dipScore = round(dipScore,3)
    score = round(score,3)

    return [final, combined, discount, dipScore, score, dividend, factor, length, name]

def writeDropCsv(stocks, directory = "all"):
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
        percent_list[astock] = getVector(values, dividend, name)

    util.writeFile(percent_list, ["Final", "Score(Reg/Dip)", "Discount", "Dip", "Reg", "Name", "Factor", "Length", "Dividend"], directory, name = "regular_report")

writeDropCsv(util.getStocks("IVV", dev = True, andEtfs = True), directory = "analysis")
#writeMinimizedReport(util.getStocks("IVV", andEtfs = True), directory = "analysis")
#writeMinimizedReport(util.getStocks("IVV", andEtfs = True))
