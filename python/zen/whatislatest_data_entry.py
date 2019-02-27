from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import datetime

yf.pdr_override() # <== that's all it takes :-)
tday = datetime.date.today().isoformat()
data = pdr.get_data_yahoo(["LIN"], start="2019-02-20", end=tday)
print (data.tail())
