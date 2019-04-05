import numpy as np
import os
import operator
import math
import pandas
import datetime
import pickle
import fix_yahoo_finance as yf
import fnmatch
import urllib.request, json
from scipy import stats
from pandas_datareader import data as pdr
from functools import lru_cache

CsvColumn = "Close"
EtfBaselineTicker = "SPY"
unnamed = "Unnamed: 0"

def formatDecimal(factor):
    return "{:.2%}".format(factor-1)
#print(formatDecimal(2.93))

def getTestItems(needed = 30, simple = False, astock=None):
    if astock:
        return getCsv(astock)[CsvColumn].tolist()
    from math import sqrt
    if simple:
        return [1,1,1,1,1,1,1,2,2,2,2,3,3,3,3,3,1,1,1,1,1,1,1,3,4,4,5,5,
        6,6,7,7,7,8,8,7,6,6,5,4,6,5,4,3,9,7,8,9]
    return [i for i in range(1,needed)]

def getPath(path, allowmake = True):
    path = "{}/../zen_dump/{}".format(os.getcwd(), path)
    parent = os.path.dirname(path)
    if allowmake and not os.path.exists(parent):
        os.makedirs(parent)
    return path

def getp(name):
    try:
        path = getPath("pkl/{}.pkl".format(name))
        return pickle.load(open(path, "rb"))
    except:
        return None

def setp(data, name):
    path = getPath("pkl/{}.pkl".format(name))
    pickle.dump(data, open(path, "wb"))

def getRangedDist(items):
    maxr = 100
    if len(items) < maxr:
        return None
    newlist = items[-1*maxr:]

    newlist_2 = []
    previtem = newlist[0]
    for item in newlist[1:]:
        newlist_2.append(round(previtem / item, 6))
    vari3 = np.var(newlist_2)

    maxv = max(newlist)
    minv = min(newlist)
    lastitems = newlist[-1]

    varlist = [newlist[0], lastitems, minv, maxv] + items[-50:]
    vari = np.var([newlist[0], lastitems, minv, maxv])

    ret2 = round(vari,5)
    ret3 = round(vari3,5)

    if lastitems == maxv:
        return round(maxv/minv,3), ret2, ret3
    else:
        ret = round((lastitems/minv)-1,3)
        return ret, ret2, ret3
#print(getRangedDist(getTestItems()))
#raise SystemExit

def regress(items):
    leng = len(items)
    if leng == 0:
        print ("why is this empty")
        return 0
    i = 0
    x = []
    for b in items:
        i+=1
        x.append(i)

    x = np.asarray(x)
    y = np.asarray(items)
    sub = sum(items)/leng

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    rs = (r_value**2)/2
    normalized_err = (std_err/sub)
    if normalized_err == 0:
        normalized_err = 0.0001
    score = rs/(normalized_err)
    return score

def averageRegress(items):
    count = int(len(items)/3)
    first = items[:count]
    second = items[count:count*2]
    three = items[count*2:]
    f1 = regress(first) / 1.618033
    f2 = regress(second) 
    f3 = regress(three) * 1.618033
    return (f1 + f2 + f3)
#print (averageRegress(getTestItems()))

def dipScore(items, interval=7, avg=3, retAvg=False):
    from collections import deque
    currentStack = deque([])
    low = deque([])
    dips = []
    gains = []
    for i,price in enumerate(items):
        currentStack.append(price)
        if len(currentStack) == interval:
            start = (max(list(currentStack)[:avg]))
            end = (min(list(currentStack)[-1*avg:]))
            tdip = (end/start)
            if tdip < 1 and not retAvg:
                dips.append(1-tdip)
            elif tdip < 1 and retAvg:
                dips.append(tdip)
            elif retAvg and tdip > 1:
                gains.append(tdip)
            currentStack.popleft()
    if retAvg:
        return round(sum(dips)/len(dips),5), round(sum(gains)/len(gains),5), 
    return round(sum(dips),6)

def getFactors(items):
    one = (items[-50] + items[-50])/2
    two = (items[-180] + items[-181])/2
    final = (items[-1] + items[-2])/2

    return round((((final/two)+1)/7)+(((final/one)+1)/2),5)

def getScore(items):
    num =  averageRegress(items)
    bottom = dipScore(items)
    return (num,bottom)
