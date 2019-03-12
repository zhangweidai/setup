#from scipy.stats.stats import pearsonr   
#a = [20,20,1]
#b = [20,20,3]   
#print (pearsonr(a,b))
#raise SystemExit

from datetime import date, timedelta
from pandas_datareader import data as pdr
from collections import Counter
import fix_yahoo_finance as yf
import os
import pandas
import util
import time

title = "standard"

spentidx = 0
amountidx = 1
datesidx = 2
class Cost():
    def __init__(self, mode, mode2, symbol):
        self.mode = mode
        self.mode2 = mode2
        self.symbol = symbol

    def __str__(self):
        return "{}/{}/{}".format(self.mode, self.mode2, self.symbol)

    def __eq__(self, other):
        isinst = isinstance(other, type(self))
        return isinst and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.__dict__[k] 
                          for k in sorted(self.__dict__)))

topdict = dict()
def isTop(hashable, symbol):
    global topdict
    if not topdict:
        topdict = util.getp("tops")
    return symbol in dict(Counter(topdict[hashable]).most_common(2))
#print (isTop(hashable, "IVV"))

spend = 2000
reportname = "strategy_report_"
size = 10
spent = 1
tranfees = 0
ivv = util.getivvstocks()
etfs = util.getFromHoldings()
etfvs = dict()

saved_portfolio = dict()
cost_basis = dict()
portf = dict()
purchases = dict()
purchasesl = dict()
purchasesh = dict()
more_etf = True
path_dict = {}
def tallyFrom(path, mode, ascending):
    global spent, tranfees, cost_basis
    loaded = None
    try:
        if path in path_dict:
            loaded = path_dict[path]
        else:
            loaded = pandas.read_csv(path)
            path_dict[path] = loaded

        if loaded is None:
            return
    except:
        return
    
    loaded.sort_values(by=[mode], inplace=True, ascending=ascending)

    if mode == "Score" and more_etf:
        for anetf in etfs:
            etfn = float(loaded[loaded['Unnamed: 0'] == anetf]['Last'])
            etfvs.setdefault(anetf, 0)
            buycount = spend / etfn
            etfvs[anetf] += buycount

    per = spend / size
    spent += spend
    tranfees += 10
    purchased = 0
    
    count = 0
    for idx,row in loaded.iterrows():
        symbol = loaded.at[idx, "Unnamed: 0"]
#        if count < 2:
#            count += 1
#            continue

#        if symbol in etfs or symbol in ivv:
#        if not symbol in ivv:
#            continue

#        hashable = "{}{}".format(mode, ascending)
#        if isTop(hashable, symbol):
#            continue

        last = loaded.at[idx, "Last"]
        lasth = loaded.at[idx, "LastH"]
        lastl = loaded.at[idx, "LastL"]

        amount = per / last
        amounth = per / lasth
        amountl = per / lastl

        if size == 15:
            date = path.split("_")[3].split(".")[0]
            custom = Cost(mode, ascending, symbol)
            cost_basis.setdefault(custom, [0,0,[]])
            cost_basis[custom][spentidx] += per
            cost_basis[custom][amountidx] += amount
            cost_basis[custom][datesidx].append(date)

        purchases.setdefault(symbol, 0)
        purchasesl.setdefault(symbol, 0)
        purchasesh.setdefault(symbol, 0)

        purchases[symbol] += round(amount,5)
        purchasesh[symbol] += round(amounth,5)
        purchasesl[symbol] += round(amountl,5)

        purchased += 1
        if purchased == size:
            break

#path = util.getPath("analysis/strategy_report_2015-11-23.csv")
#tallyFrom(path, ["Score", True])
#print (etfvs)
#raise SystemExit
rememberedFiles = []
def getFiles():
    global rememberedFiles
    import fnmatch
    if rememberedFiles:
        return rememberedFiles
    pattern = "{}*.csv".format(reportname)
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

def getTrainingTemps(mode, ascending):
    paths = getFiles()
    for path in paths:
        try:
            tallyFrom(path, mode, ascending)
        except Exception as e:
            print ('Failed: '+ str(e))
            pass

changeDict = dict()
latest_values = util.getp("latestValues")
mode_average = dict()
def calcIt(mode, ascending):
    global purchases, purchasesl, purchasesh,  spent, tranfees, mode_average
    global saved_portfolio
    spent = 1
    tranfees = 0
    asize = 0
    asizel= 0
    asizeh= 0

    purchases = dict()
    purchasesl = dict()
    purchasesh = dict()

    getTrainingTemps(mode, ascending)

    for astock in purchases:
        asize += purchases[astock] * latest_values[astock]
        asizel += purchasesl[astock] * latest_values[astock]
        asizeh += purchasesh[astock] * latest_values[astock]

    if size == 20:
        portf[mode, ascending] = purchases

    low = round(asizel / (spent + tranfees),3)
    high = round(asizeh / (spent + tranfees),3)
    close = round(asize / (spent + tranfees),3)

    changel = util.formatDecimal(low)
    changeh = util.formatDecimal(high)
    change = util.formatDecimal(close)

    mode_hash = mode
    if ascending:
        mode_hash += "A"

    mode_average.setdefault(mode_hash, [])
    mode_average[mode_hash].append(low)
    mode_average[mode_hash].append(high)
    mode_average[mode_hash].append(high)
    mode_average[mode_hash].append(close)
    mode_average[mode_hash].append(close)

    one =   "C {0:12} {1:8}".format(mode_hash, change)
    two =   "H {0:12} {1:8}".format(mode_hash, changeh)
    three = "L {0:12} {1:8}".format(mode_hash, changel)
    return ["{} {} {}".format(one, two, three)]


