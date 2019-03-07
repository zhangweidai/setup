from datetime import date, timedelta
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import pandas
import util
import time

spend = 2000
size = 10
purchase = dict()
spent = 1
tranfees = 0
etftotal = 0
etf = "USMV"
#ivv = util.getivvstocks()
def tallyFrom(path, mode):
    global spent, tranfees, etftotal
    try:
        loaded = pandas.read_csv(path)
        if loaded is None:
            print ("problem")
            return
    except:
        print ("problem")
        return
    
    loaded.sort_values(by=[mode[0]], inplace=True, 
                       ascending=mode[1])

    symbols = loaded['Unnamed: 0'].tolist()
    prices = loaded['Last'].tolist()

    etfn = float(loaded[loaded['Unnamed: 0'] == etf]['Last'])
    etftotal += spend / etfn

    per = spend / size
    spent += spend
    tranfees += 10
    purchased = 0
    for i, price in enumerate(prices):
        symbol = symbols[i]
#        if not symbol in ivv:
#            continue
        amount = per / price
        purchase.setdefault(symbol, 0)
        purchase[symbol] += round(amount,5)
        purchased += 1
        if purchased == size:
            break

rememberedFiles = []
def getFiles():
    global rememberedFiles
    import fnmatch
    if rememberedFiles:
        return rememberedFiles
    pattern = "main_report_*.csv"
    holds = []
    parentdir = util.getPath("analysis")
    listOfFiles = os.listdir(parentdir)
    for entry in listOfFiles:  
        date = entry.split("_")
        if len(date) < 3 or "-" not in date[2]:
            continue
        if fnmatch.fnmatch(entry, pattern):
            rememberedFiles.append("{}/{}".format(parentdir, entry))
    return rememberedFiles


def getTrainingTemps(mode):
    paths = getFiles()
    for path in paths:
        try:
            tallyFrom(path, mode)
        except Exception as e:
            print ('Failed: '+ str(e))
            pass

changeDict = dict()
latest_values = util.getp("latestValues")
def calcIt(mode):
    global purchase, curr_account_size, spent, tranfees, etftotal
    spent = 1
    tranfees = 0
    curr_account_size = 0
    purchase = dict()
    etftotal = 0
    getTrainingTemps(mode)
    for astock in purchase:
        curr_account_size += purchase[astock] * latest_values[astock]
    change = round(curr_account_size / (spent + tranfees),3)
    print ("mode: {}".format(mode[0]))
    print ("change: {}".format(util.formatDecimal(change)))

modes = [["Score", False],
    ["Discount", True],
    ["Dip", True],
    ["Variance", False],
    ["PointsAbove", False],
    ["WC", False],
    ["WCBad", False],
    ["3", True],
    ["6", False],
    ["12", False],
    ["24", False],
    ["48", False],
    ["96", False],
    ["192", False]]

#for mode in modes:
#    calcIt(mode)

#etfvalue = round(etftotal * latest_values[etf], 3)
#print("etf         : $" + str(etfvalue))
#print("etfchange   : " + util.formatDecimal(etfvalue/spent))
#print("spent       : " + str(spent))

path = util.getPath("csv/USMV.csv")
df = pandas.read_csv(path)
values = df['Avg'].tolist()
etfspent =  (sum(values))
print("etfspent :" + str(etfspent))
purchased = (len(values))
print("purchased :" + str(purchased ))
etfvalue = round(purchased * latest_values["USMV"], 3)
print("etfvalue :" + str(etfvalue ))
print (util.formatDecimal(etfvalue/etfspent))

maxp = purchased
occ = 1
for i in range(1, 30):
    perspend = etfspent / i
    days = int(len(values) / i)
#    print("days :" + str(days))
#    print("perspend :" + str(perspend ))
    purchased = 0
    for count, value in enumerate(values):
        if count % days == 0:
            purchased += perspend / value

    if purchased > maxp:
        maxp = purchased
        occ = i
#        print ("")
#        print (maxp)
#        print (i)
#        print (perspend * i)

print("occ:" + str(occ))
days = int(len(values) / occ)
for count, value in enumerate(values):
    if count % days == 0:
        print("count:" + str(count))
        print("value:" + str(value))

#    else:
#        print ("for {} i got {} total spent = {}".format(i,purchased, perspend * i))
etfvalue = round(maxp * latest_values["USMV"], 3)
print("etfvalue :" + str(etfvalue ))
print (util.formatDecimal(etfvalue/etfspent))


#print("\n")
#try:
#    change = round(curr_account_size / (spent + tranfees),3)
#    print("account     : $" + str(round(curr_account_size,3)))
#    print("spent       : $" + str(spent + tranfees))
#    print("tranfees    : $" + str(tranfees))
#    change = round(curr_account_size / (spent + tranfees),3)
#    print("change      : " + util.formatDecimal(change))
#    etfvalue = round(etftotal * latest_values[etf])
#    print("etf         : $" + str(etfvalue))
#    print("etfchange   : " + util.formatDecimal(etfvalue/spent))
#    print("stock count : " + str(len(purchase)))
##    print(purchase)
#
#except Exception as e:
#    print ('Failed: '+ str(e))
 
