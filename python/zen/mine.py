from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import datetime

doonce = True
startdate = datetime.date.today() - datetime.timedelta(days=777)
def process(stocks, directory="stocks"):
    global doonce
    for astock in stocks:
        if not astock:
            continue
        path = "{}/{}/{}.csv".format(os.getcwd(), directory, astock)
        data = None
        print (path)
        if os.path.exists(path):
            data = pandas.read_csv(path)
        else:
            try:
                if doonce:
                    yf.pdr_override() # <== that's all it takes :-)
                    doonce = False
                data = pdr.get_data_yahoo([astock], start=startdate.isoformat(), end=datetime.date.today().isoformat())
            except:
                print ("problem downloading")
                continue
    
#        if not os.path.exists(path):
#            print ("could not save {}".format(path))
#            continue
    
        data.drop(columns = ["Adj Close", "Volume"], inplace=True)
    
        for idx,row in data.iterrows():
            for label in ["Open","Close", "High", "Low"]:
                data.at[idx, label] = round(data.at[idx, label], 4)
    
        path = "{}/{}/{}.csv".format(os.getcwd(), directory, astock)
        data.to_csv(path)

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
        for idx, row in df.iterrows():
            countd_days += 1
#            if countd_days < 1000 or countd_days > 2500:
#                continue
            processed_day += 1
            opend = int(df.at[idx, "Open"])
            closed = int(df.at[idx, "Close"])
            lastprice = closed
    
            if buyOnOpen:
                shares += 1
                invested += (opend + 10)
                lastpurchase_date = df.at[idx, "Date"]
    
            if opend > closed:
                losed += 1
            elif closed > opend:
                if losed > maxlosed:
                    maxlosed = losed
    #                print (df.at[idx, "Date"])
    
                losed = 0
                buyOnOpen = False
    
            if losed > 6:
                buyOnOpen = True
                daysbought += 1
    #            print (df.at[idx, "Date"])
    
#        datasize = len(df.index)
        datasize = processed_day
        #print ("len : {}".format(datasize))
#        print ("daysbought : {}".format(daysbought))
#        print ("maxlosed : {}".format(maxlosed))
#        print ("invested : {}".format(invested))
#        print ("shares : {}".format(shares))
    
        if not shares:
#            notinvested.append(astock)
            continue
            
#        print ("lastprice : {}".format(lastprice))
        curval = shares * lastprice
#        print ("currentValue : {}".format(curval))
        percentup = curval / invested
#        print ("percent up : {}".format(percentup))
    
        percent_list[astock] = [percentup, shares, datasize, maxlosed, invested, curval, lastpurchase_date]

    df = pandas.DataFrame.from_dict(percent_list, orient = 'index', columns=["Change", "Shares", "DataSize", "LoseStreak", "Invested", "CurrentValue", "LastPurchase"])
    path = "{}/analysis/6d_{}_last_purchase.csv".format(os.getcwd(), directory)
    df.to_csv(path)

