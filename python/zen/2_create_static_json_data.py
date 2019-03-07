import urllib.request, json 
import os
import util

def saveJson(stocks, urlstr, dirstr, removeVec):
    for astock in stocks:
        data = None
        path = util.getPath("{}/{}.json".format(dirstr, astock))
        data = util.loadFromUrl(astock, urlstr)

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
    path = util.getPath("income/{}.json".format(astock))
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

    path = util.getPath("info/{}.json".format(astock))
    info_data = None
    if os.path.exists(path):
        with open(path) as f:
            info_data = json.load(f)

    if not info_data:
        return

    name[astock] = info_data[astock]["companyName"]
    price = float(info_data[astock]["Price"])
    dividends[astock] = round(float(info_data[astock]["LastDiv"])/float(price),4)
#    beta[astock] = round(float(info_data[astock]["Beta"]), 4)
#    capa = int(info_data[astock]["MktCap"])
#    useme = round(capa / 100000,6)
#    cap[astock] = useme
#    if prof == None:
#        pmc[astock] = "NRP"
#    elif useme:
#        pmc[astock] = round(prof / useme, 6)
#    else:
#        pmc[astock] = 0

def saveJsonData(stocks):
    for astock in stocks:
        getJsonData(astock)

    data = dict()
    for astock in stocks:
        try:
            data[astock] = [dividends[astock], name[astock]]
        except:
            pass

    return data

#removeVec = ["CEO", "image", "sector", "exchange", "Changes", "industry", "website"]
util.updateJsonCompany("COST")
#removeVec = []
#saveJson(stocks, "financials/income-statement", "income", removeVec)
#saveFinance(["GOOG", "ZEN"], "company/profile")
#saveFinance(["GOOG", "ZEN"], "company/profile")
