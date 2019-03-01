from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import datetime
import fnmatch

doonce = True

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