#a,b = getScore(getTestItems())
#print (a/b)

def writeFile(dictionary, cols, directory="all", name = "training"):
    df = pandas.DataFrame.from_dict(dictionary, orient = 'index', columns=cols)
    path = getPath("{}/{}.csv".format(directory, name))
    try:
        df.to_csv(path)
    except:
        try:
            os.makedirs(os.path.dirname(path))
            df.to_csv(path)
        except Exception as e:
            try:
                import tempfile
                path = next(tempfile._get_candidate_names())
                df.to_csv(path)
            except Exception as e:
                print ('FailedWrite: '+ str(e))
                return None
    print ("File Written " + path)
    return path


def getWC(items):
    howmany = len(items)

    half = int(howmany/2)
    first =  max(items[:half])
    second = min(items[half:])
    wcb = round(second/first,3)

    start = howmany-130 
    short = items[-10:]
    newlist = items[start:start+100]
    minv = min(short)
    maxv = max(short)
    maxv2 = max(newlist)

    up = 0
    for v in newlist:
        if v<maxv:
            up+=1
    return round(minv/maxv2,3), up/100, wcb
#print (getWC(getTestItems(1000, simple = True)))

def getChanges(items):
    last = 1
    last2 = 1
    lastvalue = items[-1]
    if len(items) >= 384:
        last = lastvalue / items[-384]
    if len(items) >= 192:
        last2 = lastvalue / items[-192]

    ret = [ lastvalue / items[-3], lastvalue / items[-6],
    lastvalue / items[-12], lastvalue / items[-24], 
    lastvalue / items[-48], lastvalue / items[-96], 
    last2, last]

    for i,b in enumerate(ret):
        ret[i] = round(b,3)

    return ret
#print (getChanges(items))

def getDiscount(items):
    newlist = items[-4:]
    num = (items[-1] + items[-2])/2
    return round(num/newlist[0],4)
#print (getDiscount(getTestItems()))

def getEtfList():
    path = getPath("analysis/ETFList.csv")
    data = pandas.read_csv(path)
    return data['Symbol'].tolist()

def getTrainingTemps():
    pattern = "*.csv"  
    holds = []
    listOfFiles = os.listdir('../zen_dump/training_data')  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append(entry)
    return holds
#print (getTrainingTemps())

def getFromHoldings():
    try: return getFromHoldings.etfs
    except: pass

    pattern = "*.csv"  
    holds = []
    listOfFiles = os.listdir('../zen_dump/holdings')  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append(entry.split("_")[0])
    holds.append("SPY")

    getFromHoldings.etfs = holds
    return holds

@lru_cache(maxsize=6)
def getETF(etf = "IVV"):
    path = getPath("holdings/{}_holdings.csv".format(etf))
    try:
        temp = pandas.read_csv(path)
        getETF.ret_df[etf] = temp
        retlist = temp['Ticker'].tolist()
    except Exception as e:
        print ('FailedWrite: '+ str(e))
        return None
    return retlist
getETF.ret_df = dict()

def getScoreFromCsv(astock):
    try:
        df = getStocks.dataf
    except:
        try:
            path = getp("buyfile")
            df = pandas.read_csv(path)
        except Exception as e:
            try:
                path = getPath("analysis/main_2019-03-12.csv")
                df = pandas.read_csv(path)
            except:
                print ("getScoreFromCsv")
                print (str(e))
                return None
    ret = df.loc[df[unnamed] == astock]["Score"].to_string()
    ret = " ".join(list(filter(None, ret.split(' ')))[1:])
    return ret
#path = getp("buyfile")
#print("path : {}".format( path ))
#raise SystemExit
def getCompanyNameFrom(astock, df):
    try : 
        ret = df.loc[df['Ticker'] == astock]
        if ret.empty:
            raise ValueError('NotFound.')
        ret = df.loc[df['Ticker'] == astock]["Name"].to_string()
        ret = " ".join(list(filter(None, ret.split(' ')))[1:])
        return ret
    except Exception as e:
        raise ValueError('NotFound.')

