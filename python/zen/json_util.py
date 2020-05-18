import urllib.request, json
from bs4 import BeautifulSoup
import z
import datetime
import buy
import os

def getMarketCapPage(astock):
    addy = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(\
            astock, astock)
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
            print ('Failed1: '+ str(e))
            return None

    return decoded.split("\n")

ttoday = datetime.date.today().day
print("ttoday : {}".format( ttoday ))
tmonth = datetime.date.today().month
print("tmonth : {}".format( tmonth ))

billion = 1000000000
def parsePage(astock, update=False):

    live = None
    if update:
        path = z.getPath("{}/{}.pkl".format("yahoo_mc", astock))
        try:
            t = os.path.getmtime(path)
            csvdate = datetime.datetime.fromtimestamp(t)
            csvday = csvdate.day
            csvmonth = csvdate.month

            if csvday == ttoday and tmonth == csvmonth:
                live = z.getp(astock, override="yahoo_mc")
                update = False
        except Exception as e:
            z.trace(e)
            pass
    else: 
        live = z.getp(astock, override="yahoo_mc")

    if live is None or update:
        print("downloading astock: {}".format( astock))
        live = getMarketCapPage(astock)
        z.setp(live, astock, override="yahoo_mc")
#        live = z.getp(astock, override="yahoo")

#        path = z.getPath("yahoo/{}".format(astock))
#        with open(path,"r") as f:
#            live = f.readlines()
#    lastprice = z.getPrice(astock)
    started = False
    lookingfor = '{{"{}"'.format(astock)
    startprinting = False
    nextone = True
    cap = None
    dividend = None
    pe = None
    beta = None
    change = None
    fcf = None

    for line in live:
        line = line.strip()
        more = line.split(":")
        for i,aline in enumerate(more):

            aline = aline.lower()

            if lookingfor in aline:
                nextone = True

#            elif nextone and "sharesOutstanding" in aline:
#                try:
#                    shares = round(int(more[i+2].split(",")[0])/billion,7)
#                    print("shares : {}".format( shares ))
#                except:
#                    pass
##                    return True

            elif nextone and "marketcap" in aline:
                try:
                    if not cap:
                        cap = round(int(more[i+2].split(",")[0])/billion,5)
                except Exception as e:
                    pass

            elif nextone and "freecashflow" in aline:
                try:
                    if not fcf:
                        fcf = round(int(more[i+2].split(",")[0])/billion,5)
#                    return (cap, beta, pe, dividend, fcf)
                except Exception as e:
                    pass

#            elif nextone and "trailingAnnualDividendYield" in aline:
#                try:
#                    if not dividend:
#                        dividend=float(more[i+2].split(",")[0])
#                except:
#                    pass

#            elif nextone and "dividend" in aline:
#                print("aline: {}".format( aline))

            elif nextone and "dividendyield" in aline:
                try:
                    if not dividend:
                        dividend=float(more[i+2].split(",")[0])
                except:
                    pass


            elif nextone and "beta" in aline:
                try:
                    beta=float(more[i+2].split(",")[0])
                except:
                    pass

            elif nextone and "trailingpe" in aline:
                try:
                    if not pe:
                        pe=round(float(more[i+2].split(",")[0]),2)
                    #return (cap, beta, pe, dividend, fcf)
                except:
                    pass
#                    return True

    if cap:
        return (cap, beta, pe, dividend, fcf)
    print ("didint find cap for {}".format(astock))
    return True

import calendar
import time
from sortedcontainers import SortedSet
def getStocksFromHistorical():
    pattern = "*.csv"
    holds = []
    listOfFiles = os.listdir('../zen_dump/historical')  
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append(entry.split(".")[0])
    return holds


def saveOutstanding(update=False):
    z.getStocks.devoverride = "IVV"
    dictionary = dict()
#    stocks = z.getStocks("ITOT")
#    stocks = getStocksFromHistorical()
    stocks = z.getp("listofstocks")
