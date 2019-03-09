import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from scipy import stats
import os
import pandas
import datetime
import pickle
import fix_yahoo_finance as yf
import fnmatch
#import statistics
from pandas_datareader import data as pdr
import urllib.request, json
csvColumn = "Adj Close"

def formatDecimal(factor):
    return "{:.2%}".format(factor-1)
#print(formatDecimal(2.93))

def getTestItems(needed = 30, simple = False):
    from math import sqrt
    if simple:
        return [1,1,1,1,1,1,1,2,2,2,2,3,3,3,3,3,1,1,1,1,1,1,1,3,4,4,5,5,
        6,6,7,7,7,8,8,7,6,6,5,4,6,5,4,3,9,7,8,9]
    return [round(sqrt(i), 2) for i in range(1,needed)]
#plt.plot(getTestItems(simple=True))
#plt.show()

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

#setp(getTestItems(20), "saved_values")
#items = (getTestItems(2000))
#setp(items, "saved_values")
#items = getp("saved_values")
#print (items)
#getPath("delme/file.csv")        

def getDividendSchedule(month, date):
    addy = "https://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=2019-{}-{}".format(month, date)
    decoded = None
    try:
        with urllib.request.urlopen(addy) as url:
            decoded = BeautifulSoup(url.read(), 'html.parser').get_text()
#                    from_encoding=url.info().getparam('charset')).prettify()
    except:
        try:
            with urllib.request.urlopen(addy) as url:
                decoded = BeautifulSoup(url.read(), 'html.parser').get_text()
        except Exception as e:
            print ('Failed: '+ str(e))
            return None

    return decoded.split("\n")

import re
def getSymbol(text):
    m = re.search(r"\((.*?)\)", text)
    if m:
        return m.group(1)
    return None

divData = dict()
def parseDividendHtml(lines):
    global divData
    symbol = ""
    started = False
    for line in lines:
        line = line.strip()
        if not line:
            symbol = ""
            continue
        
        if "Payment Date" in line:
            started = True
            continue

        if started and "Previous" in line:
            break

        if not started:
            continue

        if symbol:
            divData.setdefault(symbol, list())
            if len(divData[symbol]) < 4:
                divData[symbol].append(line)
        else:
            symbol = getSymbol(line)

        if ' </tr>' in line:
            symbol = ""
#path = getPath("divs/Mar_01.html")
#parseDividendHtml(path)

def saveDivs():
    months = ["Mar", "Apr"]
    #months = ["Mar"]
    for month in months:
        for i in range(1,30):

            # too late
            if month == "Mar" and i <= datetime.datetime.today().day + 1:
                continue

            date = str(i).zfill(2)
            lines = getDividendSchedule(month, date)
            if lines:
                parseDividendHtml(lines)

    path = getPath("divs/div.pkl")
    pickle.dump(divData, open(path, "wb"))
    print ("Saved {} symbols".format(len(divData)))

#saveDivs()

def loadDivs():
    path = getPath("divs/div.pkl")
    return pickle.load(open(path, "rb"))
#loadDivs()

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

#def get3DayLow(items, idx):
#    size = len(items)
#    if idx + 3 >= size:
#        idx = size - 3
#    low = items[idx]
#    for i in range(1,3):
#        print (i)
#        if items[idx+i] < low:
#            low = items[idx+i]
#    return low
#print (get3DayLow(getTestItems(), 20))

from collections import deque
def dipScore(items):
    SIZE = 7
    currentStack = deque([])
    low = deque([])
    dips = []
    for i,price in enumerate(items):
        currentStack.append(price)
        if len(currentStack) == SIZE:
            start = (max(list(currentStack)[:3]))
            end = (min(list(currentStack)[-3:]))
            tdip = (end/start)
            if tdip < 1:
                dips.append(1-tdip)
            currentStack.popleft()
    return round(sum(dips),6)
#print (dipScore(getTestItems()))

import math
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

def getData(filename, asList = False):
    path = filename
    if not os.path.exists(filename):
        path = getPath("analysis/{}.csv".format(filename))

    if not os.path.exists(path):
        print ("could not find" + path)
        return None

    trend = pandas.read_csv(path)
    whatdict = trend.to_dict('split')
    ret = dict()
    if not asList:
        for company_data in whatdict['data']:
            ret[company_data[0]] = company_data[1:]
    else:
        ret = list()
        for company_data in whatdict['data']:
            ret.append(company_data)

    return ret

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
                return

    print ("File Written " + path)


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

etfs = None
def getFromHoldings():
    global etfs
    if etfs:
        return etfs
    pattern = "*.csv"  
    holds = []
    listOfFiles = os.listdir('../zen_dump/holdings')  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append(entry.split("_")[0])
    etfs = holds
    return holds

subset = list()
def getivvstocks():
    global subset
    if not subset:
        path = getPath("holdings/IVV_holdings.csv")
        dataivv = pandas.read_csv(path)
        subset = set(dataivv['Ticker'].tolist())
    return subset

