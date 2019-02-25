import urllib.request, json 
import stock_analyze
import os

def loadFromUrl(astock, urlstr):
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


def saveJson(stocks, urlstr, dirstr, removeVec):
    for astock in stocks:
        data = None
        path = "{}/{}/{}.json".format(os.getcwd(), dirstr, astock)
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
        else:
            data = loadFromUrl(astock, urlstr)

        if not data:
            continue
        print (astock)

        for item in removeVec:
            if item in data[astock]:
                print ("deleting {}".format(item))
                del data[astock][item]
        try: 
            with open(path, 'w') as outfile:
                json.dump(data, outfile)
        except Exception as e:
            print ('Failed: '+ str(e))

def normalizeDict(dic):
    temp = sum(dic.values())
    if not temp:
        return
    factor=1.0/temp
    for k in dic:
        dic[k] = round(dic[k]*factor*100, 7)

dividends = dict()
cap = dict()
beta = dict()
profit = dict()
pmc = dict()
name = dict()
def getJsonData(astock):
    global dividends, cap, beta, pmc, name
    path = "{}/{}/{}.json".format(os.getcwd(), "income", astock)
    data = None
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)

    prof = None
    if data:
        try:
            prof = float(data[astock]["Gross profit"]['TTM'])
        except:
            pass

    path = "{}/{}/{}.json".format(os.getcwd(), "info", astock)
    info_data = None
    if os.path.exists(path):
        with open(path) as f:
            info_data = json.load(f)

    if not info_data:
        return

    name[astock] = info_data[astock]["companyName"]
    price = float(info_data[astock]["Price"])
    dividends[astock] = round(float(info_data[astock]["LastDiv"])/float(price),4)
    beta[astock] = round(float(info_data[astock]["Beta"]), 4)
    capa = int(info_data[astock]["MktCap"])
    useme = round(capa / 100000,6)
    cap[astock] = useme
    if prof == None:
        pmc[astock] = "NRP"
    elif useme:
        pmc[astock] = round(prof / useme, 6)
    else:
        pmc[astock] = 0

def getAllData(stocks):
    for astock in stocks:
        getJsonData(astock)

#    beta["NORMAL"] = 1
#    normalizeDict(dividends)
#    normalizeDict(beta)
    normalizeDict(cap)
#    normalizeDict(pmc)

    data = dict()
    for astock in stocks:
        try:
            data[astock] = [dividends[astock], pmc[astock], beta[astock], cap[astock], name[astock]]
        except:
            pass

    return data
#print (getJsonData("GOOG"))
    
#saveJson(["GOOG", "ZEN"])
#saveJson(
#stocks = ["GOOG", "ZEN"]
stocks = stock_analyze.getStocks("IVV")
adata = getAllData(stocks)
import pandas
df = pandas.DataFrame.from_dict(adata, orient = 'index', columns=["Dividend", "P:MC(big is good)", "BETA(small)", "MarketCap", "Name"])
path = "{}/analysis/gg_json.csv".format(os.getcwd())
df.to_csv(path)

#removeVec = ["CEO", "image", "sector", "exchange", "Changes", "industry", "website"]
#removeVec = []
#saveJson(stocks, "financials/income-statement", "income", removeVec)
#saveFinance(["GOOG", "ZEN"], "company/profile")
#saveFinance(["GOOG", "ZEN"], "company/profile")
