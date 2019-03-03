from datetime import date, timedelta
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import pandas
import util
import time

#main()
yf.pdr_override()
startdate = date.today() - timedelta(days=4)

def getDataFromYahoo(astock):
    data = None
    try:
        data = pdr.get_data_yahoo([astock], start=str(startdate.isoformat()), end=str(date.today().isoformat()))
    except Exception as e:
        print (str(e))
        return None
    
    data.drop(columns = ["Adj Close", "Volume"], inplace=True)
    
    for idx,row in data.iterrows():
        for label in ["Open", "Close", "High", "Low"]:
            data.at[idx, label] = round(data.at[idx, label], 3)

    return data

def updateCsv(astock, directory = "../new"):
    path = "{}/{}/{}.csv".format(os.getcwd(), directory, astock)
    data = None
    lines = None
    if os.path.exists(path):
        with open(path, "r") as f:
            lines = f.readlines()
    else:
        print ("Problem with" + astock)
        return
    path = "{}/../new/{}.csv".format(os.getcwd(), astock)
    print (path)
    with open(path, "w") as f:
        for aline in lines:
            linet = aline.split(",")
            date = linet[0]
            if (date == "Date"):
                f.write("{},Avg\n".format(aline.strip()))
                continue
                
            opend = linet[1]
            high = linet[2]
            low = linet[3]
            closed = linet[4].strip()
            avg = round((float(opend) + float(high) + 
                         float(low) + float(closed))/4, 4)

            f.write("{},{},{},{},{},{}\n".format(date, opend, high, 
                                                 low, closed, avg))
            
stocks = util.getStocks("IVV", andEtfs=True)
#stocks = util.getFromHoldings()
for astock in stocks:
    updateCsv(astock)

#if pulled:
#    util.saveJsonData(stocks, "ijh")

