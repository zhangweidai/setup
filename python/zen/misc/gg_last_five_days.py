from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import util

import numpy as np
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler

def norm(x):
    return x / np.linalg.norm(x)

#scaler = MinMaxScaler(feature_range=(0, 1))
#data = pandas.read_csv("{}/raw/GOOG.csv".format(os.getcwd()))
#data.drop(columns = ["Date", "Adj Close"], inplace=True)
#data = scaler.fit_transform(data)
#msk = np.random.rand(len(data)) < 0.8
#train = data[msk]
#test = data[~msk]
#print (test)
#print (norm(data["Open"].tolist()))

def getEtfList():
    path = "{}/analysis/ETFList.csv".format(os.getcwd())
    data = pandas.read_csv(path)
    return data['Symbol'].tolist()

#util.process(getEtfList())
#raise SystemError

def process(stocks, directory = "all"):
    #global percent_list, notinvested
    percent_list = {}

    for astock in stocks:
        path = "{}/{}/{}.csv".format(os.getcwd(), directory, astock)
        if not os.path.exists(path):
            continue

        print (path)
        df = pandas.read_csv(path)
        raising = 0 
        down = 0 
        total = 0 

        start = 0 
        last = 0 
        for idx, row in df.tail(12).iterrows():
            opend = int(df.at[idx, "Open"])
            closed = int(df.at[idx, "Close"])
            if start == 0:
                start = opend
            last = closed

            total += 1
            if opend > closed:
                down += 1
            if closed > opend:
                raising += 1
        try:
            percent_list[astock] = [ round(down/total,3), round(raising/total,3), round(last/start,4) ] 
        except:
            pass

    df = pandas.DataFrame.from_dict(percent_list, orient = 'index', columns=["%Down", "%Up", "Change"])
    path = "{}/analysis/gg_trending.csv".format(os.getcwd())
    df.to_csv(path)

def getOtherData(stocks):
    for astock in stocks:
        path = "{}/{}/_{}.csv".format(os.getcwd(), directory, astock)
        if not os.path.exists(path):
            continue

        print (path)
        df = pandas.read_csv(path)


stocks = getStocks("IVV")
#getOtherData(stocks)
process(stocks)
#process(getStocks("IWB"), "all")
