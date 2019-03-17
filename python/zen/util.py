import numpy as np
import matplotlib.pyplot as plt
import os
import math
import pandas
import datetime
import pickle
import fix_yahoo_finance as yf
import fnmatch
import urllib.request, json
from scipy import stats
from pandas_datareader import data as pdr
from importlib import reload
from termcolor import colored
from collections import deque

CsvColumn = "Close"
EtfBaselineTicker = "SPY"

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
    return [round(sqrt(i), 2) for i in range(1,needed)]

def getPath(path):

    path = "{}/../zen_dump/{}".format(os.getcwd(), path)
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
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
    if len(items) < 18:
        return None
    newlist = items[-18:]
    maxv = max(newlist)
    minv = min(newlist)
    lastitems = items[-1]
    vari = np.var([newlist[0], lastitems, minv, maxv])
    if lastitems == maxv:
        return "{}".format(round(maxv/minv,3)), round(vari,2)
    else:
        first = str(round((lastitems/minv)-1,3))
        second = str(round((maxv/lastitems)-1,3))
        return "{}/{}".format(first, second), round(vari,2)
#print(getRangedDist(getTestItems()))

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

def getiusgstocks(etf = "IUSG"):
    try : return getiusgstocks.ret
    except : pass

    path = getPath("holdings/{}_holdings.csv".format(etf))
    dataivv = pandas.read_csv(path)
    getiusgstocks.ret = set(dataivv['Ticker'].tolist())
    return getiusgstocks.ret

def getivvstocks(etf = "IVV"):
    try : return getivvstocks.ret
    except : pass

    path = getPath("holdings/{}_holdings.csv".format(etf))
    getivvstocks.dataivv = pandas.read_csv(path)
    getivvstocks.ret = set(getivvstocks.dataivv['Ticker'].tolist())
    return getivvstocks.ret

#getivvstocks()
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
    try : 
        return getCompanyNameFrom(astock, getivvstocks.dataivv)
    except:
        getivvstocks()
        try : return getCompanyNameFrom(astock, 
                                        getivvstocks.dataivv)
        except:
            try : return getCompanyNameFrom(astock, 
                                            getStocks.iwb)
            except:
                getStocks()
                try : return getCompanyNameFrom(astock, 
                                                getStocks.iwb)
                except:
                    try : return getCompanyNameFrom(astock, 
                                                    getStocks.iusg)
                    except : 
                        print ("Couldnt find {}".format(astock))
                        pass
    if astock in getFromHoldings():
        return "ETF"
    return None

def diff_IWB_and_IUSG():
    path1 = getPath("holdings/IWB_holdings.csv")
    path2 = getPath("holdings/IUSG_holdings.csv")
    dataiwb = set(pandas.read_csv(path1)['Ticker'].tolist())
    data = set(pandas.read_csv(path2)['Ticker'].tolist())
    return (data-dataiwb)

def saveAdded(astock):
    getAdded.added = getp("addedStocks")
    if getAdded.added == None:
        getAdded.added = list()
    getAdded.added.append(astock)
    setp(getAdded.added, "addedStocks")

def getAdded():
    getAdded.added = getp("addedStocks")
    if getAdded.added == None:
        getAdded.added = list()
    return getAdded.added
getAdded.added = list()

def getStocks(holding = "IVV", andEtfs = True, 
        difference = False, dev=False, ivv=False, reset = False):

    if dev:
        return ["BA", "BRO", "IFF", "MU", "SM", "WCC"]

    if not reset:
        try: return getStocks.ret
        except: pass

    subset = getivvstocks()
    if ivv:
        ret = list(subset) + getFromHoldings()
        ret.sort()
        return ret

    val = getStocks.fromCsv
    if val and len(val) == 3:
        path = val[0]
        if not os.path.exists(path):
            path = getPath(path)
        df = pandas.read_csv(path)
        getStocks.cols = df.columns
        try:
            getStocks.colname = df.columns[val[1]]
        except:
            getStocks.colname = df.columns[0]
        df.sort_values(by=getStocks.colname, 
                inplace=True, ascending=val[2])
        retCol = df.columns[0]
        getStocks.ret = df[retCol].tolist()
        return getStocks.ret

    path = getPath("holdings/IWB_holdings.csv")
    getStocks.iwb = pandas.read_csv(path)
    data1 = set(getStocks.iwb['Ticker'].tolist())

    path = getPath("holdings/IJH_holdings.csv")
    getStocks.ijh = pandas.read_csv(path)
    data3 = set(getStocks.ijh['Ticker'].tolist())

    path2 = getPath("holdings/IUSG_holdings.csv")
    getStocks.iusg = pandas.read_csv(path2)
    data2 = set(getStocks.iusg['Ticker'].tolist())
    ret = list(data1 | data2 | data3 | subset) + getFromHoldings() + \
        getAdded()
    getStocks.ret = ret
    return ret

getStocks.fromCsv = None
getStocks.colname = None

def getSortDisplay():
    ret = getStocks.cols.tolist()[1:7]
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

    path = getCsv("WMT", asPath = True)
    getNumberOfDates.ret = sum(1 for line in open(path)) - 1
    return getNumberOfDates.ret

#expected_count = 1050
removed = []
def getRemovedStocks():
    return removed

