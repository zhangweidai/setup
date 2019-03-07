from pandas_datareader import data as pdr
from portfolio import getPortfolio
import fix_yahoo_finance as yf
import numpy as np
import pandas
import math
import os
import util 
import scipy 

base = util.loadUSMV_dict()
total = len(base)
low = 350
stocks = util.getStocks()
sub = util.getIVVStocks()
i = 0
start = ( total-low + i * 40 < total )
while ( total-low + (i + 1) * 40 < total):
    i += 1
    start = total - (total-low + i * 40)
    util.loadUSMV_dict(start)
    writeDropCsv(stocks, cut=start)
