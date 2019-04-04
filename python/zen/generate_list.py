import z 
import operator
from random import sample
import dask_help

from collections import OrderedDict
from sortedcontainers import SortedSet
keeping = 12
discardlocation = int(keeping/2)
import csv

def getScore(idxstart, df):
    minid = 10
    realstart = idxstart-15
    dips = 0 
    gains = 0 
    for idx in range(realstart, idxstart):
        bought = df.at[idx,"Close"]
        now = df.at[idx+1,"Close"]
        change = now/bought
        if change < 1:
            dips += 1-change
        else:
            gains += change

    bought = df.at[realstart,"Close"]
    now = df.at[idxstart,"Close"]
    change = now/bought
    s1 = -1
    if change > 1 and dips:
        s1 = ((change-1)*100)/dips

    bought = df.at[idxstart-4,"Close"]
    now = df.at[idxstart-2,"Close"]
    change = now/bought

    s2 = -1
    if change < 1:
        s2 = round((1-change)*gains,3)

    return s1,s2

def process(astock, col, saveprices, datesdict):
    path = z.getPath("{}/{}.csv".format(dask_help.createRollingData.dir, astock))
    for row in csv.DictReader(open(path)):

        cdate = row['Date']
        if saveprices:
            openp = float(row['Open'])
            closep = float(row['Close'])
            setSortedDict.prices[cdate][astock] = [openp, closep]

        try:
            val = float(row[col])
        except Exception as e:
            continue

        try:
            datesdict[cdate].add((val, astock))
        except:
            datesdict[cdate] = SortedSet([(val, astock)])

        if len(datesdict[cdate]) > keeping:
            datesdict[cdate].discard(datesdict[cdate][discardlocation])

from collections import defaultdict
def setSortedDict(usepkl=True, prices_only=False):

    prefix = ""
    final = setSortedDict.final
    if type(z.getStocks.devoverride) == str:
        prefix = z.getStocks.devoverride

    if usepkl:
        print("prefix: {}".format( prefix))
        setSortedDict.prices = z.getp("{}prices{}".format(prefix, 
                                                          final))
        saveEtfPrices.prices = z.getp("etfprices")
        if prices_only:
            return
        setSortedDict.sorteddict = z.getp("{}sorteddict{}".format(
            prefix, final))
        return

    stocks = z.getStocks()
    setSortedDict.sorteddict = defaultdict(dict)
    for i,mode in enumerate(dask_help.getModes()):
        print("mode : {}".format( mode ))
        for astock in stocks:
            process(astock, mode, bool(i==0), setSortedDict.sorteddict[mode])

    print("saving")
    z.setp(setSortedDict.sorteddict, "{}sorteddict{}".format(prefix, final))
    z.setp(setSortedDict.prices, "{}prices{}".format(prefix, final))
    print("done saving")

setSortedDict.final = ""
setSortedDict.sorteddict = None
setSortedDict.prices = defaultdict(dict)

def getSortedStocks(date, mode, howmany = 2, getall = False):
    alist = setSortedDict.sorteddict[mode][date]
    if getall:
        return alist
    if getSortedStocks.get == "both":
        return sample(alist,howmany)
    if getSortedStocks.get == "high":
        return sample(alist[-1*discardlocation:],howmany)
    if getSortedStocks.get == "low":
        return sample(alist[:discardlocation],howmany)
getSortedStocks.get = "both"
#    return [alist[0], alist[1]]

def getEtfPrice(astock, date):
    try:
        return saveEtfPrices.prices[date][astock]
    except:
        print("problem etf date: {}".format( date))
        print("astock: {}".format( astock))
        return None

import random
from random import shuffle
def getPricedStocks(idxdate, price):
    stocks = z.getStocks()
    minprice = price * 10
    maxprice = (price+1) * 10
#    shuffle(stocks)
    ret = list()
    for astock in stocks:
        try:
            cprice = getPrice(astock, idxdate)
        except:
            pass

        if not cprice or random.randint(3, 6) != 5:
            continue

        if minprice < cprice < maxprice:
            ret.append((cprice, astock))

        if len(ret) >= 3:
            return ret

    print("price: {}".format( price))
    print("idxdate: {}".format( idxdate))
    print (len(ret))
    return None
#    raise SystemExit

def getPrice(astock, date, value = 1):
    try:
        return setSortedDict.prices[date][astock][value]
    except Exception as e:
        if astock in z.getEtfList():
            try:
                return saveEtfPrices.prices[date][astock]
            except:
                pass
            return None

        if len(setSortedDict.prices) == 1:
            setSortedDict(prices_only = True)
            return setSortedDict.prices[date][astock][value]

#        print("date: {}".format( date))
#        print("astock: {}".format( astock))
#        print ('problemGetPrices: '+ str(e))
        return None

#z.getStocks.devoverride = "ITOT"
#print (getPricedStocks("2017-01-11", 3))
#raise SystemExit

def saveEtfPrices():
    for astock in z.getEtfList():
        path = z.getPath("{}/{}.csv".format(dask_help.convertToDask.directory, astock))
        for row in csv.DictReader(open(path)):
            cdate = row['Date']
            saveEtfPrices.prices[cdate][astock] = float(row['Close'])
    z.setp(saveEtfPrices.prices, "etfprices")
saveEtfPrices.prices = defaultdict(dict)

# ALGN, HPE
if __name__ == '__main__':
    import datetime
#    saveEtfPrices()
#    z.getStocks.devoverride = "ITOT"
#    setSortedDict(usepkl = False)

    dask_help.convertToDask.directory = "csv"
    dask_help.createRollingData.dir = "csvCalculated"
    setSortedDict.final = "Final"
    z.getStocks.devoverride = "IUSG"
    setSortedDict()
    getSortedStocks.get = "both"
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    print("yesterday : {}".format( yesterday ))
    for i,mode in enumerate(dask_help.getModes()):
        alist = getSortedStocks(yesterday, mode, getall=True)
        for item in alist:
            astock = item[1]
            value = getPrice(astock, yesterday)
            if value < 30:
                print("{} at {}".format(astock, value))
#    alist = getSortedStocks("2019-04-02", "C30", getall = True)
#    print(alist )
