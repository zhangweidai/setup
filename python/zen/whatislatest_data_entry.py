from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import datetime
import sys

lookup = "GOOG"
if len(sys.argv) == 2:
    lookup = sys.argv[1]

yf.pdr_override() # <== that's all it takes :-)
tday = datetime.date.today().isoformat()
print (tday)
try:
    startdate = "2019-02-09"
    data = pdr.get_data_yahoo([lookup], start=startdate, end=str(tday))
    print (data.tail())
except Exception as e:
    print (str(e))