def saveProcessedFromYahoo(astock, add=False):
    tday = datetime.date.today().isoformat()
    saveStartDate = "2015-01-05" if getCsv.csvdir == "csv" else "2000-01-05"

    global removed
    path = getCsv(astock, asPath = True)
    if os.path.exists(path):
        return

    if not astock.isalpha():
        return

    df = None
    try:
        df = pdr.get_data_yahoo([astock], start=saveStartDate, end=str(tday),
                pause=0.3, adjust_price=True )
    except Exception as e:
        print (str(e))
        try:
            df = pdr.get_data_yahoo([astock], start=saveStartDate, end=str(tday),
                pause=0.3, adjust_price=True )
        except Exception as e:
            print (str(e))

    if df is None:
        print ("problem with {}; did not save".format(astock))
        removed.append(astock)
        return

    for idx,row in df.iterrows():
        if df.at[idx, "Volume"] == "0":
            print ("corrupt data ".format(astock))
            removed.append(astock)
            return

        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            df.at[idx, label] = round(df.at[idx, label], 4)

    df.to_csv(path)
    try : trimStock(astock, getTrimStock(astock))
    except: pass

    if add:
        saveAdded(astock)

    return df

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
        values = df['Adj Close'].tolist()
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
        b = baseline[i]
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

    endDate = df['Date'].iloc[-1]
    startDate = df['Date'].iloc[0]

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

                values = df['Close'].tolist()
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
                last = df['Close'].iloc[-1]
                port[astock] = [name, round(float(last) * float(count),2)]
            except:
                continue

def getVectorForStrategy(values, astock):
    score, dipScore = getScore(values)
    discount = getDiscount(values)
    distrange, vari = getRangedDist(values)
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
    new = round((((pointsabove-(pointsbelow/3.1415))* fd)/dipScore) + math.sqrt(score), 3)
    wc, probup, wcb = getWC(values)
    return [new, discount, dipScore, vari, pointsabove, pointsbelow, wc]
savedReads = dict()

def getCsv(astock, idx = None, asPath=False):
    if asPath:
        return getPath("{}/{}.csv".format(getCsv.csvdir, astock))

    global savedReads
    if idx == 0:
        idx = "Unnamed: 0"

    df = None
    try:
        if savedReads and (astock in savedReads):
            if idx:
                return df[idx].tolist()
            return savedReads[astock]
    except Exception as e:
        return None

    try:
        path = getPath("{}/{}.csv".format(getCsv.csvdir, astock))
        df = pandas.read_csv(path)
    except:
        # allow getCsv to return from specified csv files
        path = getPath(astock)
        if os.path.exists(path):
            df = pandas.read_csv(path)
        else:
            try:
                df = saveProcessedFromYahoo(astock)
                df.to_csv(path) 
                df = pandas.read_csv(path)
            except Exception as e:
                print (str(e))
                print ("problem with {}".format(astock))
                return None
    savedReads[astock] = df
    if idx:
        return df[idx].tolist()
    return df
getCsv.csvdir = "csv"

def writeStrategyReport(stocks, start = None, end = None, 
        reportname="strategy_report_", reportdir = "analysis"):
    loadBaseline(start=start, end=end)
    percent_list = {}
    ivv = getivvstocks()
    iusg = getiusgstocks()
    buyList = []
    for astock in stocks:
        df = getCsv(astock)

        if df is None:
            continue

        if start and end:
            dist = end - start
            try:
                tstart = list(df["Date"]).index(getStartDate())
            except Exception as e:
#                print ('FailedGet: '+ str(e))
#                print (astock)
                continue
            df = df[tstart:tstart+dist]

        values = df[CsvColumn].tolist()

#        if df['Date'].iloc[0] != getStartDate():
#            continue

        last = 0
        lasth = 0
        lastl = 0
        name = ""
        if astock in getFromHoldings():
            name = "ETF"
        else:
            if astock in ivv:
                name = "ivv"
            if astock in iusg:
                name += "iusg"

        lasth = max(df['High'].iloc[-8:])
        lastl = min(df['Low'].iloc[-4:])
        last = df['Close'].iloc[-1]

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

        try:
            percent_list[astock] = getVectorForStrategy(values, astock) + [name, last, lastl, lasth]
        except Exception as e:
            import traceback
            print (traceback.format_exc())
            print ('FailedVec: '+ str(e))
            

    headers = ["Score", "Discount", "Dip", "Variance", "PointsAbove", 
    "PointsBelow", "WC", "ETF", "Last", "LastL", "LastH"]

    if buyList and "main" in reportname:
        print ("Buy List : {}".format(", ".join(buyList)))

    r_name = "{}{}".format(reportname, getEndDate())
    return writeFile(percent_list, headers, reportdir, name = r_name)

#def plot(astock, start = None, end = None):
#    df = getCsv(astock)
#    df = df[start:end]
#    values = df[CsvColumn].tolist()
#    plt.plot(values)
#    plt.show()
#
def getTrimStock(astock):
    try : return getp("trims")[astock]
    except : return None
#print (getTrimStock("VST"))

def delStock(astock):
    try: 
        path = getCsv(astock, asPath=True)
        os.remove(path)
    except Exception as e:
        print ('FailedDelete: '+ str(e))
    os.system("./scrub.sh {}".format(astock))

def resetStock(astock):
    global savedReads
    try: 
        path = getCsv(astock, asPath=True)
        os.remove(path)
    except:
        pass

    trims = getp("trims")
    del trims[astock]
    setp(trims, "trims")

    saveProcessedFromYahoo(astock)
    del savedReads[astock]

def trimStock(astock, end):
    global savedReads
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

    del savedReads[astock]
    setp(trimStock.trims, "trims")
#print (getTrimStock("GOOG"))
#trimStock("VST", 200)
#plot("EXAS")

def getAverageStats(values, interval=3, last=30):
    values = values[-1*last:]
    return dipScore(items, interval=interval, avg=1, retAvg=True)

#print (getCompanyName("GOOG"))

#print (list(getCsv("KO")["Date"]).index("2001-12-28"))
