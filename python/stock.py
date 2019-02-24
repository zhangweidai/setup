from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import mine

import numpy as np
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler

def norm(x):
    return x / np.linalg.norm(x)

scaler = MinMaxScaler(feature_range=(0, 1))
data = pandas.read_csv("{}/raw/GOOG.csv".format(os.getcwd()))
data.drop(columns = ["Date", "Adj Close"], inplace=True)
data = scaler.fit_transform(data)
msk = np.random.rand(len(data)) < 0.8
train = data[msk]
test = data[~msk]
print (test)
#print (norm(data["Open"].tolist()))

def getEtfList():
    path = "{}/analysis/ETFList.csv".format(os.getcwd())
    data = pandas.read_csv(path)
    return data['Symbol'].tolist()

#mine.process(getEtfList())
#raise SystemError
def getStocks(holding):
    data = pandas.read_csv("{}/holdings/{}_holdings.csv".format(os.getcwd(), holding))
    return data['Ticker'].tolist()

#stocks = []
#for holding in holdings:

#mine.process(getStocks("IWB"), "all")
#mine.process2(getStocks("IWB"), "all")
#percent_list = mine.process2(getEtfList(), "etfs")
