import z
import zen
import statistics
from sortedcontainers import SortedSet
from collections import defaultdict
import csv
import update_history

import os

def etfToDic(directory = "ETF"):
    global dics
    path = z.getPath(directory)  
    etfs = z.getEtfList(buys = True)
    for entry in etfs:
        path = z.getPath("{}/{}.csv".format(directory, entry))
        if not os.path.exists(path):
            print("entry: {}".format( entry))
            df = update_history.getDataFromYahoo(entry, "2010-01-04")
            if df is not None:
                df.to_csv(path)

        for row in csv.DictReader(open(path)):
            date = row['Date']
            try:
                dics[entry][date] = float(row['Close'])
            except:
                dics[entry] = dict()
                dics[entry][date] = float(row['Close'])


#etfToDic("historical")
#z.setp(dics, update_pickle)

dates = z.getp("dates")
#dates = dates[-100:-30]
dlen = len(dates)
endd = -15
start = -170
buyatdic = z.getp("buyatdic")
dics = dict()
def proc(astock, forEtf=False):
    global buyatdic, dics
    drops = SortedSet()
    for i, date in enumerate(dates[start:endd]):
        try:
            cidx = dlen+start-1+i
            eidx = cidx - endd - 1
            date2 = dates[eidx]
            minv = 9000
            try:
                astockdata = dics[astock]
            except:
                path = z.getPath("historical/{}.csv".format(astock))
                if not os.path.exists(path):
                    df = update_history.getDataFromYahoo(astock, "2010-01-04")
                    if df is not None:
                        df.to_csv(path)
                    else:
                        print ("Did not find {}".format(astock))
                        exit()
                for row in csv.DictReader(open(path)):
                    date = row['Date']
                    try:
                        dics[astock][date] = float(row['Close'])
                    except:
                        dics[astock] = dict()
                        dics[astock][date] = float(row['Close'])
                        astockdata = dics[astock]
    
                astockdata = dics[astock]
            for mini in range(cidx, eidx):
                date_other = dates[mini]
                pv = astockdata[date_other]
                if pv < minv:
                    minv = pv
            p1 = astockdata[date]
            p2 = astockdata[date2]
            change = round(minv / p1,4)
            if change < 1.00:
                drops.add(change)
        except Exception as e:
            continue

    if forEtf:
        med = statistics.median(drops)
        avg = statistics.mean(drops)
        buyat = (med + drops[1] + avg)/3
        last = zen.getPrice(astock)
        buyatdic[astock] = ((round(last * buyat, 2), round(last * max(avg, med), 2)))
    else:
        med = statistics.median(drops)
        avg = statistics.mean(drops)
        buyat = (drops[1] + min(med,avg))/2
        try:
            last = zen.getPrice(astock)
            high = round(last * buyat, 2)
            low = round(last * drops[1], 2)
            buyatdic[astock] = (low, high)
        except:
            print("astock: {}".format( astock))
            return

def doetfs():
    update_pickle = "stocks_bigdic_demo"
    dics = z.getp(update_pickle)
    stocks = dics.keys()
    for astock in stocks:
        proc(astock, forEtf=True)
    print("buyatdic: {}".format(buyatdic))
    buyatdic = dict()

#dics = None

#etfs = z.getEtfList(buys = True)
#for astock in stocks:
#    proc(astock)
#
def runmain():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--s', default=None)
    args = parser.parse_args()
    if args.s:
        proc(args.s.upper())
    else:
        dics = z.getp("stocks_bigdic")
        stocks = dics.keys()
        for astock in stocks:
            proc(astock, forEtf=False)


    print("buyatdic: {}".format( buyatdic))
    z.setp(buyatdic, "buyatdic") 

if __name__ == '__main__':
    runmain()