def getCompanyName(astock):

    if astock not in getETF("ITOT"):
        if astock in getFromHoldings():
            return "ETF"
        return None

    df = getETF.ret_df["ITOT"]
    try:
        ret = df.loc[df['Ticker'] == astock]["Name"].to_string()
        ret = " ".join(list(filter(None, ret.split(' ')))[1:])
    except Exception as e:
        print ("cname")
        print (str(e))
        if astock in getFromHoldings():
            return "ETF"
        return None
    return ret

#    for etf in getCompanyName.etfs:
#        try : 
#            return getCompanyNameFrom(astock, getETF.ret_df[etf])
#        except:
#            try:
#                getETF(etf)
#                return getCompanyNameFrom(astock, getETF.ret_df[etf])
#            except:
#                pass
#    if astock in getFromHoldings():
#        return "ETF"
#    return None
getCompanyName.etfs = ["IVV", "IWB", "IUSG", "USMV"]

def saveAdded(astock):
    print("astock: {}".format( astock))
    getAdded.added = getp("addedStocks")
    if getAdded.added == None:
        getAdded.added = set()
    getAdded.added.add(astock)
    setp(getAdded.added, "addedStocks")

def getAdded():
    getAdded.added = getp("addedStocks")
    if getAdded.added == None:
        getAdded.added = set()
    return getAdded.added

getAdded.added = list()
toremove = list()
def getProblems():
    global toremove
    getStocks.totalOverride=True
    stocks = getStocks()
    problems = []
    for astock in stocks:
        df = getCsv(astock)
        if df is None:
            toremove.append(astock)
            continue

        vals = []
        for idx in range(len(df)-2):
            start = df.at[idx,"Close"]
            end = df.at[idx+1,"Close"]
            change = start/end
            if change > 5:
                problems.append(astock)
                break
    print(toremove )
    print("problems: {}".format( problems))
    return problems
    
def getStocks(holding = "IVV", andEtfs = True, 
        dev=False, ivv=False, reset = False, noivv = False, 
        simple = False):

    if dev:
#        return getProblems()
        return ["SPY", "BA", "BRO"]

    if not reset:
        try: return getStocks.ret
        except: pass

    if ivv:
        subset = getETF()
        ret = list(subset) + getFromHoldings()
        ret.sort()
        return ret

    val = getStocks.fromCsv
    if val and len(val) == 3:
        path = val[0]
        print("path : {}".format( path ))
        if not os.path.exists(path):
            path = getPath(path)

        if "selection" in path:
            getStocks.ret = fromSelection(path)
            return getStocks.ret

        df = pandas.read_csv(path)
        getStocks.cols = df.columns
        print("getStocks: {}".format( getStocks.cols))
        try:
            getStocks.colname = df.columns[val[1]]
        except:
            getStocks.colname = val[1]
        print("getStocks: {}".format( getStocks.colname))
        df.sort_values(by=getStocks.colname, inplace=True, ascending=val[2])
        getStocks.dataf = df
        retCol = df.columns[0]
        getStocks.ret = df[retCol].tolist()

        ret = df[retCol].tolist()
        ret2 = set()
        if "/" in ret[0]:
            for item in ret:
                ret2.add(item.split("/")[2])
            getStocks.ret = list(ret2)
        else:
            getStocks.ret = df[retCol].tolist()

        cleanUpRet()
        return getStocks.ret

    if getStocks.totalOverride:
        setGetStocksRet(noivv, simple)
        return getStocks.ret

    subset = getETF()
    etfs = ["IWB", "IUSG"]
    ret = subset
    for etf in etfs:
        ret += getETF(etf)
    ret += getFromHoldings()

    getStocks.ret = list(dict.fromkeys(ret))
    cleanUpRet()
    return getStocks.ret

def setGetStocksRet(noivv, simple):
    etfs = ["ITOT"]
    merge = False
    if type(getStocks.totalOverride) == str:
        if "|" in getStocks.totalOverride:
            etfs = getStocks.totalOverride.split("|")
            merge = True
        else:
            etfs = [getStocks.totalOverride]

    thelist = []
    theset = set()
    for etf in etfs:
        path = getPath("holdings/{}_holdings.csv".format(etf))
        tmp = pandas.read_csv(path)
        if merge:
            thelist.append(tmp['Ticker'].tolist())
        else:
            thelist = tmp['Ticker'].tolist()

    if merge:
        thelist = list(set(thelist[0]).intersection(thelist[1]))
            
    if noivv:
        path = getPath("holdings/IVV_holdings.csv")
        ivv = set(pandas.read_csv(path)['Ticker'].tolist())
        return list(set(thelist) - set(ivv))

    if simple:
        getStocks.ret = thelist
    else:
        getStocks.ret = thelist + getFromHoldings() + list(getAdded())

    cleanUpRet()