def getStocks(holding = "IVV", andEtfs = True, difference = False, dev=False, ivv=False):
    if dev:
        return ["GOOG", "IVV"]

    subset = getivvstocks()
    if ivv:
        return list(subset) + getFromHoldings()

    path = getPath("holdings/IWB_holdings.csv")
    dataiwb = pandas.read_csv(path)

    removed = getp("removedstocks")
    ret = list(subset | set(dataiwb['Ticker'].tolist()) ) + getFromHoldings()
    ret = set(ret) - set(removed)
    return list(ret)

#    if not holding == "IVV":
#        listOfFiles = os.listdir('../zen_dump/holdings')  
#        for entry in listOfFiles:  
#            if holding in entry:
#                path = getPath("holdings/{}".format(entry))
#                break
#
#    data = pandas.read_csv(path)
#    if andEtfs:
#        return data['Ticker'].tolist() + getFromHoldings()
#
#    if (difference):
#        ivv = set(getStocks("IVV"))
#        return list(set(data['Ticker'].tolist()) - ivv)
#    return data['Ticker'].tolist()

yf.pdr_override() # <== that's all it takes :-)

def loadFromUrl(astock, urlstr = "company/profile"):
    decoded = None
    try:
        with urllib.request.urlopen(
                "https://financialmodelingprep.com/api/{}/{}".format(urlstr, 
                    astock)) as url:
            decoded = url.read().decode()
    except Exception as e:
        print ("Not FIND :" + astock)
        print ('Failed: '+ str(e))

    if not decoded:
        return None

    return json.loads(decoded.replace("<pre>",""))


def getJsonData(astock):
    data = loadFromUrl(astock)
    if not data:
        return None, None
    price = float(data[astock]["Price"])
    lastDiv = round(float(data[astock]["LastDiv"])/float(price),4)
    name = data[astock]["companyName"]
    return lastDiv, name

def saveJsonData(stocks, directory="all"):
    print ("Saving Json Data")
    print (stocks)

    data = dict()
    for astock in stocks:
        dividend, name = getJsonData(astock)
        if name:
            data[astock] = [dividend, name]

    import pandas
    df = pandas.DataFrame.from_dict(data, orient = 'index', 
            columns=["Dividend", "Name"])
    path = getPath("analysis/json_{}.csv".format(directory))
    df.to_csv(path)

def getNumberOfDates():
    path = getPath("csv/GOOG.csv")
    num_lines = sum(1 for line in open(path))
    return num_lines-1

tday = datetime.date.today().isoformat()
startdate = "2015-01-05"
expected_count = 1050
removed = []
def getRemovedStocks():
    return removed

def saveProcessedFromYahoo(astock):
    global removed
    path = getPath("csv/{}.csv".format(astock))
    if os.path.exists(path):
        return

    df = None
    try:
        df = pdr.get_data_yahoo([astock], start=startdate, end=str(tday))
    except Exception as e:
        print (str(e))
        try:
            df = pdr.get_data_yahoo([astock], start=startdate, end=str(tday))
        except Exception as e:
            print (str(e))

    if df is None:
        print ("problem with {}; did not save".format(astock))
        removed.append(astock)
        return

    count = len(df)
    if count != expected_count:
        print ("not enough data for {} {} ".format(astock, str(count)))
        removed.append(astock)
        return

#    avg = list()
#    df.drop(columns = ["Adj Close"], inplace=True)
    for idx,row in df.iterrows():
        if df.at[idx, "Volume"] == "0":
            print ("corrupt data ".format(astock))
            removed.append(astock)
            return

        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            df.at[idx, label] = round(df.at[idx, label], 4)
    df.to_csv(path)
    return df
#        avg.append(round(sub/4, 4))

#    df.insert(loc=4, column='Avg', value=avg)
#    return df
#saveProcessedFromYahoo("AMD")

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

#def getNumberOfDates():
#    return numberOfDates

def loadUSMV_dict(end = None, start=None):
    global baseline, endDate, numberOfDates, startDate
    path = getPath("csv/IUSG.csv")
#    path = getPath("csv/USMV.csv")
    df = pandas.read_csv(path)
    df = df[start:end]

    endDate = df['Date'].iloc[-1]
    startDate = df['Date'].iloc[0]

    values = df[csvColumn].tolist()
    numberOfDates = len(values)
    last = values[-1]
    ret = []
    for b in values:
        ret.append(round(last/b,3))
    baseline = ret
    return baseline
#print (loadUSMV_dict())


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

def getWanted():
    return {"PAYX":65}

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

def loadFromUrl(astock, urlstr = "company/profile"):
    decoded = None
    try:
        with urllib.request.urlopen("https://financialmodelingprep.com/api/{}/{}".format(urlstr, astock)) as url:
            decoded = url.read().decode()
    except Exception as e:
        print ("Not FIND :" + astock)
        print ('Failed: '+ str(e))

    if not decoded:
        return None

    return json.loads(decoded.replace("<pre>",""))

def updateJsonCompany(astock):
    data = getData("gg_json")
#    data = loadFromUrl(astock)
    if data is None:
        return ""
    try:
        return data[astock][1]
    except:
        pass
    return ""

    price = float(data[astock]["Price"])
    dividend = round(float(data[astock]["LastDiv"])/float(price),4)
