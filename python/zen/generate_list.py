import z 
import operator
from random import sample
import dask_help

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

#    return round(dips+change,3)
#    return round(dips+change,3)

def getBuyStocks2(idxdate, mode, howmany = 5):
    return z.getEtfList()

def getBuyStocks(idxdate, mode, howmany = 2):
    thedayl=dict()
    thedayll=dict()
    thedays1=dict()
    thedays2=dict()
    for astock in getBuyStocks.stocks:
        df = z.getCsv(astock)
        if df is None:
            print("problem astock: {}".format( astock))
            continue

        df_dates = df["Date"].tolist() 
        try:
            starti = df_dates.index(idxdate)
            if not starti:
                continue
        except Exception as e:
#            print ('port: '+ str(e))
#            print("astock: {}".format( astock))
            continue

        try:
            close = df.at[starti,"Close"]
            if close < 2:
                continue
        except Exception as e:
            print ('port: '+ str(e))
            print("idxdate: {}".format( idxdate))
            print("starti: {}".format( starti))
            print("df: {}".format(len( df)))
            print("df_dates: {}".format(len( df_dates)))
            exit()

        try:
            opened = df.at[starti-3,"Open"]
            changel = round((close/opened) - (close/df.at[starti-8,"Open"])/2,3)
            changell = round(close/opened,3)
            s1,s2 = getScore(starti, df)
        except Exception as e:
            continue

#        if changeh > 1:
#            thedayh[astock] = round(changeh,4)
        if changel < 1:
            thedayl[astock] = round(changel,4)
        if changell < 1:
            thedayll[astock] = round(changell,4)

        thedays1[astock] = s1
        thedays2[astock] = s2

    sorted_xl = sorted(thedayl.items(), key=operator.itemgetter(1))
    sorted_xll = sorted(thedayll.items(), key=operator.itemgetter(1))

    sorted_xs1 = sorted(thedays1.items(), key=operator.itemgetter(1))
    sorted_xs2 = sorted(thedays2.items(), key=operator.itemgetter(1))

    try:
#        if mode == "high":
#            return sample(sorted_xh[-6:],2)
        if mode == "special1":
            return sample(sorted_xs1[-15:],howmany)
        elif mode == "special2":
            return sample(sorted_xs2[-15:],howmany)
        elif mode == "low":
            return sample(sorted_xl[:15],howmany)
        elif mode == "lowlow":
            return sample(sorted_xll[:15],howmany)
    except Exception as e:
        print ('port: '+ str(e))
        print("mode : {}".format( mode ))
        print("idxdate: {}".format( idxdate))
        return []

    print ("shoudlntget here")
    raise SystemExit
getBuyStocks.stocks = []

from collections import OrderedDict
from sortedcontainers import SortedSet
keeping = 4
discardlocation = int(keeping/2)
inputf_dict = dict()
import csv
def process(astock, col, saveprices, datesdict):
    path = z.getPath("calculated/{}.csv".format(astock))
    inputf_dict[astock] = csv.DictReader(open(path))
    inputf = inputf_dict[astock]

    for row in inputf:
        cdate = row['Date']
        try:
            val = float(row[col])
        except Exception as e:
            continue

        if saveprices:
            openp = float(row['Open'])
            closep = float(row['Close'])
            setSortedDict.prices[cdate][astock] = [openp, closep]

        try:
            datesdict[cdate].add((val, astock))
        except:
            datesdict[cdate] = SortedSet([(val, astock)])

        if len(datesdict[cdate]) > keeping:
            datesdict[cdate].discard(datesdict[cdate][discardlocation])

from collections import defaultdict
def setSortedDict():
    stocks = z.getStocks()
    setSortedDict.sorteddict = defaultdict(dict)
    for i,mode in enumerate(dask_help.getModes()):
        print("mode : {}".format( mode ))
        for astock in stocks:
            process(astock, mode, bool(i==0), 
                    setSortedDict.sorteddict[mode])
setSortedDict.sorteddict = None
setSortedDict.prices = defaultdict(dict)

def getSortedStocks(date, mode):
    return setSortedDict.sorteddict[mode][date]

def getPrice(astock, date, value = 1):
    try:
        return setSortedDict.prices[date][astock][value]
    except Exception as e:
        print("date: {}".format( date))
        print("astock: {}".format( astock))
        print ('problemGetPrices: '+ str(e))
        return None

if __name__ == '__main__':
    z.getStocks.devoverride = True
    setSortedDict()
    print(setSortedDict.prices['2019-03-26']['AMD'])
    print(getPrice( 'AMD', '2019-03-26'))
#    print(setSortedDict.sorteddict['Change'])
#    print(len(setSortedDict.sorteddict))