def cleanUpRet():
    try:
        dels = getp("deletes")
        for item in dels:
            getStocks.ret.remove(item)
    except:
        pass

getStocks.fromCsv = None
getStocks.colname = None
getStocks.totalOverride = True
#setGetStocksRet(noivv=False, simple=True)
#raise SystemExit

def fromSelection(path):
    df = pandas.read_csv(path)
    getStocks.cols = df.columns
    fromSelection.cdict = dict()
    fromSelection.ddict = dict()
    for idx in df.index:
        if fromSelection.mode in df.at[idx,unnamed]:
            ticker = df.at[idx,"Ticker"]
            fromSelection.cdict[ticker] = df.at[idx,"DollarChange"]
            dates = df.at[idx,"PurchaseDates"].split(" ")
            fromSelection.ddict[ticker] = dates
    getStocks.colname = fromSelection.mode.split("/")[0]
    sorted_x = sorted(fromSelection.cdict.items(), 
            key=operator.itemgetter(1),
            reverse = True)
    ret = []
    for item in sorted_x:
        ret.append(item[0])
    return ret
fromSelection.ddict = dict()
fromSelection.mode = "Vari/True"

#path = getPath("history/selection_standard_3.csv")
#fromSelection(path)
#raise SystemExit


#print (len(getStocks()))
#raise SystemExit

def getSortVec():
    return ["Last", "Dip", "Range", "WC", "Vari2"]

def getSortDisplay():
    from termcolor import colored
#    ret = getStocks.cols.tolist()[1:5]
    ret = getSortVec()
#    del ret["Discount"]
    for i, b in enumerate(ret):
        if getStocks.colname == b:
            color = colored("<{}>".format(b),"green") 
            ret[i] = color
    return " ".join(ret)

#getStocks.fromCsv = ("holdings/IVV_holdings.csv", 4, True)
#getStocks.fromCsv = ("holdings/IVV_holdings.csv", "Weight (%)", True)
#print (getStocks())
#raise SystemExit

def setWhatToBuy(column, ascending = True):
    try: 
        if not setWhatToBuy.fromfile:
            setWhatToBuy.fromfile = getp("buyfile")
    except Exception as e:
        print ("setWhatToBuy")
        print (str(e))
    if not column:
        getStocks.fromCsv = None
        return
    getStocks.fromCsv = (setWhatToBuy.fromfile, column, ascending)
setWhatToBuy.fromfile = None

yf.pdr_override() # <== that's all it takes :-)
def getNumberOfDates():
    try : return getNumberOfDates.ret
    except : pass

    try:
        path = getCsv("SPY", asPath = True)
        getNumberOfDates.ret = sum(1 for line in open(path)) - 1
    except:
        path = getCsv("BA", asPath = True)
        getNumberOfDates.ret = sum(1 for line in open(path)) - 1
    return getNumberOfDates.ret

#expected_count = 1050
removed = []
def getRemovedStocks():
    return removed

import z
from datetime import date, timedelta
def saveProcessedFromYahoo(astock, add=False):
    if not saveProcessedFromYahoo.download:
        return

    try:
        if astock in getp("deletes"):
            return
    except:
        pass

    global removed
    path = z.getCsv(astock, asPath = True)
    if os.path.exists(path) and z.getCsv.csvdir != "csv":
        return

    if not astock.isalpha():
        return

    df = None

    saveStartDate = "2000-01-05"
    if z.getCsv.csvdir == "csv":
        saveStartDate = date.today() - timedelta(days=60)

    try:
        df = pdr.get_data_yahoo([astock], start=saveStartDate)
    except Exception as e:
        print (str(e))
        try:
            df = pdr.get_data_yahoo([astock], start=saveStartDate)
        except Exception as e:
            print (str(e))

    if df is None:
