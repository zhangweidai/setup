def getRanges(values):
    ret = []
    items =  len(values)
    minimum = 25
    minrequired = 200
    i = 1
    last = (items % minimum)
    while ((i * minimum) + minrequired < items):
        start = ((i-1) * minimum) 
        
        end = ((i) * minimum) + minrequired
        ret.append([start, end])
        i += 1
    
    start = ((i-1) * minimum)
    end = start + last + minrequired

    ret.append([start, end])
    return ret

#import util 
#print (getRanges(util.getTestItems(500)))

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
low = 370
stocks = util.getStocks()
sub = util.getivvstocks()
i = 0
#endi = ( total-low + i * 20 < total)
#while ( total-low + (i + 1) * 20 < total):
#    i += 1
#    endi = total - (total-low + i * 20)
#    util.loadUSMV_dict(endi)
#    util.writeDropCsv(stocks, end=endi, start=100)
#
for vals in getRanges():
    util.loadUSMV_dict()
    util.writeDropCsv(stocks, end=endi, start=100)



