from datetime import date, timedelta
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import pandas
import util
import time

#main()
yf.pdr_override()
startdate = date.today() - timedelta(days=6)
today = date.today().isoformat()

def getDataFromYahoo(astock):
    data = None
    try:
        data = pdr.get_data_yahoo([astock], 
                                  start=str(startdate.isoformat()), 
                                  end=str(date.today().isoformat()))
    except Exception as e:
        try:
            data = pdr.get_data_yahoo([astock], 
                                      start=str(startdate.isoformat()), 
                                      end=str(date.today().isoformat()))
        except Exception as e:
            print (str(e))
            raise SystemExit
            return None
    
    for idx,row in data.iterrows():
        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            data.at[idx, label] = round(data.at[idx, label], 3)

    return data

pulled = False
#latest = util.getp("lastValues")
latest = dict()
problem = []
def updateCsv(astock, yahoo_date):
    global pulled, latest, problem
    loaded = None

    path = util.getPath("csv/{}.csv".format(astock))
    if not os.path.exists(path):
        util.saveProcessedFromYahoo(astock)
        pulled = True
        return

    loaded = pandas.read_csv(path)
    lastdate = loaded.tail(1)["Date"].item()
    if lastdate == yahoo_date:
        return

    data = getDataFromYahoo(astock)
    if data is None:
        problem.append(astock)
        print (astock)
        return

#    latest[astock] = loaded.tail(1)["Close"].item()
#    return
    appending = False
    for idx,row in data.iterrows():
        cdate = str(idx.to_pydatetime()).split(" ")[0]

        if appending:
            with open(path, "a") as f:
                opend = data.at[idx, "Open"]
                high = data.at[idx, "High"]
                low = data.at[idx, "Low"]
                closed = data.at[idx, "Close"]
                adj = data.at[idx, "Adj Close"]
                vol = data.at[idx, "Volume"]
                f.write("{},{},{},{},{},{},{}\n".format(cdate, 
                            opend, high, low, 
                            closed, adj, vol))
                latest[astock] = closed
            
        if cdate == lastdate:
            appending = True

def updateStocks(yahoo_date):
    stocks = util.getStocks()
    for astock in stocks:
        updateCsv(astock, yahoo_date)
    util.setp(latest, "lastValues")
    util.setp(problem, "problematicUpdateStocks")
    print (problem)


#if pulled:
#    util.saveJsonData(stocks, "ijh")