#    for astock in stocks:
    total_mcsorted = SortedSet()
    for idx, astock in enumerate(stocks):
        if not idx % 100:
            print("idx: {}".format( idx))
        try:
            answer = parsePage(astock, update=update)
            if answer == True and not update:
                answer = parsePage(astock, update=True)
                if answer == True:
                    continue
            dictionary[astock] = answer
            try:
                total_mcsorted.add((answer[0], astock))
            except:
                print("astock: {}".format( astock))
                print("answer: {}".format( answer))
#                raise SystemExit
        except Exception as e:
            print ('saveFailed: '+ str(e))
            z.trace(e)
            print ("Not FIND :" + astock)
            raise SystemExit
            continue

    epoch = int(calendar.timegm(time.gmtime()))
    outname = "{}_outstanding".format(epoch)
    z.setp(dictionary, outname)

    print("update saved : {}".format( outname ))
    outname = "ITOT_total_mcsorted"
    z.setp(total_mcsorted, outname)
    savMCIdx(total_mcsorted)

def savMCIdx(total_mcsorted = None):
    if not total_mcsorted:
        outname = "ITOT_total_mcsorted"
        total_mcsorted = z.getp(outname)

    ITOT_total_mcsorted_idx = list()
    for item in reversed(total_mcsorted):
        ITOT_total_mcsorted_idx.append(item[1])
    z.setp(ITOT_total_mcsorted_idx, "ITOT_total_mcsorted_idx")
#    other(outname)

#raise SystemExit

def other(outname):
    dictionary = z.getp(outname)
    path = z.getPath("analysis/{}outstanding.csv".format(z.getStocks.devoverride))
    with open(path, 'w') as f:
        for key, value in dictionary.items():
            f.write("{},{},{},{},{}\n".format(key, value[0], value[1], value[2], value[3]))

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
            print ('Failed1: '+ str(e))
            return None

    return decoded.split("\n")

def getSymbol(text):
    import re
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
    months = ["Apr", "May"]
    #months = ["Mar"]
    for month in months:
        for i in range(1,30):
    
            # too late
            if month == "Mar" and i <= datetime.datetime.today().day + 1:
                continue

            date = str(i).zfill(2)
            try:
                lines = getDividendSchedule(month, date)
            except:
                continue
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
    cap = float(data[astock]["MktCap"])
    return lastDiv, cap

def saveJsonData(stocks, directory="all"):
    print ("Saving Json Data")

    from sortedcontainers import SortedSet
    data = dict()
    mcs = SortedSet()
    for idx, astock in enumerate(stocks):
        if not idx % 100:
            print("idx: {}".format( idx))

        try:
            dividend, cap = getJsonData(astock)
            data[astock] = [dividend, cap]
            mcs.add((cap, astock))
        except:
            print("astock: {}".format( astock))
            continue

    z.setp(data, "div_mc_dic")
    z.setp(mcs, "mc_set")
    buy.sortedSetToRankDict("latestmc", mcs, reverse=True)
#
#    import pandas
#    df = pandas.DataFrame.from_dict(data, orient = 'index', 
#            columns=["Dividend", "Name"])
#    path = getPath("analysis/json_{}.csv".format(directory))
#    df.to_csv(path)

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

def runmain():
    saveOutstanding(update=True)
    savMCIdx()

def remaining():
    stocks = z.getp("listofstocks")
    data = z.getp("div_mc_dic")
#    m1 = ["COST", "WMT", "NKE", "FB", "MSFT"]
    for astock in stocks:
        try:
            data[astock][1] = round(data[astock][1] / billion, 5)
        except:
            print("\nastock : {}".format( astock ))
            try:
                cap, beta, pe, div = parsePage(astock, update=True)
                data[astock] = [div, cap]
            except:
                pass
    z.setp(data, "div_mc_dict")

