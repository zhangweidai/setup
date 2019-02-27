from datetime import date, timedelta
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import pandas
import mine

#main()
yf.pdr_override()
startdate = date.today() - timedelta(days=4)

def getDataFromYahoo(astock):
    data = None
    try:
        data = pdr.get_data_yahoo([astock], start=startdate.isoformat(), end=date.today().isoformat())
    except Exception as e:
        print (str(e))
        return None
    
    data.drop(columns = ["Adj Close", "Volume"], inplace=True)
    
    for idx,row in data.iterrows():
        for label in ["Open", "Close", "High", "Low"]:
            data.at[idx, label] = round(data.at[idx, label], 3)

    return data

def updateCsv(astock):
    path = "{}/all/{}.csv".format(os.getcwd(), astock)
    loaded = None
    if os.path.exists(path):
        loaded = pandas.read_csv(path)
    else:
        return

    lastdate = loaded.tail(1)["Date"].item()
    data = getDataFromYahoo(astock)
    if data is None:
        return

    appending = False
    for idx,row in data.iterrows():
        cdate = str(idx.to_pydatetime()).split(" ")[0]

        if appending:
            with open(path, "a") as f:
                opend = data.at[idx, "Open"]
                high = data.at[idx, "High"]
                low = data.at[idx, "Low"]
                closed = data.at[idx, "Close"]
                f.write("{},{},{},{},{}\n".format(cdate, opend, high, low, closed))
            
        if cdate == lastdate:
            appending = True
import stock_analyze
stocks = stock_analyze.getStocks("IVV")
#stocks = ["C"]
for astock in stocks:
    updateCsv(astock)

