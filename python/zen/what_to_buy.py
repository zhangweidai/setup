import util
from datetime import date, timedelta
import datetime
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import math
#3/20
#PointsAbove 25.22%  0.02    39.40%  2.00%   0   1.949
#Score   24.50%  0.021   38.40%  1.20%   0   1.937
#VariA   23.95%  0.021   36.40%  1.50%   0   1.922
#WCA 34.38%  0.042   56.20%  -0.20%  0.167   1.9
#Dip 32.25%  0.066   57.30%  -8.60%  0.167   1.888
#HighLow 30.20%  0.043   48.30%  -0.90%  0.167   1.826
#Vari2   27.62%  0.031   46.00%  -2.10%  0.167   1.793
#Range   13.65%  0.005   21.50%  1.60%   0   1.744
#Discount    38.27%  0.088   62.30%  -6.80%  0.333   1.734
#IUSG    12.28%  0.009   21.74%  2.82%   0   1.732
#WC  23.23%  0.031   39.50%  -4.10%  0.167   1.724


#3/17
#VariA   24.67%  0.03    55.10%  -1.50%  0.014
#ScoreA  14.94%  0.017   29.80%  -8.10%  0.097
#Vari2   16.77%  0.014   38.70%  -6.90%  0.097
#IUSG    9.37%   0.008   21.34%  -6.05%  0.125
#IVV     7.77%   0.009   20.27%  -9.30%  0.125
#IWB     8.15%   0.009   21.21%  -8.85%  0.125
#SPY     7.68%   0.008   20.07%  -9.26%  0.125
#DipA    8.05%   0.007   19.00%  -8.70%  0.167
#DSI     4.68%   0.018   21.74%  -20.35% 0.167
#Disco   17.02%  0.017   33.60%  -6.00%  0.181
#Vari    7.35%   0.014   28.40%  -17.80% 0.181


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

def what_to_buy():
    util.getStocks.totalOverride = True
    should, latestInfo = shouldUpdate()
#    if should:
    import update_csv
    update_csv.updateStocks(latestInfo)

    end = util.getNumberOfDates()
    start = end - util.getBuyBackTrack()
    vals = [start, end]
    stocks = util.getStocks()

    csvfile = util.report(stocks, 
            start=vals[0], end=vals[1], reportname = "main_")

    util.setp(csvfile, "buyfile")
#    print (util.getWhatToBuy(1, True))

util.getStocks.totalOverride = True
util.saveProcessedFromYahoo.download = False
util.getCsv.csvdir="historical"
#print (util.getp("buyfile"))
what_to_buy()

#stocks = util.getStocks()
#probability(stocks)


#stocks = util.getStocks(dev=True)
#print (util.prob_per_stock(stocks))
