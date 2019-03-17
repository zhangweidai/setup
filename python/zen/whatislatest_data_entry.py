from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import datetime
import sys
import util

lookup = "IVV"
if len(sys.argv) == 2:
    lookup = sys.argv[1]

tday = datetime.date.today().isoformat()

yf.pdr_override() # <== that's all it takes :-)
print (tday)
try:
    startdate = "2019-03-05"
    data = pdr.get_data_yahoo(["GOOG", "IVV"], start=startdate, 
                              end=str(tday))
#    data.rename( columns={'Unnamed: 0':'Date'}, inplace=True )
    dates = data.tail()
    print(dates)
#    path = util.getPath("csv/{}.csv".format(lookup))
#    data.to_csv(path)
except Exception as e:
    print ('Deleting : '+ str(e))
#    try:
#        startdate = "2019-02-21"
#        data = pdr.get_data_yahoo([lookup], start=startdate, end=str(tday))
#        print (data.tail())
#    except Exception as e:
#        print (str(e))

#saveData(data)
