import util
from datetime import date, timedelta
import datetime
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

def shouldUpdate():
    tday = datetime.date.today().isoformat()
    yf.pdr_override() # <== that's all it takes :-)
    startdate = "2019-03-05"
    try:
        data = pdr.get_data_yahoo(["IVV"], start=startdate, end=str(tday))
    except : 
        try:
            data = pdr.get_data_yahoo(["IVV"], start=startdate, end=str(tday))

        except Exception as e:
            print ('Problems : '+ str(e))
            return False

    loaded = util.getCsv("IVV")
    lastdate = loaded.tail(1)["Date"].item()
    yahoo_date = str(data.index[-1]).split(" ")[0]

    if lastdate == yahoo_date:
        return False, yahoo_date

    return True, yahoo_date

def doit():
    should, latestInfo = shouldUpdate()
    if should:
        import update_csv
        update_csv.updateStocks(latestInfo)

    end = util.getNumberOfDates()
    start = end - 201
    vals = [start, end]
    stocks = util.getStocks()

    csvfile = util.writeStrategyReport(stocks, 
            start=vals[0], end=vals[1], reportname = "main_")

    util.setp(csvfile, "buyfile")
    print (util.getWhatToBuy(1, True))

print (util.getp("buyfile"))
#doit()

#print (util.getWhatToBuy(1, False))
#    updateCsvs()
#    print ("good")

