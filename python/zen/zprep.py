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
    csvmonth = csvdate.month
    ttoday = datetime.date.today().day
    tmonth = datetime.date.today().month
    if csvday >= ttoday and tmonth == csvmonth:
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


def updateHistory():
    util.saveProcessedFromYahoo.download = True
#    stocks = z.getStocks()
    stocks = z.getStocks()
    print("stocks : {}".format( len(stocks) ))
    for astock in stocks:
        try:
            updateCsv(astock)
        except Exception as e:
            print (str(e))
            raise SystemExit
            pass

def updateBuyListSource():
    util.saveProcessedFromYahoo.download = True
    z.getCsv.csvdir = "csv"
    z.getStocks.devoverride = "IUSG"
    stocks = z.getStocks()
    print("stocks : {}".format( len(stocks) ))
    for astock in stocks:
        try:
            updateCsv(astock)
        except Exception as e:
            print (str(e))
            raise SystemExit
            pass

def getMissingStockList():
    import csv
    missing_list = list()
    dates = set(z.getp("dates"))
    stocks = z.getStocks()

    for astock in stocks:
        path = z.getPath("calculated2/{}.csv".format(astock))
        inputf = csv.DictReader(open(path))
        firstdate = None
        myset = set()
        for row in inputf:
            date = row['Date']
            myset.add(date)
            if not firstdate:
                firstdate = date

        missing = (dates-myset)

        if not missing:
            continue

        missing = sorted(missing)

        for item in missing: 
            if firstdate < item:
                print("firstdate : {}".format( firstdate ))
                print("item: {}".format( item))
                print("astock: {}".format( astock))
                missing_list.append(astock)
                break
    z.setp(missing_list, "missing_list")
    print(missing_list)

cheaplist = list()
pricelist = list()
import generate_list
def genBuyList():
    util.saveProcessedFromYahoo.download = True
#    stocks = z.getStocks()
    z.getStocks.devoverride = "IUSG"
    z.getCsv.csvdir = "csv"
    generate_list.setSortedDict(prices_only=True)
#    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    yesterday = "2019-03-27"
    stocks = z.getStocks()
    print("stocks : {}".format( len(stocks) ))
    for astock in stocks:
#        try:
#            price = generate_list.getPrice(astock, yesterday)
#            if price > 10 and price < 20:
#                price2 = generate_list.getPrice(astock, "2017-01-11")
#                price3 = generate_list.getPrice(astock, "2016-01-11")
#                if price < price2 and price > price3:
#                    price3 = generate_list.getPrice(astock, "2018-01-11")
#                    if price > price3:
#                        price3 = generate_list.getPrice(astock, "2019-02-22")
#                        if price3 > price:
#                            pricelist.append((price, astock))
#        except:
#            pass
#        continue
        try:
            util.saveProcessedFromYahoo(astock)
        except Exception as e:
            print (str(e))
            raise SystemExit
            pass
#    import matplotlib.pyplot as plt
#    sorted_xl = sorted(pricelist)
#    print(sorted_xl[-10:] )
#    print(sorted_xl[:10])
#    print(len(sorted_xl))
#
#    for i,item in enumerate(sorted_xl):
#        plt.scatter(i, item[0])
#    plt.show()

#    z.setp(latest, "lastValues")
if __name__ == '__main__':
    updateBuyListSource()
#    z.getStocks.devoverride = "ITOT"
#    getMissingStockList()
#print("downloaded: {}".format( downloaded))
#    genBuyList()
#    updateHistory()
#print(notadded)
#setStockDays()


