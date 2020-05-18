import math
import z
from sortedcontainers import SortedSet
import os
import buy
import statistics

dates = z.getp("dates")
years = -1*252*4
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

def genUlt(stocks = None):

    allofthem = False
    if not stocks:
        stocks = z.getp("listofstocks")
        allofthem = True
#    ago500 = dates[-30]
    savedic = dict()

    avg30c = SortedSet()
    avg30 = SortedSet()
    worst30c = SortedSet()
    prices = list()
    saveme = dict()
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
            try:
                c_close = float(row[z.closekey])
            except:
                continue

            seen.append(c_close)
            if len(seen) > length:
                change1year = round(c_close/seen[i-length],3)
                bar = seen[i-length]
                if change1year > 3.2:
                    change1year = 3.2
                changes.append(change1year)

        try:
            y1l = changes[-1]
        except:
            y1l = "NA"
            
        try:
            y1l2 = changes[-252]
        except:
            y1l2 = "NA"

        try:
            y1m = statistics.median(changes)
            y1w = min(changes)
            score = (y1w*2)+y1m
            avg30.add((score,astock))
        except Exception as e:
            y1m = "NA"
            y1w = "NA"
        try:
            saveme[astock] = min(changes[:-252]) + statistics.median(changes[:-252])
        except:
            pass

        try:
            mcrank = int(buy.getMCRank(astock))
            if (mcrank < 280) or (c_close >= 200 and mcrank < 420):
                avg30c.add((score,astock))
                worst30c.add((y1l,astock))
        except:
            prices.append(c_close)
            pass

        savedic[astock] = [y1w, y1m, y1l, y1l2]

    if allofthem:
        z.setp(avg30[-30:], "avg30")
        z.setp(avg30c[-30:], "avg30c")
        z.setp(worst30c[:40], "worst30c", True)
        z.setp(worst30c[-40:], "best30c")
        z.setp(savedic, "annuals");
        z.setp(saveme, "y1wm2");


HIGHEST = 10000
def dosomething2():
    savedSort = SortedSet()
    low_high_sort = SortedSet()
    stocks = z.getp("listofstocks")
    s1 = SortedSet()
    s2 = SortedSet()
    for idx,astock in enumerate(stocks):
#        print("astock : {}".format( astock ))

        if not idx % 100:
            print("idx: {}".format( idx))

        lowFromHigh = HIGHEST
        high = 0
        for i, row in enumerate(buy.getRows(astock,ago500)):
            try:
                c_high = float(row['High'])
            except:
                continue
            c_low = float(row['Low'])
    
            if i < 450:
                if c_high > high:
                    high = c_high
#                    print("high : {} {}".format( high, row['Date'] ))
                    lowFromHigh = HIGHEST
    
#                if c_high < lowFromHigh:
#                    lowFromHigh = c_high
    
#                if c_low > high:
#                    high = c_low
#                    lowFromHigh = HIGHEST
    
                if c_low < lowFromHigh:
                    lowFromHigh = c_low
#                    print("low : {} {}".format( c_low, row['Date'] ))
#
        try:
            last = float(row[z.closekey])
            h1 = round(lowFromHigh/high,4)
#            highchange = z.percentage(lowFromHigh/high)
#            print("high: {}".format( high))
#            print("last: {}".format( last))
#            lowchange = z.percentage(last/lowFromHigh)
            l1 = round(last/lowFromHigh,4)
        except:
            continue
#        print("lowFromHigh: {}".format( lowFromHigh))
#        print("highchange : {}".format( highchange ))
#        print("lowchange : {}".format( lowchange ))
        s1.add((h1, astock))
        s2.add((l1, astock))

    z.setp(s1, "s1")
    z.setp(s2, "s2")
    
    print (s1[-10:])
    print (s1[:10])
    print (s2[-10:])
    print (s2[:10])

def dosomething3():
    s1 = z.getp("s1")
    s2 = z.getp("s2")
    d1 = dict()
    d2 = dict()
    d3 = dict()
    bar = s1[-1]
    print("bar : {}".format( bar ))
    bar = s1[0]
    print("bar : {}".format( bar ))
    for i, apair in enumerate(s1):
#        if apair[0] > 1:
#            continue
        astock = apair[1]
        d1[astock] = i
        d3[astock] = buy.getMCRank(astock)

    for i, apair in enumerate(reversed(s2)):
        d2[apair[1]] = i

    score = SortedSet()
    for i, apair in enumerate(s1):
        astock = apair[1]
        try:
            one = d1[astock]
            two = d2[astock]
            three = d3[astock]
            if three > 2000 or three < 70:
                continue
#            if astock == "SLS":
#                print("one : {}".format( one ))
#                print("two : {}".format( two ))
#                print("three : {}".format( three ))
            sc = math.log(one) + math.log(two) + math.log(three)
            score.add((sc, astock))
        except:
            pass
#    bar = s2[-1]
#    print("bar : {}".format( bar ))
#    bar = d2['SLS']
#    print("bar : {}".format( bar ))
    print("score: {}".format( score[-30:]))
    print("score: {}".format( score[:30]))
    z.setp(score[:30], "newstuff")



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
    import rows
    try:
        data = z.getp("div_mc_dict")
        del(data[astock])
        z.setp(data, "div_mc_dict")
    except:
        pass

    afile = z.getPath("historical/{}.csv".format(astock))
    if os.path.exists(afile):
        os.remove(afile)
    try:
        for afile in rows.getFiles(astock):
            if os.path.exists(afile):
                os.remove(afile)
                print("removed  : {}".format( afile ))
    except Exception as e:
        z.trace(e)
        print("1problem  : {}".format( afile ))
        pass
    import gbuy
    gbuy.setlistofstocks()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--delete')
    args = parser.parse_args()
    if args.delete:
        delstock(args.delete.upper())
#    else:
    genUlt()
#    dosomething2()
#    dosomething3()
#    dosomething()
#    genUlt(['FAST'])

