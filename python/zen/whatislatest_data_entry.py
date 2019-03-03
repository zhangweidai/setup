from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import datetime
import sys

lookup = "GOOG"
if len(sys.argv) == 2:
    lookup = sys.argv[1]

tday = datetime.date.today().isoformat()
startdate = "2017-01-01"
#def saveProcessedFromYahoo(df, path):
#    try:
#        df = pdr.get_data_yahoo([lookup], start=startdate, end=str(tday))
#    except:
#        try:
#            df = pdr.get_data_yahoo([lookup], start=startdate, end=str(tday))
#        except Exception as e:
#            print (str(e))
#
#    avg = list()
#    df.drop(columns = ["Adj Close"], inplace=True)
#    for idx,row in df.iterrows():
#        sub = 0
#        for label in ["Open", "Close", "High", "Low"]:
#            temp = round(df.at[idx, label], 4)
#            sub += temp
#            df.at[idx, label] = temp
#        avg.append(sub/4)
#
#    idx = 4
#    df.insert(loc=idx, column='Avg', value=avg)
#
#    path = "/mnt/c/Users/Peter/Documents/setup/python/zen/new/{}.csv".format(astock)
#    df.to_csv(path)
#
yf.pdr_override() # <== that's all it takes :-)
print (tday)
try:
    startdate = "2019-02-21"
    data = pdr.get_data_yahoo([lookup], start=startdate, end=str(tday))
    print (data.tail())
except:
    try:
        startdate = "2019-02-21"
        data = pdr.get_data_yahoo([lookup], start=startdate, end=str(tday))
        print (data.tail())
    except Exception as e:
        print (str(e))

#saveData(data)