#        delStock(astock)
        print ("problem with {}; did not save".format(astock))
        removed.append(astock)
        return

    for idx in df.index:
        if df.at[idx, "Volume"] == "0":
            print ("corrupt data ".format(astock))
            removed.append(astock)
            return

        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            df.at[idx, label] = round(df.at[idx, label], 4)

    print ("saved {}".format(astock))
    df.to_csv(path)
    return path
saveProcessedFromYahoo.download = False
#    try : trimStock(astock, getTrimStock(astock))
#    except: pass

#    if add:
#        saveAdded(astock)

#    return df

#    avg.append(round(sub/4, 4))
#    df.insert(loc=4, column='Avg', value=avg)
#    return df

def getMinimizedVector(values):
    try:
        factor = getFactors(values)
    except:
        factor = 1

    score, dipScore = getScore(values)
    discount = getDiscount(values)
    combined = round(score/dipScore,4)
    final = round((combined / (discount*discount)) * factor)
    dipScore = round(dipScore,3)
    return [final, dipScore]

def writeMinimizedReport(stocks, directory = "report"):
    percent_list = {}
    for astock in stocks:
        path = getPath("csv_mini/{}.csv".format(astock))
        df = pandas.read_csv(path)
        values = df[CsvColumn].tolist()
        percent_list[astock] = getMinimizedVector(values)
    writeFile(percent_list, ["Final", "Dip"], directory, 
            name="minimal_report")

baseline = []
def getPointsAbove(items):
    total = len(items)
    lastpart = int(total/5)*4
    last = items[-1]
    points = 0
    bonus = 1
    below = 0

    higherPoints = 0
    for i,item in enumerate(items):
        s = last/item
        try:
            b = baseline[i]
        except:
            continue

        if s > b:
            if i > lastpart:
                bonus = 1.07
            points += (s-b) * bonus
        elif s < b:
            below += b-s
    return round(points,3), round(below,2)
#print (getPointsAbove(getTestItems(300)))

endDate = ""
startDate = ""
def getEndDate():
    return endDate

def getStartDate():
    return startDate

numberOfDates = 0
def loadBaseline(end = None, start=None):
    global baseline, endDate, numberOfDates, startDate
    df = getCsv(EtfBaselineTicker)
    df = df[start:end]

    lasti = len(df)-1
    endDate = df.at[lasti,'Date']
    startDate = df.at[0,'Date']

    values = df[CsvColumn].tolist()
    numberOfDates = len(values)
    last = values[-1]
    ret = []
    for b in values:
        ret.append(round(last/b,3))
    baseline = ret
    return baseline
#print (loadBaseline())

loadedDivs = dict()
def getDividend(astock, lastvalue, json_dict):
    global loadedDivs
    if not loadedDivs:
        loadedDivs = loadDivs()

    div = loadedDivs.get(astock, 0)

    dividend_idx = 0
    dividend = 0
    if not div or len(div) < 2:
        try:
            dividend = json_dict[astock][dividend_idx]
        except:
            dividend = 0
    else:
        dividend = "{:.2%}".format(float(div[2])/lastvalue)

    return dividend

#json_dict = getData("gg_json")
#print (getDividend("BLK", 300, json_dict))

def listRightIndex(alist, value):
    return len(alist)- alist[-1::-1].index(value) -1

def targetPrice(items):
    lookrange = items
    count = len(items)
    if count == 0:
        return

    maxv = max(lookrange)
    idx = listRightIndex(items, maxv)

    if idx + 1 >= count-6 and count > 3 :
        return targetPrice(items[:-2])

    newlist = lookrange[idx:]
    minv = min(newlist)
    idx = listRightIndex(newlist, minv)
    newlist = newlist[idx:]
    if len(newlist) > 3:
        return targetPrice(newlist)
    return minv

#path = getPath("csv/GOOG.csv")
#df = pandas.read_csv(path)
#values = df['Avg'].tolist()
#bar = targetPrice(values)
#idx = listRightIndex(values, bar)
#print (df['Date'].tolist()[idx])

def saveTargets():
    setp(targets, "targets")

def setTargetPrice(astock, price):
    global targets
    targets[astock] = price, ""

targets = dict()
def getTargetPrice(astock, end = None, start = None):
    global targets
    if not targets:
        dic = getp("targets")
        if not dic:
            for stock in getStocks():
                path = getPath("csv/{}.csv".format(stock))
                df = pandas.read_csv(path)
                df = df[start:end]

                values = df[CsvColumn].tolist()
                minv = targetPrice(values)
                idx = listRightIndex(values, minv)
                date = df['Date'].tolist()[idx]
                targets[stock] = minv, date
            setp(targets, "targets")
        else:
            targets = dic
    return targets[astock]
