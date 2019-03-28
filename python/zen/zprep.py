from datetime import date, timedelta
import datetime
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import z
import pandas
import util
import time
from pandas_datareader import data as pdr
z.listen()

def setStockDays():
    df = z.getCsv("SPY")
    dates = df["Date"].tolist()
    z.setp(dates,"dates")

yf.pdr_override()
startdate = date.today() - timedelta(days=16)
def getDataFromYahoo(astock):
    data = None
    try:
        data = pdr.get_data_yahoo([astock], start=str(startdate.isoformat())) 
    except Exception as e:
        try:
            data = pdr.get_data_yahoo([astock], start=str(startdate.isoformat())) 
        except Exception as e:
            print (str(e))
            print("astock: {}".format( astock))
            return None
    
    for idx in data.index:
        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            data.at[idx, label] = round(data.at[idx, label], 3)
    return data

latest = dict()
downloaded = list()
notadded = list()
def updateCsv(astock):
    global latest
    path = z.getCsv(astock, asPath=True)
    if not os.path.exists(path):
        print("path: {}".format( path))
        util.saveProcessedFromYahoo(astock)
        downloaded.append(astock)
#        print("i didnt exist astock: {}".format( astock))
#        raise SystemExit
        return

    t = os.path.getmtime(path)
    csvdate = datetime.datetime.fromtimestamp(t)
    csvday = csvdate.day
    csvdate = str(csvdate).split(" ")[0]
    ttoday = datetime.date.today().day-1
    if csvday >= ttoday:
        return

    df = z.getCsv(astock)
    csvdate = df["Date"].tolist()[-1]

    data = getDataFromYahoo(astock)
    if data is None:
        print ("problem" + astock)
        raise SystemExit
        return

    appending = False
    added = False
    for idx in data.index:
        cdate = str(idx.to_pydatetime()).split(" ")[0]

        if appending:
            with open(path, "a") as f:
                added = True
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
            
        if str(cdate) == str(csvdate):
            appending = True

    if not added:
        print ("downloaded but did not add " + astock)
        notadded.append(astock)


def updateStocks():
    util.saveProcessedFromYahoo.download = True
#    stocks = z.getStocks()
    stocks = z.getStocks()
    for astock in stocks:
        try:
            updateCsv(astock)
        except Exception as e:
            print (str(e))
            raise SystemExit
            pass
#    z.setp(latest, "lastValues")

print("downloaded: {}".format( downloaded))
updateStocks()
print(notadded)
#setStockDays()


