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

def getInputTarget():
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = pandas.read_csv("{}/raw/GOOG.csv".format(os.getcwd()))
    data.drop(columns = ["Date", "Adj Close"], inplace=True)
    data = scaler.fit_transform(data)
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    test = data[~msk]
    
    input_example = train[:-1]
    target_example = train[1:]
    return input_example, target_example

#for input_example, target_example in  dataset.take(1):
#    print ('Input data: ', repr(''.join(idx2char[input_example.numpy()])))
#    print ('Target data:', repr(''.join(idx2char[target_example.numpy()])))

#print (norm(data["Open"].tolist()))

#stocks = []
#for holding in holdings:

#util.process(getStocks("IWB"), "all")
#util.process2(getStocks("IWB"), "all")
#percent_list = util.process2(getEtfList(), "etfs")
