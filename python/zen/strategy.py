#from scipy.stats.stats import pearsonr   
#a = [20,20,1]
#b = [20,20,3]   
#print (pearsonr(a,b))
#raise SystemExit
import numpy as np
from collections import Counter, defaultdict
import os
import pandas
import util
import time

title = "standard"
his_idx = 0
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
hisdict = defaultdict(list)
topdict = dict()
latest_values = dict()
def isTop(hashable, symbol):
    global topdict
    if not topdict:
        topdict = util.getp("tops")
    return symbol in dict(Counter(topdict[hashable]).most_common(2))
#print (isTop(hashable, "IVV"))

spend = 2000
size = 10
spent = 1
tranfees = 0
#ivv = util.getETF()
#etfs = []
etfs = util.getFromHoldings()
etfvs = defaultdict(int)

cost_basis = dict()
portf = dict()

more_etf = True
path_dict = {}
etf_purchase_times = defaultdict(int)
def tallyFrom(path, mode, ascending, isLast = False):
    global spent, tranfees, cost_basis, latest_values, etf_purchase_times
    loaded = None
    try:
        if path in path_dict:
            loaded = path_dict[path]
        else:
            loaded = pandas.read_csv(path)
            path_dict[path] = loaded

        if loaded is None:
            return
    except Exception as e:
        print ('2Failed: '+ str(e))
        return
    
    loaded.sort_values(by=[mode], inplace=True, ascending=ascending)

    if mode == "Score" and more_etf:
        for anetf in etfs:
            try:
                etfn = float(loaded[loaded['Unnamed: 0'] == anetf]['Last'])
                buycount = spend / etfn
                etfvs[anetf] += buycount
#                print("anetf: {}".format( anetf))
#                print("buycount: {}".format( buycount))

                etf_purchase_times[anetf] += 1

            except Exception as e:
#                print ('Failed: '+ str(e))
#                print ("Problem with {}".format(anetf))
#                print("path: {}".format( path))
#                raise SystemExit
                continue

    per = spend / size
    spent += spend
    tranfees += 10
    purchased = 0
    if isLast and more_etf:
        for idx,row in loaded.iterrows():
            symbol = loaded.at[idx, "Unnamed: 0"]
            last = loaded.at[idx, "Last"]
            latest_values[symbol] = last
#            if symbol == "SPY":
#                print("last: {}".format( last))
#                print("symbol: {}".format( symbol))
    
    count = 0
    for idx,row in loaded.iterrows():
        symbol = loaded.at[idx, "Unnamed: 0"]
        if symbol in dontBuy:
            continue
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

        purchases[symbol] += round(amount,3)
        purchasesh[symbol] += round(amounth,3)
        purchasesl[symbol] += round(amountl,3)

        purchased += 1
        if purchased == size:
            break

#path = util.getPath("analysis/strategy_report_2015-11-23.csv")
#tallyFrom(path, ["Score", True])
#raise SystemExit
rememberedFiles = []
def getFiles(where):
    global rememberedFiles
    import fnmatch
    if rememberedFiles:
        return rememberedFiles
    holds = []
    reportname = "_{}".format(where, his_idx)
    pattern = "{}*.csv".format(reportname)
    parentdir = util.getPath(where)
    listOfFiles = os.listdir(parentdir)
    for entry in listOfFiles:  
        date = entry.split("_")
        if his_idx == 0 and len(date) < 3 or "-" not in date[2]:
            continue
        if fnmatch.fnmatch(entry, pattern):
            rememberedFiles.append("{}/{}".format(parentdir, entry))
    rememberedFiles.sort()
    return rememberedFiles
#his_idx = 7
#print (getFiles())
#raise SystemExit

def getTrainingTemps(mode, ascending, where):
    paths = getFiles(where)
    leng = len(paths)
    for i,path in enumerate(paths):
        try:
            tallyFrom(path, mode, ascending, isLast=(i==leng-1))
        except Exception as e:
#            print ('Failed: '+ str(e))
#            print("path : {}".format( path ))
            pass

purchases = defaultdict(float)
purchasesl = defaultdict(float)
purchasesh = defaultdict(float)
dontBuy = util.getp("dont")
#latest_values = util.getp("lastValues")
mode_average = defaultdict(list)
def calcIt(mode, ascending, where):
    global purchases, purchasesl, purchasesh,  spent, tranfees, mode_average
    global dontBuy
    spent = 1
    tranfees = 0
    asize = 0
    asizel= 0
    asizeh= 0

    purchases = defaultdict(float)
    purchasesl = defaultdict(float)
    purchasesh = defaultdict(float)

    getTrainingTemps(mode, ascending, where)

    try:
        for astock in purchases:
            lvalue = latest_values[astock]
            asize += purchases[astock] * lvalue
            asizel += purchasesl[astock] * lvalue
            asizeh += purchasesh[astock] * lvalue
    except:
        dontBuy.append(astock)
        print("dont astock: {}".format( astock))
        return
        
