import math
import z
import util
from sortedcontainers import SortedSet
import os
import buy
import statistics

dates = z.getp("dates")
years = -1*252*3
start = dates[years]
ago500 = dates[-504]
ago200 = dates[-200]
ago190 = dates[-190]
ago100 = dates[-100]
print("ago190 : {}".format( ago190 ))
print("ago100 : {}".format( ago100 ))
print("ago500 : {}".format( ago500 ))
ago5 = dates[-13]
close = z.closekey
length = 252

def genUlt():
    stocks = z.getp("listofstocks")
#    ago500 = dates[-30]
    savedic = dict()

    avg30c = SortedSet()
    avg30 = SortedSet()
    worst30c = SortedSet()
    prices = list()
    for idx, astock in enumerate(stocks):
#        if astock != "NTDOY":
#            continue

        if not idx % 100:
            print("idx: {}".format( idx))


        changes = list()
        seen = list()
        first = None
        for i, row in enumerate(buy.getRows(astock, start)):
            if i  == 0:
                first = row
            c_close = float(row[z.closekey])
            seen.append(c_close)
            if len(seen) > length:
                change1year = round(c_close/seen[i-length],3)
                if change1year > 2.5:
                    change1year = 2.5
                changes.append(change1year)

        try:
            y1l = changes[-1]
        except:
            y1l = "NA"
            
        try:
            y1m = statistics.median(changes)
            y1w = min(changes)
            score = (y1w*2)+y1m
            avg30.add((score,astock))
        except Exception as e:
            y1m = "NA"
            y1w = "NA"

        try:
            mcrank = buy.getMCRank(astock)
            if int(mcrank) < 420 or c_close >= 200:
                avg30c.add((score,astock))
                worst30c.add((y1l,astock))
        except:
            prices.append(c_close)
            pass

        savedic[astock] = [y1w, y1m, y1l]

    z.setp(avg30[-30:], "avg30", printdata = True)
    z.setp(avg30c[-30:], "avg30c", printdata = True)
    z.setp(worst30c[:30], "worst30c")
    z.setp(worst30c[-30:], "best30c")
    z.setp(savedic, "annuals");


def dosomething():
    savedSort = SortedSet()
    low_high_sort = SortedSet()
    stocks = z.getp("listofstocks")
    for idx,astock in enumerate(stocks):

        if not idx % 100:
            print("idx: {}".format( idx))

        try:
            mcrank = buy.getMCRank(astock)
            if int(mcrank) > 1234:
                continue

            ago500_price = buy.getPrice(astock, ago500)
            ago200_price = buy.getPrice(astock, ago200)
            ago5_price = buy.getPrice(astock, ago5)
            last = buy.getPrice(astock)
            change1 = round(ago5_price/ago500_price,3)

            ago190_price = buy.getPrice(astock, ago190)
            changelow = round(ago190_price/ago500_price,3)
            if changelow < 0.80:
                change2 = round(last/ago190_price,3)
                if change2 > 1.1 and change2 < 4:
                    change2  = math.sqrt(change2)
                    score = (changelow * 3) - (change2-1)
                    low_high_sort.add((score, astock))

            if change1 > 4 or change1 < 1:
                continue

            if int(mcrank) > 720:
                continue

            change2 = round(last/ago5_price,3)
            if change2 < .825 or change2 > 1:
                continue
            score = round((change1) + (1-change2) * 1.41,5)
            savedSort.add((score, astock))
        except Exception as e:
            pass

    print("savedSort : {}".format( savedSort[-30:] ))
    z.setp(savedSort[-30:], "gained_discount");

    print("lowhighSort : {}".format( low_high_sort[:30] ))
    z.setp(low_high_sort[:30], "low_high_sort");
#    print("savedSort : {}".format( savedSort[:2] ))
#        z.breaker(5)

def delstock(astock):
    try:
        data = z.getp("div_mc_dict")
        del(data[astock])
        z.setp(data, "div_mc_dict")
    except:
        pass

    import split_data
    afile = z.getPath("historical/{}.csv".format(astock))
    if os.path.exists(afile):
        os.remove(afile)
    for afile in buy.getFiles(astock):
        if os.path.exists(afile):
            os.remove(afile)
            print("afile : {}".format( afile ))
    split_data.setlistofstocks()

if __name__ == '__main__':
#    dosomething()
    delstock("ROX")
#    genUlt()

