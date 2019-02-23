from pandas_datareader import data as pdr

import fix_yahoo_finance as yf
import numpy as np
import pandas
import os


#holdings = ["IVV"]
#stocks = []
#for holding in holdings:
#    data = pandas.read_csv("{}/holdings/{}_holdings.csv".format(os.getcwd(), holding))
#    stocks = data['Ticker'].tolist()

doonce = True

stocks = ["GOOG"]
#print (data)
#
## download Panel
def process(stocks):
    global doonce
    for astock in stocks:
        if not astock:
            continue
        path = "{}/stocks/{}.csv".format(os.getcwd(), astock)
        data = None
        print (path)
        if os.path.exists(path):
            data = pandas.read_csv(path)
        else:
            try:
                if doonce:
                    yf.pdr_override() # <== that's all it takes :-)
                    doonce = False
                data = pdr.get_data_yahoo([astock], start="2007-01-01", end="2019-12-24")
                data.to_csv(path)
            except:
                print ("problem downloading")
                pass
    
        if not os.path.exists(path):
            print ("could not save {}".format(path))
            continue
    
        data.drop(columns = ["High", "Low", "Close", "Volume"], inplace=True)
    
        for idx,row in data.iterrows():
            for label in ["Open","Adj Close"]:
                data.at[idx, label] = int(round(data.at[idx, label]))
    
        path = "{}/stocks/_{}.csv".format(os.getcwd(), astock)
        data.to_csv(path)

for astock in stocks:
    path = "{}/stocks/_{}.csv".format(os.getcwd(), astock)
    df = pandas.read(path)
#    print df
