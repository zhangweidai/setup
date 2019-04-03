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
    path = z.getPath("calculated2/{}.csv".format(astock))
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
def setSortedDict(usepkl=True):

    prefix = ""
    if type(z.getStocks.devoverride) == str:
        prefix = z.getStocks.devoverride

    if usepkl:
        print("prefix: {}".format( prefix))
        setSortedDict.sorteddict = z.getp("{}sorteddict".format(prefix))
        setSortedDict.prices = z.getp("{}prices".format(prefix))
        saveEtfPrices.prices = z.getp("etfprices")
        return

    stocks = z.getStocks()
    setSortedDict.sorteddict = defaultdict(dict)
    for i,mode in enumerate(dask_help.getModes()):
        print("mode : {}".format( mode ))
        for astock in stocks:
            process(astock, mode, bool(i==0), setSortedDict.sorteddict[mode])

    print("saving")
    z.setp(setSortedDict.sorteddict, "{}sorteddict".format(prefix))
    z.setp(setSortedDict.prices, "{}prices".format(prefix))
    print("done saving")

setSortedDict.sorteddict = None
setSortedDict.prices = defaultdict(dict)

def getSortedStocks(date, mode, howmany = 2):
    alist = setSortedDict.sorteddict[mode][date]
    return sample(alist,howmany)

def getEtfPrice(astock, date):
    try:
        return saveEtfPrices.prices[date][astock]
    except:
        print("problem etf date: {}".format( date))
        print("astock: {}".format( astock))
        return None

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
            setSortedDict()
            return setSortedDict.prices[date][astock][value]

        print("date: {}".format( date))
        print("astock: {}".format( astock))
        print ('problemGetPrices: '+ str(e))
        return None

def saveEtfPrices():
    for astock in z.getEtfList():
        path = z.getPath("historical/{}.csv".format(astock))
        for row in csv.DictReader(open(path)):
            cdate = row['Date']
            saveEtfPrices.prices[cdate][astock] = float(row['Close'])
    z.setp(saveEtfPrices.prices, "etfprices")
saveEtfPrices.prices = defaultdict(dict)

# ALGN, HPE
if __name__ == '__main__':
    saveEtfPrices()
#    z.getStocks.devoverride = "ITOT"
#    setSortedDict(usepkl = False)

#    z.getStocks.devoverride = "IJH"
#    setSortedDict(usepkl = False)

#    z.getStocks.devoverride = "IJR"
#    setSortedDict(usepkl = False)
    date = '2001-02-01'
    astock = 'IVV'
    print(getPrice(astock, date))
#    mode = 'C3'
#
#    alist = setSortedDict.sorteddict[mode]
#    print(alist )

#    setSortedDict.sorteddict = None
#    setSortedDict.prices = defaultdict(dict)
#
#    z.getStocks.devoverride = "IVV"
#    setSortedDict(usepkl=False)

#    print(getSortedStocks(date, mode))
#    print(getPrice(astock, date))
