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

def process2(stocks, directory = "stocks"):
    #global percent_list, notinvested
    percent_list = {}

    for astock in stocks:
        path = "{}/{}/{}.csv".format(os.getcwd(), directory, astock)
        if not os.path.exists(path):
            continue
    
        df = pandas.read_csv(path)
        losed = 0
        daysbought = 0
        maxlosed = 0
    
        invested = 0
        shares = 0
        countd_days = 0
        processed_day = 0
    
        buyOnOpen = False
        lastprice = 0
        lastpurchase_date = None
        high = 0
        low = 1000000
        start = None
        ldate = 0
        hdate = 0
        days_to_consider = 365
        lowest_date = None
        highest_date = None

        for idx, row in df.tail(days_to_consider).iterrows():
            if not start:
                start = round(float(df.at[idx, "Open"]), 4)
            chigh = round(float(df.at[idx, "High"]), 4)
            clow = round(float(df.at[idx, "Low"]),4)
            if chigh > high:
                high = chigh
                hdate = idx
                highest_date = df.at[idx, "Date"]
            if clow < low:
                low = clow
                ldate = idx
                lowest_date = df.at[idx, "Date"]
            lastprice = round(float(df.at[idx, "Close"]),4)

        if ldate < hdate:
            hdate = 0
            for idx, row in df.tail(days_to_consider).iterrows():
                chigh = round(float(df.at[idx, "High"]),4)
                clow = round(float(df.at[idx, "Low"]),4)
                if chigh > high and idx < ldate:
                    high = chigh
                    hdate = idx
                    highest_date = df.at[idx, "Date"]

        if not low or not high or not start:
            continue

#        if hdate < ldate:
        try:
            drop = round(low/high,3)
            recover = round(lastprice/low, 3)
            total = round(lastprice/start,3)
        except:
            continue

        evaluation = (drop) * (2*(recover + total))

        dropTime = ldate - hdate
        percent_list[astock] = [start, high, low, lastprice, drop, recover, total, round(evaluation, 3), 
                                highest_date, 
                                lowest_date, 
                                dropTime] 

    df = pandas.DataFrame.from_dict(percent_list, orient = 'index', columns=["Start", "High", "Low", "Last", "Drop", "Recover", "TotalChange", "Score", "HighDate", "LowDate", "DropTime"])
    path = "{}/analysis/gg_365_drop.csv".format(os.getcwd(), directory)
    df.to_csv(path)


#for holding in holdings:

#util.process(getStocks("IWB"), "all")
#process2(["GOOG", "AAPL"], "all")

name_idx = 1
dividend_idx = 0
#etfs = util.getFromHoldings()
def writeDropCsv(stocks, directory = "all"):
    #global percent_list, notinvested
    percent_list = {}
    json_dict = util.getData("json_{}".format(directory))
    if json_dict is None:
        return

    for astock in stocks:
        path = "{}/{}/{}.csv".format(os.getcwd(), directory, astock)
        if not os.path.exists(path):
            continue

        try:
            dividend = 10*json_dict[astock][dividend_idx]
        except:
            dividend = 0

        try:
            name = json_dict[astock][name_idx]
        except:
            name = ""
#            if astock in etfs:
#                name = "ETF"

        df = pandas.read_csv(path)
        values = df['Open'].tolist()
        length = len(values)

        try:
            factor = util.getFactors(values)
        except:
            print ("Not enough data for {}".format(astock))
            continue

        score, dipScore = util.getScore(values)
        discount = util.getDiscount(values)
        combined = round(score/dipScore,4)
        final = round((combined / (discount*discount)) * factor, 4)

        dipScore = round(dipScore,3)
        score = round(score,3)
        percent_list[astock] = [final, combined, discount, dipScore, score, dividend, factor, length, name]

    util.writeFile(percent_list, ["Final", "Score(Reg/Dip)", "Discount", "Dip", "Reg", "Dividend", "Factor", "Length", "Name"], directory)

#writeDropCsv(["GOOG"], "all")
writeDropCsv(util.getStocks("IJH"), "ijh")
#process2(getStocks("IVV"), "all")
