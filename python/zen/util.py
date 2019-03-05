import numpy as np
try:
    import matplotlib.pyplot as plt
    from bs4 import BeautifulSoup
except:
    pass
from scipy import stats
import os
import pandas
import datetime
import pickle
import fix_yahoo_finance as yf
#import statistics
from pandas_datareader import data as pdr
import urllib.request, json


def formatDecimal(factor):
    return "{:.2%}".format(factor-1)
#print(formatDecimal(2.93))

def getTestItems(needed = 30, simple = False):
    from math import sqrt
    if simple:
        return [i for i in range(1,needed)]
    return [round(sqrt(i), 2) for i in range(needed)]

def getPath(path):
    path = "{}/../zen_dump/{}".format(os.getcwd(), path)
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)
    return path

def getp(name):
    path = getPath("pkl/{}.pkl".format(name))
    return pickle.load(open(path, "rb"))

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
    addy = "https://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=2019-{}-{}".format(
            month, date)
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
    months = ["Mar"]
    for month in months:
        for i in range(1,30):

            # too late
            if month == "Mar" and i < 5:
                continue

            date = str(i).zfill(2)
            lines = getDividendSchedule(month, date)
            if lines:
                parseDividendHtml(lines)

    path = getPath("divs/div.pkl")
    pickle.dump(divData, open(path, "wb"))
    print ("Saved {} symbols".format(len(divData)))
#saveDivs()
loadedDivs = None

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
#    print (statistics.stdev(dips))
#    print (sum(dips)/len(dips))
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
    import fnmatch
    pattern = "*.csv"  
    holds = []
    listOfFiles = os.listdir('../zen_dump/training_data')  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append(entry)
    return holds
#print (getTrainingTemps())

def getFromHoldings():
    import fnmatch
    pattern = "*.csv"  
    holds = []
    listOfFiles = os.listdir('../zen_dump/holdings')  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append(entry.split("_")[0])
    return holds

def getStocks(holding, andEtfs = False, difference = False, dev=False):
    if dev:
        return ["GOOG", "IVV"]

    path = getPath("holdings/{}_holdings.csv".format(holding))
    if not holding == "IVV":
        listOfFiles = os.listdir('../zen_dump/holdings')  
        for entry in listOfFiles:  
            if holding in entry:
                path = getPath("holdings/{}".format(entry))
                break

    data = pandas.read_csv(path)
    if andEtfs:
        return data['Ticker'].tolist() + getFromHoldings()

    if (difference):
        ivv = set(getStocks("IVV"))
        return list(set(data['Ticker'].tolist()) - ivv)
    return data['Ticker'].tolist()

doonce = True
yf.pdr_override() # <== that's all it takes :-)
def pullNewCsvFromYahoo(stocks, directory="all"):
    startdate = "2017-01-09"
    for astock in stocks:
        if not astock:
            continue
        path = getPath("{}/{}.csv".format(directory, astock))
        data = None
        print (path)

        try:
            data = pdr.get_data_yahoo([astock], start=startdate, 
                    end=str(datetime.date.today().isoformat()))
        except Exception as e:
            try:
                data = pdr.get_data_yahoo([astock], start=startdate, 
                        end=str(datetime.date.today().isoformat()))
            except Exception as e:
                print ("Problem  :" + astock)
                print ('Failed: '+ str(e))
                continue

        try:
            data.drop(columns = ["Adj Close"], inplace=True)
        except:
            print ("Problem with {}".format(astock))
            continue
        for idx,row in data.iterrows():
            for label in ["Open","Close", "High", "Low"]:
                data.at[idx, label] = round(data.at[idx, label], 4)
    
        path = getPath("{}/{}.csv".format(directory, astock))
        data.to_csv(path)


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
startdate = "2017-01-01"
def saveProcessedFromYahoo(astock):

    path = getPath("csv/{}.csv".format(astock), True)
    if os.path.exists(path):
        return

    df = None
    try:
        df = pdr.get_data_yahoo([astock], start=startdate, end=str(tday))
    except:
        try:
            df = pdr.get_data_yahoo([astock], start=startdate, end=str(tday))
        except Exception as e:
            print (str(e))

    if df is None:
        print ("problem with {}".format(astock))
        return

    avg = list()
    df.drop(columns = ["Adj Close"], inplace=True)
    for idx,row in df.iterrows():
        sub = 0
        for label in ["Open", "Close", "High", "Low"]:
            temp = round(df.at[idx, label], 4)
            sub += temp
            df.at[idx, label] = temp
        avg.append(round(sub/4, 4))

    idx = 4
    df.insert(loc=idx, column='Avg', value=avg)

    path = "/mnt/c/Users/Peter/Documents/setup/python/new/{}.csv".format(astock)
    df.to_csv(path)

#saveProcessedFromYahoo("IVV")

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
        values = df['Avg'].tolist()
        percent_list[astock] = getMinimizedVector(values)
    writeFile(percent_list, ["Final", "Dip"], directory, name="minimal_report")

def getPointsAbove(items):
    lastpart = int(len(items)/5)*4
    last = items[-1]
    ret = []
    points = 0
    bonus = 1
    below = 0
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

baseline = []
def setBaselineScores():
    global baseline
    path = getPath("csv/USMV.csv")
    df = pandas.read_csv(path)
    values = df['Avg'].tolist()
    last = values[-1]
    ret = []
    for b in values:
        ret.append(round(last/b,3))
    baseline = ret
#print (setBaselineScores())


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

def getWanted():
    return {"PAYX":65}
#json_dict = getData("gg_json")
#print (getDividend("BLK", 300, json_dict))

