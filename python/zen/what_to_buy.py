import util
from datetime import date, timedelta
import datetime
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import math
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
#Vari2A  11.41%  0.014   30.10%  -11.90% 0.181
#Score   12.93%  0.017   26.00%  -14.30% 0.194
#HighLow 16.33%  0.017   33.00%  -7.10%  0.194
#PointsA 16.40%  0.028   42.60%  -16.60% 0.194
#WC      12.79%  0.017   28.90%  -14.90% 0.194
#Hghw    9.85%   0.013   32.00%  -11.10% 0.208
#PointA  9.61%   0.012   31.50%  -8.00%  0.208
#WCA     19.42%  0.029   56.40%  -5.40%  0.208
#DsntA   14.24%  0.02    42.60%  -11.40% 0.222
#Dip     21.04%  0.054   61.50%  -18.50% 0.236
#IJH     9.76%   0.01    24.90%  -3.94%  0.25
#EWH     8.87%   0.01    24.92%  -5.90%  0.25
#MCHI    2.11%   0.038   33.19%  -20.12% 0.75


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
    should, latestInfo = shouldUpdate()
    if should:
        import update_csv
        update_csv.updateStocks(latestInfo)

    end = util.getNumberOfDates()
    start = end - util.getBuyBackTrack()
    vals = [start, end]
    stocks = util.getStocks()

    csvfile = util.writeStrategyReport(stocks, 
            start=vals[0], end=vals[1], reportname = "main_")

    util.setp(csvfile, "buyfile")
#    print (util.getWhatToBuy(1, True))

#util.getStocks.totalOverride = True
#util.saveProcessedFromYahoo.download = False
#util.getCsv.csvdir="historical"
#print (util.getp("buyfile"))
what_to_buy()

def probability(stocks):
    util.getStocks.totalOverride = True
    util.saveProcessedFromYahoo.download = False
    util.getCsv.csvdir="historical"
    ups = []
    downs = []
    minv = 6000 
    for stock in stocks:
        if not stock.isalpha():
            continue

        df = util.getCsv(stock)
        if df is None:
            continue

        values = df["Close"].tolist()
        numv = len(values)

        if numv < minv:
            minv = numv

        half = int(len(values)/2)
        try:
            values = values[-1204:]
        except:
            continue

        answer =  round(values[-1] / values[0],3)
        if answer > 1:
            ups.append(answer)
        else:
            downs.append(answer)
    down = len(downs)
    up = len(ups)
    print("minv : {}".format( minv ))
    print("up : {}".format( up ))
    print("downs : {}".format( down ))
    count = len(stocks)
    print("count : {}".format( count ))
    print (round(up/count, 3))

#stocks = util.getStocks()
#probability(stocks)


#stocks = util.getStocks(dev=True)
#print (util.prob_per_stock(stocks))