#print (getTargetPrice("IVV"))

port = dict()
latestPrices = dict()
def writeDict(port, name):
    path = getPath("{}.csv".format(name))
    with open(path, "w") as f:
        for a in port:
            try:
                what = [a] + port[a]
            except:
                what = [a] + [port[a]]
            value = ",".join(str(x) for x in what)
            f.write(value + "\n")
#d  = {"bar" : ["name", str(2)], "d" : 2}
#writeDict(d, "test")

def updatePort():
    global port
    for astock in port:
        if not type(port[astock]) == list:
            count = port[astock]

            try:
                path = getPath("csv/{}.csv".format(astock))
                df = pandas.read_csv(path)
            except:
                continue
            name = json_util.updateJsonCompany(astock)
            try:
                lasti = len(df)-1
                last = df.at[lasti,CsvColumn]
                port[astock] = [name, round(float(last) * float(count),2)]
            except:
                continue

def getVectorForStrategy(values, astock):
    score, dipScore = getScore(values)
    discount = getDiscount(values)
    highlow, vari, vari2 = getRangedDist(values)
    dipScore = round(dipScore,3)
    pointsabove = 0
    pointsbelow = 0
    if not astock == EtfBaselineTicker:
        pointsabove, pointsbelow = getPointsAbove(values)
    changes = getChanges(values)
    factor = 1
    fd = 1
    if changes:
        factor = round(np.prod(changes),3)
        fd = round(float(factor)/float(discount), 3)
    new = round((((pointsabove-(pointsbelow/3.1415))* fd)/dipScore) + \
            math.sqrt(score), 3)
    wc, probup, wcb = getWC(values)
    return [new, discount, dipScore, highlow, vari, vari2, pointsabove, wc]

def getBuyBackTrack():
    return 180

def saveCsvCache():
    saveProcessedFromYahoo.download = False
    stocks = getStocks()
    for astock in stocks:
        getCsv.savedReads[astock] = getCsv(astock)
    setp(getCsv.savedReads, "allcsvs")
                
def getCsv(astock, asPath=False, save=True):

    if asPath:
        return getPath("{}/{}.csv".format(getCsv.csvdir, astock))

    try:
        if save:
            return getCsv.savedReads[astock]
    except :
        pass

    df = None
    try:
        path = getPath("{}/{}.csv".format(getCsv.csvdir, astock), 
                allowmake = False)
        df = pandas.read_csv(path)
        if df is None:
            return None
    except:
        # allow getCsv to return from specified csv files
        path = getPath(astock, allowmake = False)
        if os.path.exists(path):
            df = pandas.read_csv(path)
            if df is None:
                return None
        else:
            try:
                path = saveProcessedFromYahoo(astock)
                if path:
                    df = pandas.read_csv(path)
                    if df is None:
                        return None
            except Exception as e:
                print (str(e))
                print ("problem with {}".format(astock))
                return None
    if save:
        getCsv.savedReads[astock] = df
    return df
getCsv.csvdir = "historical"
getCsv.savedReads = dict()
skipstock = []

def getEtfQualifications(astock):
    ret = []
    for etf in getCompanyName.etfs:
        subset = getETF(etf)
        if astock in subset: 
            ret.append(etf)
    return ",".join(ret)

def report(stocks, 
        start = None, 
        end = None, 
        reportname="strategy_report_", 
        reportdir = "analysis",
        delete_fail = False):

    global skipstock
    loadBaseline(start=start, end=end)
    percent_list = {}
    ivv = getETF()
    iusg = getETF("IUSG")
    buyList = []
    for astock in stocks:

        if astock in skipstock:
            continue
        df = getCsv(astock)
        if df is None:
            continue

        bar = getStartDate()
        if start and end:
            dist = end - start
            try:
                tstart = list(df["Date"]).index(getStartDate())
            except Exception as e:
