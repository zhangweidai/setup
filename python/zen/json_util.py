from util import *
import urllib.request, json
from bs4 import BeautifulSoup
import z

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

billion = 1000000000
def parsePage(astock, dateformc, live=False):

    if live:
        live = getMarketCapPage(astock)
        z.setp(live, astock, override="yahoo")
    else:
        live = z.getp(astock, override="yahoo")
#        path = z.getPath("yahoo/{}".format(astock))
#        with open(path,"r") as f:
#            live = f.readlines()
    lastprice = z.getPrice(astock, dateformc, orlatest=True)
    started = False
    lookingfor = '{{"{}"'.format(astock)
    for line in live:
        line = line.strip()
        more = line.split(":")
        startprinting = False
        nextone = True
        shares = None
        cap2 = None
        for i,aline in enumerate(more):
            if lookingfor in aline:
                nextone = True
            elif nextone and "sharesOutstanding" in aline:
                shares = round(int(more[i+2].split(",")[0])/billion,5)
                cap2 = round(shares * lastprice, 5)
            elif nextone and "marketCap" in aline:
                cap = round(int(more[i+2].split(",")[0])/billion,5)
                return (shares, cap, cap2)


def saveOutstanding():

    import generate_list
    z.getStocks.devoverride = "IUSG"
    generate_list.setSortedDict(prices_only=True)
#    stocks = z.getStocks("IUSG")
    dictionary = dict()
    dateformc = z.getLatestDate(etf="IUSG", final="")
    for astock in ["KO"]:
        try:
            dictionary[astock] = parsePage(astock, dateformc)
        except Exception as e:
            print ('saveFailed: '+ str(e))
            print ("Not FIND :" + astock)
            continue
    z.setp(dictionary, "outstanding")
    print(dictionary)

#saveOutstanding()
#raise SystemExit

def other():
    dictionary = z.getp("outstanding")
    path = z.getPath("analysis/outstanding.csv")
    with open(path, 'w') as f:
        for key, value in dictionary.items():
            value = round(value/billion, 4)

            f.write("{},{},{}\n".format(key, value))

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

if __name__ == '__main__':
    saveOutstanding()