#    except Exception as e:
#        print ('3Failed: '+ str(e))
#        return

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

    mode_average[mode_hash].append(high)
    mode_average[mode_hash].append(close)

    one =   "C {0:12} {1:8}".format(mode_hash, change)
    two =   "H {0:12} {1:8}".format(mode_hash, changeh)
    three = "L {0:12} {1:8}".format(mode_hash, changel)
    return ["{} {} {}".format(one, two, three)]


def etfData():
    maxetf = 0
    max_etf_name = ""

    ret = []
    for etf in etfvs:
        etfvalue = round(etfvs[etf] * latest_values[etf], 3)
        if etfvalue > maxetf:
            maxetf = etfvalue 
            max_etf_name = etf

    for etf in etfvs:
        if etf == max_etf_name:
            etfvalue = round(etfvs[etf] * latest_values[etf], 3)
#            print("etfvalue : {}".format( etfvalue ))
            count = etf_purchase_times[etf]
            spent2 = count * spend
            change = etfvalue/spent
#            print("spent: {}".format( spent))

            hisdict[etf].append(change)
#            print("change: {}".format( change))

            change = util.formatDecimal(change)
            ret.append("{0:4}({1:5})\n".format(etf, change))

    for i,etf in enumerate(etfvs):
        if not etf == max_etf_name:
#            print("etf : {}".format( etf ))
            etfvalue = round(etfvs[etf] * latest_values[etf], 3)
#            print("etfvalue : {}".format( etfvalue ))

            count = etf_purchase_times[etf]
            spent2 = count * spend
            change = etfvalue/spent

            hisdict[etf].append(change)
#            print("change: {}".format( change))

            change = util.formatDecimal(change)
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
        try:
            currentValue = round(amount * latest_values[astock])
        except:
            dontBuy.append(astock)
            continue
        change = util.formatDecimal(currentValue/spent)

#        if not (cost.mode == "Variance" and not cost.mode2):
#            continue
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


def writeCostDict(newdict, where):
    import pandas
    df = pandas.DataFrame.from_dict(newdict, orient = 'index', 
            columns=["Value", "Cost", "Change", 
            "DollarChange", "PurchaseDates"])
    path = util.getPath("{}/selection_{}_{}.csv".format(where, title, his_idx))
    df.to_csv(path)
    print ("written {}".format(path))
        

#writeCostDict(newdict)
modes = util.report.headers[:-4]

def doit(where):
    global size, more_etf
    testingModes = [15]
#    testingModes = [10, 15, 20]
    appended = []
    for csize in testingModes:
        size = csize
        appended.append(["stocks {}".format(size)])
        for mode in modes:
            appended.append(calcIt(mode, True, where))
            more_etf = False
            appended.append(calcIt(mode, False, where))
    
    prevavg = 0
    prevvar = 0
    appended.append(["\n"])
    for i, mode in enumerate(mode_average):
        items = mode_average[mode]
        average = sum(items)/len(items)
        vari = round(np.var(items),3)
    
        hisdict[mode] += items
#        print("mode: {}".format( mode))
#        print("items : {}".format( items ))

        appended.append(["A {0:12} {1:8} {2}".format(mode, 
                        util.formatDecimal(average), vari)])
        if i % 2 == 1:
            daverage = abs(prevavg - average)
            dvari =  (prevvar + vari)/2
            appended.append(["{0:8} {1}".format(round(daverage,4), dvari)])
        prevavg = average
        prevvar = vari

    try:
        appended += etfData()
        appended = [item for sublist in appended for item in sublist]
    except:
        appended = []
    
    path = util.getPath("{}/report_{}_{}.txt".format(where, title, his_idx))
    with open(path, "w") as f:
        f.write("\n".join(appended))
    print ("written {}".format(path))

    newdict = costToDict()
    writeCostDict(newdict, where)

#"".join(bar)
def multi(where):
    global his_idx, spent, more_etf, etfvs, latest_values, cost_basis
    global etf_purchase_times, rememberedFiles

    for i in range(2, 10):
        more_etf = True
        his_idx = i
        spent = 1
    
        doit(where)
    
        etfvs = defaultdict(int)
        latest_values = dict()
        cost_basis = dict()
        etf_purchase_times = defaultdict(int)
        rememberedFiles = []

    writeReport(where)

def writeReport(where):
    import csv
    path = util.getPath("{}/Final_{}report.csv".format(where, where))
    with open(path, 'w') as f:
        for key in hisdict.keys():
            appended = []
            current = hisdict[key]
            negs = 0
            mini = util.formatDecimal(min(current))
            maxi = util.formatDecimal(max(current))
            for item in current:
                if item < 1:
                    negs += 1
                appended.append(util.formatDecimal(item))
            avg = util.formatDecimal(sum(current)/len(current))
            vari = round(np.var(current),3)
            percentages  = " ".join(appended)
            f.write("{},{},{},{},{},{},{}\n".format(key, avg, 
                        vari, 
                        maxi,mini,
                        round(negs/len(current),3),
                        percentages))
#doit()
#util.setp(dontBuy, "dont")
#print(dontBuy)