#                print ('DateVec: '+ str(e))
#                print("df : {}".format( len(df)))
#                if delete_fail:
#                    delStock(astock)
                continue
            df = df[tstart:tstart+dist]

        values = df[CsvColumn].tolist()

        if df.at[0,'Date'] != getStartDate():
            print ("date problem {}".format(astock))
            continue

        last, lasth, lastl, name = 0,0,0,""
#        lasth = 0
#        lastl = 0
#        name = ""


        lasth = max(df['High'].iloc[-8:])
        lastl = min(df['Low'].iloc[-4:])
        lasti = len(df)-1
        last = df.at[lasti, CsvColumn]

        if "main" in reportname:
            try:
                target, date = getTargetPrice(astock)
                if last > target:
                    notation = ""
                    if astock in ivv:
                        notation = "*"
                    buyList.append(astock + notation)
            except:
                pass


        rangescore = getRangeScore(astock)

        mains = []
        if "main" in reportname:
            if astock in getFromHoldings():
                name = "ETF"
            else:
                name = getEtfQualifications(astock)

            try:
                spdip = getSPDip(df)
            except:
                print ("problem sp with {}".format(astock))
                spdip = "NA"

            mains = [spdip, name]
            if not report.mainupdated:
                report.mainupdated = True
                report.headers.insert(8, "Dip1")
                report.headers.insert(9, "ETF")

        try:
            sub = getVectorForStrategy(values, astock) + \
            mains + [rangescore] + [last, lastl, lasth]
            percent_list[astock] = sub

        except Exception as e:
            print("values : {}".format( len(values)))
            skipstock.append(astock)
            import traceback
            print (traceback.format_exc())
            print ('FailedVec: '+ str(e))
            print (astock)
            raise SystemExit

    if buyList and "main" in reportname and len(buyList) < 30:
        print ("Buy List : {}".format(", ".join(buyList)))

    r_name = "{}{}".format(reportname, getEndDate())
    return writeFile(percent_list, report.headers, 
            reportdir, name = r_name)
report.mainupdated = False
report.headers = ["Score", "Discount", "Dip", 
    "HighLow","Vari", "Vari2", "PointsAbove", "WC", 
    "Range", "Last", "LastL", "LastH"]

def getSPDip(df, start = None, end = None):
    if not start and not end:
        start, end = getDipDates()

    dates = list(df["Date"])
    starti = dates.index(start)
    endi = dates.index(end) if end else starti

    start = df.at[starti,"High"]
    end = df.at[endi,"Low"]
    adjust = df.at[endi,CsvColumn]
    if adjust < end:
        return round(adjust/start,3)
    return round(end/start,3)

def analyzeDrops(df):
    dic = dict()
    for idx in df.index:
        change = round(df.at[idx, CsvColumn]/df.at[idx, "Open"],4)
        dic[df.at[idx, "Date"]] = change
    bar = list(dic.values())
    sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
    print(sorted_x[:5])
    print(sorted_x[-5:])
#    print(sorted_x[:-5])

#    Start : 2007-10-16(153.78)
#    End   : 2009-03-11(72.64)
#df = getCsv("SPY")
#for day in drops:
#    print (formatDecimal(getSPDip(df, start = day)))

#analyzeDrops(df)
#raise SystemExit
#tstart = list(df["Date"]).index("2008-09-29")
#print("tstart : {}".format( tstart ))
#end = list(df["Date"]).index("2009-09-21")
#print("end : {}".format( end ))

@lru_cache(maxsize=6)
def getDipDates(astock = "SPY"):
    df = getCsv(astock)
    df = df[-150:-1]
    highs = df["High"].tolist()
    lows = df["Low"].tolist()
    hv = max(highs)
    lv = min(lows)
    hi = highs.index(hv)
    li = lows.index(lv)
    dlist = list(df['Date'])
    hd = dlist[hi]
    ld = dlist[li]
    return (hd, ld)
#getDipDates()
#raise SystemExit

def getTrimStock(astock):
    try : return getp("trims")[astock]
    except : return None
#print (getTrimStock("VST"))

def delStock(astock, report = True):
    print("Deleting astock: {}".format(astock))
    try: 
        path = getCsv(astock, asPath=True)
        os.remove(path)
    except Exception as e:
        if report:
            print ('FailedDelete: '+ str(e))
    os.system("./scrub.sh {}".format(astock))
    try :
        getStocks.ret.remove(astock)
    except Exception as e:
        print ('Failed Removal from getStocks: '+ str(e))

    dels = getp("deletes") or set()
    dels.add(astock)
    print("astock: {}".format( astock))
    setp(dels, "deletes")

    dels = getp("deletes")
    print(dels )

