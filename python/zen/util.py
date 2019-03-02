import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import pandas
import fnmatch
import datetime
import fix_yahoo_finance as yf
from pandas_datareader import data as pdr

def getTestItems():
    return [807.0,811.84,803.19,807.6025,807.0,811.84,803.19,808.38,807.6025, 807.0,811.84,803.19,808.38,807.6025,807.0,811.84,803.19,807.6025]

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
    rs = r_value**2
    normalized_err = (std_err/sub)
    if normalized_err == 0:
        normalized_err = 0.0001
    score = rs/normalized_err
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
#            print (currentStack)
            start = (max(list(currentStack)[:3]))
            end = (min(list(currentStack)[-3:]))
            tdip = (end/start)
            if tdip < 1:
                dip = (1-tdip)
                dips.append(dip)
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
    path = "{}/analysis/{}.csv".format(os.getcwd(), filename)
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

#    if "new" in directory:
#        directory = "averaged"

    path = "{}/{}/{}.csv".format(os.getcwd(), directory, name.zfill(3))
    df.to_csv(path)
    print ("File Written " + path)


def getDiscount(items):
    idx = -1 * (int(len(items)/4))
    tvec = items[idx:]
    average = sum(tvec)/len(tvec)
    num = (items[-1] + items[-2])/2
    return round(num/average,4)

def getEtfList():
    path = "{}/analysis/ETFList.csv".format(os.getcwd())
    data = pandas.read_csv(path)
    return data['Symbol'].tolist()

def getFromHoldings():
    pattern = "*.csv"  
    holds = []
    listOfFiles = os.listdir('./holdings')  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append(entry.split("_")[0])
    return holds

def getStocks(holding, andEtfs = False, difference = False, dev=False):
    if dev:
        return ["GOOG", "IVV"]

    path = "{}/holdings/{}_holdings.csv".format(os.getcwd(), holding)
    if not holding == "IVV":
        listOfFiles = os.listdir('./holdings')  
        for entry in listOfFiles:  
            if holding in entry:
                path = "{}/holdings/{}".format(os.getcwd(), entry)
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
    global doonce
    for astock in stocks:
        if not astock:
            continue
        path = "{}/{}/{}.csv".format(os.getcwd(), directory, astock)
        data = None
        print (path)
#        if doonce:
#            doonce = False
        try:
            data = pdr.get_data_yahoo([astock], start=startdate, end=str(datetime.date.today().isoformat()))
        except Exception as e:
            try:
                data = pdr.get_data_yahoo([astock], start=startdate, end=str(datetime.date.today().isoformat()))
            except Exception as e:
                print ("Problem  :" + astock)
                print ('Failed: '+ str(e))
                continue

        try:
            data.drop(columns = ["Adj Close", "Volume"], inplace=True)
        except:
            print ("Problem with {}".format(astock))
            continue
    
        for idx,row in data.iterrows():
            for label in ["Open","Close", "High", "Low"]:
                data.at[idx, label] = round(data.at[idx, label], 4)
    
        path = "{}/{}/{}.csv".format(os.getcwd(), directory, astock)
        data.to_csv(path)

import urllib.request, json

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
    df = pandas.DataFrame.from_dict(data, orient = 'index', columns=["Dividend", "Name"])
    path = "{}/analysis/gg_json_{}.csv".format(os.getcwd(), directory)
    df.to_csv(path)

def getNumberOfDates():
    path = "{}/../new/GOOG.csv".format(os.getcwd())
    num_lines = sum(1 for line in open(path))
    return num_lines-1

#def writeTrainingData1(items, size = 7):
#    currentStack = deque([])
#    low = deque([])
#    dips = []
#    for i,price in enumerate(items):
#        currentStack.append(price)
#
#        if len(currentStack) == size:
##            print (currentStack)
#            list(currentStack)
#
#            currentStack.popleft()

#writeTrainingData1(getTestItems())