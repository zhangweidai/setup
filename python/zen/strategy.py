from datetime import date, timedelta
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import os
import pandas
import util
import time

spend = 2000
reportname = "strategy_report_"
size = 10
spent = 1
tranfees = 0
ivv = util.getivvstocks()
etfs = util.getFromHoldings()
etfvs = dict()

saved_size = 0
saved_portfolio = dict()
cost_basis = dict()
purchases = dict()
purchasesl = dict()
purchasesh = dict()
more_etf = True
path_dict = {}
def tallyFrom(path, mode):
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
    
    loaded.sort_values(by=[mode[0]], inplace=True, ascending=mode[1])

    if mode[0] == "Score" and more_etf:
        for anetf in etfs:
            etfn = float(loaded[loaded['Unnamed: 0'] == anetf]['Last'])
            etfvs.setdefault(anetf, 0)
            buycount = spend / etfn
            etfvs[anetf] += buycount

    per = spend / size
    spent += spend
    tranfees += 10
    purchased = 0

    for idx,row in loaded.iterrows():
        symbol = loaded.at[idx, "Unnamed: 0"]
        if symbol in etfs:
            continue

        last = loaded.at[idx, "Last"]
        lasth = loaded.at[idx, "LastH"]
        lastl = loaded.at[idx, "LastL"]

        amount = per / last
        amounth = per / lasth
        amountl = per / lastl

        if mode[0] == "Dip" and size == 20:
            cost_basis.setdefault(symbol, 0)
            cost_basis[symbol] += per

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
mode_average = dict()
def calcIt(mode):
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

    getTrainingTemps(mode)

    for astock in purchases:
        asize += purchases[astock] * latest_values[astock]
        asizel += purchasesl[astock] * latest_values[astock]
        asizeh += purchasesh[astock] * latest_values[astock]

    if mode[0] == "Dip" and size == 20:
        saved_portfolio = purchases
        saved_size = asize

    low = round(asizel / (spent + tranfees),3)
    high = round(asizeh / (spent + tranfees),3)
    close = round(asize / (spent + tranfees),3)

    changel = util.formatDecimal(low)
    changeh = util.formatDecimal(high)
    change = util.formatDecimal(close)

    mode_average.setdefault(mode[0], [])
#    mode_average[mode[0]].append(low)
    mode_average[mode[0]].append(high)
    mode_average[mode[0]].append(close)

    one =   "C {0:12} {1:8}".format(mode[0], change)
    two =   "H {0:12} {1:8}".format(mode[0], changeh)
    three = "L {0:12} {1:8}".format(mode[0], changel)
    return ["{} {} {}".format(one, two, three)]

modes = [["Score", True],
    ["Discount", False],
    ["Dip", True],
    ["Variance", True],
    ["PointsAbove", False],
    ["WC", True]
    ]
#    ["3", True],
#    ["6", False],
#    ["12", True],
#    ["24", False],
#    ["48", False],
#    ["96", False],
#    ["192", False]]

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


def doit():
    global size, more_etf
    testingModes = [10, 15, 20, 30]
    appended = []
    for csize in testingModes:
        size = csize
        appended.append(["stocks {}".format(size)])
        for mode in modes:
            appended.append(calcIt(mode))
        more_etf = False

    
    import numpy as np
    appended.append(["\n"])
    for mode in mode_average:
        items = mode_average[mode]
        average = sum(items)/len(items)
        vari = round(np.var(items),3)

        appended.append(["A {0:12} {1:8} {2}".format(mode, 
                    util.formatDecimal(average), vari)])

    appended += etfData()
    appended = [item for sublist in appended for item in sublist]

    newdict = dict()
    for astock in saved_portfolio:
        value = round(saved_portfolio[astock] * latest_values[astock])
        cost = cost_basis[astock]
        change = util.formatDecimal(value/cost)
#        appended.append("{0:4} {1:8} {2:8}".format(astock, cost, change))
        newdict[astock] = [value, cost, change]

    import pandas
    df = pandas.DataFrame.from_dict(newdict, orient = 'index', 
            columns=["Value", "Cost", "Change"])
    path = util.getPath("analysis/stocks_strat.csv")
    df.to_csv(path)
        
    path = util.getPath("analysis/report.txt")
    with open(path, "w") as f:
        f.write("\n".join(appended))
doit()