def resetStock(astock):
    try: 
        path = getCsv(astock, asPath=True)
        os.remove(path)
    except:
        pass

    trims = getp("trims")
    del trims[astock]
    setp(trims, "trims")

    saveProcessedFromYahoo(astock)
    del getCsv.savedReads[astock]

def trimStock(astock, end):
    if not end:
        return
    try:
        path = getCsv(astock, asPath=True)
        os.system("sed -i {},{}d {}".format(2,end, path))
    except:
        print ("Did not trim csv {}".format(path))
        pass

    end = int(end)

    try: trimStock.trims[astock] += end
    except : 
        trimStock.trims = getp("trims")
        try : trimStock.trims[astock] = end
        except : 
            trimStock.trims = dict()
            trimStock.trims[astock] = end

    del getCsv.savedReads[astock]
    setp(trimStock.trims, "trims")
#print (getTrimStock("GOOG"))
#trimStock("VST", 200)
#plot("EXAS")

def getAverageStats(values, interval=3, last=30):
    values = values[-1*last:]
    return dipScore(items, interval=interval, avg=1, retAvg=True)

def getRangeScore(astock, sub=False):
    values = astock
    if type(astock) is str:
        df = getCsv(astock)
        values = df[CsvColumn].tolist()

    ups = []
    downs = []
    minv = 6000 
    maxl = len(values)
    normalized = 1500
    num = 0

    if maxl > normalized:
        num = int((maxl-normalized)/1.618)

    values = values[num:maxl]
    maxl = len(values)
    span = 35
    maxr = int(maxl/(span*3.1415))
    intervals = [i for i in range(1, maxr)]

    mapping = dict()
    mapall = dict()
    for interval in intervals:
        ups = []
        alls = []
        idxspan = 0
        idxspan = interval*span
        for i,end in enumerate(values):
            try:
                start = values[int(i-idxspan)]
            except :
                print ("problem")
                print (values)
                continue
            val = end/start
            if val > 1:
                ups.append(val)
            alls.append(val)

        mapping[idxspan] = round(len(ups)/maxl,3)
        mapall[idxspan] = round(sum(alls)/maxl,3)

    probupsum  = sum(mapping.values())
    percsum  = sum(mapall.values())
    if sub:
        return round(probupsum,3), round(percsum,3)
    return round(probupsum * percsum, 3)


#####
# Cleanse code of items() and use iteritems()
#for  k, v in d.iteritems():
# d = dict(izip(list1, list2))

# d = defaultdict(int)
# for k in ks:
#    d[color] += 1

# d = defaultdict(list)
# for name in ks:
#   k = len(name)
#   d[k].append(name)

# d = ChainMap(dics,)
# namedtuple

#x,y,z= (calc(x) , calc(y), calc(z)

#d = {}
#for k in ks:
#    d[k] = d.get(k, 0) + 1
#print (getCompanyName("GOOG"))
#print (list(getCsv("KO")["Date"]).index("2001-12-28"))
def getPrice(astock, idx=-1):
    df = getCsv(astock)
    if type(idx) == int:
        return df.at[idx,"Close"]
    try:
        idx = list(df["Date"]).index(idx)
    except Exception as e:
        getPrice.noprice.append(astock)
        return None
    return df.at[idx,"Close"]
getPrice.noprice = list()

def calcPortfolio(stocks, idx = -1):
    balance = 0
    printed = False
    for astock in stocks:
        df = getCsv(astock)

        if type(idx) != int:
            idx = list(df["Date"]).index(idx)

        price = df.at[idx,"Open"]
        balance += round(price * stocks[astock], 3)
    return balance

import code, traceback, signal

def debug(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message  = "Signal received : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)

def listen():
    signal.signal(signal.SIGUSR1, debug)  # Register handler


calcPortfolio.latest = None
#df = getCsv("BA")
#print (pandas.Index(df["Date"]).get_loc("2018-12-28"))
#print (list(df["Date"]).index(getStartDate()))
#print (calcPortfolio({"BA":1}, idx = -1))
