from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import mine

#print (norm(data["Open"].tolist()))

#def getEtfList():
#    path = "{}/analysis/ETFList.csv".format(os.getcwd())
#    data = pandas.read_csv(path)
#    return data['Symbol'].tolist()

#mine.process(getEtfList())
#raise SystemError
def getStocks(holding):
    data = pandas.read_csv("{}/holdings/{}_holdings.csv".format(os.getcwd(), holding))
    return data['Ticker'].tolist()

#stocks = getStocks("IWB")
stocks = ["GOOG"]
directory = "all"
    

def process2(stocks, directory = "stocks"):
    #global percent_list, notinvested
    percent_list = {}

    for astock in stocks:
        path = "{}/{}/_{}.csv".format(os.getcwd(), directory, astock)
        if not os.path.exists(path):
            continue
        print (path)
    
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
        low = 10000
        start = None
        ldate = 0
        hdate = 0
        for idx, row in df.tail(140).iterrows():
            countd_days += 1
#            if countd_days < 1000 or countd_days > 2500:
#                continue
            processed_day += 1
            opend = int(df.at[idx, "Open"])
            closed = int(df.at[idx, "Close"])
            if not start:
                start = opend
            lastprice = closed
            if opend > high:
                high = opend
                hdate = idx
            if closed > high:
                high = closed
                hdate = idx
            if opend < low:
                low = opend
                ldate = idx
            if closed < low:
                low = closed
                ldate = idx

        if low == 0:
            continue

        drop = 0
        if hdate < ldate:
            drop = round(low/high,3)
        else:
            drop = round(low/start,3)

        recover = round(lastprice/low, 3)
        total = round(lastprice/start,3)
        evaluation = (2 * drop) + recover + total
        percent_list[astock] = [start, high, low, lastprice, drop, recover, total, round(evaluation, 3)] 
#        else:
#            print ("need more logic for {}".format(astock))

    df = pandas.DataFrame.from_dict(percent_list, orient = 'index', columns=["Start", "High", "Low", "Last", "Drop", "Recover", "TotalChange", "Score"])
    path = "{}/analysis/analysis.csv".format(os.getcwd(), directory)
    df.to_csv(path)


#for holding in holdings:

#mine.process(getStocks("IWB"), "all")
process2(getStocks("IWB"), "all")
#percent_list = mine.process2(getEtfList(), "etfs")