def genMCRanking():
    sortedlist = SortedSet()
    stocks = z.getp("div_mc_dict")
    for astock in stocks:
        if astock in ['TMK', 'MCHI', 'WAGE', 'USRT', 'USD', 'VICL', "SPY", "IVV", "VIG"]:
            continue
        sortedlist.add((stocks[astock][1], astock))

    sort = dict()
    savesort = SortedSet()
    for i, pair in enumerate(reversed(sortedlist)):
        astock = pair[1]
        sort[astock] = [stocks[astock][0], i]
        savesort.add((i, astock))

    z.setp(sort, "mcdivdict")
    z.setp(savesort, "mcsortedlist")


import os
def iterateStocks():
    dic = z.getp("mcdivdict")
    stocks = z.getp("listofstocks")
    parent = z.getPath("yahoo_mc")
    data = z.getp("div_mc_dict")
    for astock in stocks:  
        try:
            if dic[astock][1] > 1000:
                continue
        except:
            pass
        fpath = "{}/{}.pkl".format(parent, astock)
        t = os.path.getmtime(fpath)
        csvdate = datetime.datetime.fromtimestamp(t)
        csvmonth = csvdate.month
        if csvmonth != 12:
            continue


#        path = z.getPath("yahoo_mc/{}.pkl".format(astock))
#        if os.path.exists(path):
#            continue
        try:
            print("astock: {}".format( astock))
            cap, beta, pe, div = parsePage(astock, update=True)
            if cap > 10000:
                cap = cap / billion
            data[astock] = [div, round(cap,5)]
        except Exception as e:
#            z.trace(e)
#            print ("roblem")
#            exit()
            pass
    z.setp(data, "div_mc_dict")
    print("data: {}".format( data['NTDOY']))
    print("data: {}".format( data['TM']))
    print("data: {}".format( data['MSFT']))
    print("data: {}".format( data['BA']))
    print("data: {}".format( data['KO']))
    print("data: {}".format( data['X']))
    print("data: {}".format( data['GPRO']))

def updateOldYahoos():
    parent = z.getPath("yahoo_mc")
    listOfFiles = os.listdir(parent)

    data = z.getp("div_mc_dic")
    for entry in listOfFiles:  
        pattern = "*.pkl"
        if fnmatch.fnmatch(entry, pattern):
#            fpath = "{}/{}".format(parent, entry)
#            t = os.path.getmtime(fpath)
#            csvdate = datetime.datetime.fromtimestamp(t)
#            csvmonth = csvdate.month
#            if csvmonth == 11:
#                continue
#
            astock = os.path.splitext(entry)[0]
#            print("fpath : {} {} ".format( fpath, csvdate))
            try:
                cap, beta, pe, div = parsePage(astock)
                if astock == "TM" or astock == "NTDOY":
                    print("{} cap: {}".format( astock , cap))

                data[astock] = [div, round(cap,5)]
            except Exception as e:
#                z.trace(e)
#                exit()
                pass

    z.setp(data, "div_mc_dict")

def parses(stocks, update=True, addone = False):
    print ("Saving Json Data")

    from sortedcontainers import SortedSet
    mcs = SortedSet()
    divdict = dict()
    if addone:
        divdict = z.getp("mcdivdict")
    for idx, astock in enumerate(stocks):
        try:
            cap, beta, pe, div, fcf = parsePage(astock, update=update)
            if not idx % 200:
                print("{} {} {} {} ".format( idx , astock, cap, div ))
            mcs.add((cap, astock))
            divdict[astock] = div, cap, pe
        except Exception as e:
            z.trace(e)
            continue
#
    z.setp(divdict, "mcdivdict")
    if not addone:
        buy.sortedSetToRankDict("latestmc", mcs, reverse=True)

if __name__ == '__main__':
#    updateOldYahoos()
#    iterateStocks()
    stocks = z.getp("listofstocks")
#    stocks = ["BA"]
    parses(stocks, update=True)
#    remaining()

#    print (parsePage("EC"))
#    genMCRanking()
#    runmain()
#    zen.diffOuts()

#    print(parsePage("WTW", update=False))