#    with open(path, "a") as f:
#        f.write("{},{},{}\n".format(astock, dividend, name))
    return name


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

            name = updateJsonCompany(astock)
            try:
                last = df['Close'].iloc[-1]
                port[astock] = [name, round(float(last) * float(count),2)]
            except:
                continue

def getVector(values, dividend, name, astock, last):
    score, dipScore = getScore(values)
    discount = getDiscount(values)
    distrange, vari = getRangedDist(values)
    dipScore = round(dipScore,3)

    pointsabove = 0
    pointsbelow = 0
    if not astock == "IUSG":
        pointsabove, pointsbelow = getPointsAbove(values)

    changes = getChanges(values)
    factor = "NotEnoughData"
    fd = 1
    if changes:
        factor = round(np.prod(changes),3)
        fd = round(float(factor)/float(discount), 3)

#    discount = formatDecimal(discount)

    new = round((((pointsabove-(pointsbelow/3.1415))* fd)/dipScore) + 
            math.sqrt(score), 3)

    wc, probup, wcb = getWC(values)
#    for i,b in enumerate(changes):
#        changes[i] = formatDecimal(b)

    date = ""
#    target, date = getTargetPrice(astock, end)
    target = targetPrice(values)
#    target = "{}({})".format(target, date)

    if astock in subset:
        name = "**" + name

    return [name, new, discount, dipScore, target, last, dividend, 
    distrange, vari, pointsabove, pointsbelow, wc, probup, wcb] + changes

def writeDropCsv(stocks, directory = "analysis", start = None, end = None):
    global port

    name_idx = 1
    etfs = getFromHoldings()

    #global percent_list, notinvested
    percent_list = {}
    json_dict = getData("gg_json")
    if json_dict is None:
        return

    portkeys = []
    if not end:
        import portfolio
        port = portfolio.getPortfolio()
        portkeys = port.keys()
    start_str = "{}_".format(getStartDate())
    end_str = "_{}".format(getEndDate())
    for astock in stocks:

        path = getPath("csv/{}.csv".format(astock))
        try:
            df = pandas.read_csv(path)
        except:
            try:
                df = saveProcessedFromYahoo(astock)
            except Exception as e:
                print (str(e))
                print ("problem with {}".format(astock))
                continue
        df = df[start:end]
        values = df[csvColumn].tolist()
        if len(values) < 200:
#            print ("Can't do {} with {}".format(astock, str(end)))
            continue

        last = 0
        if start == None and end == None: 
            last = df['Close'].iloc[-1]
            latestPrices[astock] = last

#        values = values[:-46]
        dividend = getDividend(astock, values[-1], json_dict)

        try:
            name = json_dict[astock][name_idx]
        except:
            name = ""
            if astock in etfs:
                last = df['Close'].iloc[-1]
                name = "ETF"

        if astock in portkeys:
            value = round(port[astock] * float(last),3)
            port[astock] = [name, value]

        percent_list[astock] = getVector(values, dividend, name, astock, last)

    headers = ["Name", "Score", "Discount", "Dip", 
               "Target", "Last", "Dividend", "DistRange", "Variance", 
               "PointsAbove", "PointsBelow", "WC", 
               "ProbUp", "WCBad", 
               "3", "6", "12", "24", "48", "96", "192", "384"]

    r_name = "on_{}{}".format(on_type, end_str)
    if end == None and start == None:
        updatePort() 
        writeDict(port, "Portfolio")
        setp(latestPrices, "latestValues")
        r_name = "complete_report"
    writeFile(percent_list, headers, directory, name = r_name)

def getVectorForStrategy(values, astock):
    score, dipScore = getScore(values)
    discount = getDiscount(values)
    distrange, vari = getRangedDist(values)
    dipScore = round(dipScore,3)
    pointsabove = 0
    pointsbelow = 0
    if not astock == "IUSG":
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

def writeStrategyReport(stocks, start = None, end = None):
    percent_list = {}
    for astock in stocks:
        path = getPath("csv/{}.csv".format(astock))
        try:
            df = pandas.read_csv(path)
        except:
            try:
                df = saveProcessedFromYahoo(astock)
            except Exception as e:
                print (str(e))
                print ("problem with {}".format(astock))
                continue
        df = df[start:end]
        values = df[csvColumn].tolist()
        if len(values) < 200:
            continue

        last = 0
        lasth = 0
        lastl = 0
        name = ""
        if astock in getFromHoldings():
            name = "ETF"
        lasth = max(df['High'].iloc[:7])
        lastl = min(df['Low'].iloc[:3])
        last = df['Close'].iloc[-1]

        percent_list[astock] = getVectorForStrategy(values, astock) + [name, last, lastl, lasth]

    headers = ["Score", "Discount", "Dip", "Variance", "PointsAbove", 
    "PointsBelow", "WC", "ETF", "Last", "LastL", "LastH"]

    r_name = "strategy_report_{}".format(getEndDate())
    writeFile(percent_list, headers, "analysis", name = r_name)
#updateJsonCompany("COST")
