from datetime import date, timedelta
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import pandas
import util
import time

spend = 3000
size = 30
purchase = dict()
spent = 0
def tallyFrom(path):
    global spent
    loaded = pandas.read_csv(path)
    print (loaded.columns)
    loaded.sort_values(by=['Score'], inplace=True, ascending=False)
#    print (loaded['Score'].tolist()[:30])
    symbols = loaded['Unnamed: 0'].tolist()[:30]
    prices = loaded['Last'].tolist()[:30]
    per = spend / size
    spent += spend
    for i,price in enumerate(prices):
        amount = per / price
        symbol = symbols[i]
        purchase.setdefault(symbol, 0)
        purchase[symbol] += round(amount,2)

def getTrainingTemps():
    import fnmatch
    pattern = "main_report_*.csv"
    holds = []
    parentdir = util.getPath("analysis")
    listOfFiles = os.listdir(parentdir)
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            path = "{}/{}".format(parentdir, entry)
            print("path :" + path )
            tallyFrom(path)
            break
#getTrainingTemps()
print (util.getp("latestValues"))