def etfData():
    maxetf = 0
    etf_name = ""

    ret = []
    for etf in etfvs:
        etfvalue = round(etfvs[etf] * latest_values[etf], 3)
        if etfvalue > maxetf:
            maxetf = etfvalue 
            etf_name = etf

    for etf in etfvs:
        if etf == etf_name:
            etfvalue = round(etfvs[etf] * latest_values[etf], 3)
            change = util.formatDecimal(etfvalue/spent)
            ret.append("{0:4}({1:5})\n".format(etf, change))

    for i,etf in enumerate(etfvs):
        if not etf == etf_name:
            etfvalue = round(etfvs[etf] * latest_values[etf], 3)
            change = util.formatDecimal(etfvalue/spent)
            ret.append("{0:4}({1:5})".format(etf, change))
            if i == 6:
                ret.append("\n")
    return [["".join(ret), "{}\n".format(spent)]]


def costToDict():
    global topdict
    newdict = dict()
    for cost in cost_basis:
        values = cost_basis[cost]
        spent = values[spentidx]
        amount = values[amountidx]
        dates = values[datesidx]
        astock = cost.symbol
        currentValue = round(amount * latest_values[astock])
        change = util.formatDecimal(currentValue/spent)
        if not (cost.mode == "Dip" and not cost.mode2):
            continue
        hashable = "{}".format(str(cost))
        newdict[hashable] = [currentValue, round(spent), change, 
        round(currentValue-spent), ",".join(dates)]

        hashable = "{}{}".format(cost.mode, cost.mode2)
        if not topdict.get(hashable):
            topdict[hashable] = dict()
        topdict[hashable][astock] = currentValue - spent

#    util.setp(topdict, "tops")
    return newdict

def testCostToDict():
    custom = Cost("MODE2", False, "IVV")
    cost_basis.setdefault(custom, [0,0])
    cost_basis[custom][spentidx] += 200
    cost_basis[custom][amountidx] += 100
    
    custom = Cost("MODE2", False, "GOOG")
    cost_basis.setdefault(custom, [0,0])
    cost_basis[custom][spentidx] += 1200
    cost_basis[custom][amountidx] += 10
    
    custom = Cost("MODE", True, "ABC")
    cost_basis.setdefault(custom, [0,0])
    cost_basis[custom][spentidx] += 200
    cost_basis[custom][amountidx] += 100
    newdict = costToDict()



def writeCostDict(newdict):
    import pandas
    df = pandas.DataFrame.from_dict(newdict, orient = 'index', 
            columns=["Value", "Cost", "Change", 
            "DollarChange", "PurchaseDates"])
    path = util.getPath("analysis/selection_{}.csv".format(title))
    df.to_csv(path)
        

#writeCostDict(newdict)
#
modes = ["Score", "Discount", "Dip", "Variance", "PointsAbove", "WC"]
#modes = ["Score", "Discount"]
def doit():
    global size, more_etf
    testingModes = [3, 5, 9, 12, 15]
#    testingModes = [10, 15, 20]
    appended = []
    for csize in testingModes:
        size = csize
        appended.append(["stocks {}".format(size)])
        for mode in modes:
            appended.append(calcIt(mode, True))
            more_etf = False
            appended.append(calcIt(mode, False))
    
    import numpy as np
    prevavg = 0
    prevvar = 0
    appended.append(["\n"])
    for i, mode in enumerate(mode_average):
        items = mode_average[mode]
        average = sum(items)/len(items)
        vari = round(np.var(items),3)
    
        appended.append(["A {0:12} {1:8} {2}".format(mode, 
                        util.formatDecimal(average), vari)])
        if i % 2 == 1:
            daverage = abs(prevavg - average)
            dvari =  (prevvar + vari)/2
            appended.append(["{0:8} {1}".format(round(daverage,4), dvari)])
        prevavg = average
        prevvar = vari


    appended += etfData()
    appended = [item for sublist in appended for item in sublist]

    path = util.getPath("analysis/report_{}.txt".format(title))
    with open(path, "w") as f:
        f.write("\n".join(appended))

    newdict = costToDict()
    writeCostDict(newdict)

doit()