import math
import z
import util
from sortedcontainers import SortedSet
import os
import buy
import statistics

dates = z.getp("dates")
years = -1*252*2
start = dates[years]
close = z.closekey
indicator_leng = 60
totalconsideration = indicator_leng * 2
#stopdate = dates[-1*totalconsideration]

ivvdict = dict()

def genUlt(stocks = None):
#    retdict = dict()
    ud_dict = dict()
    for idx, astock in enumerate(stocks):
        if not idx % 100:
            print("idx: {}".format(idx))

        seen = list()
        ups = list()
        downs = list()
        for i, row in enumerate(buy.getRows(astock, start)):


            try:
                c_close = float(row[z.closekey])
                cdate = row['Date']
            except:
                continue

            seen.append(c_close)
            if len(seen) > totalconsideration:
                starting = i-(indicator_leng*2)
                dayslater = starting + indicator_leng
                firstval = seen[starting]
                second = seen[dayslater]

                change = round(second/firstval, 3)
                change2 = round(c_close/second, 3)
                if change >= 1.06:
                    ups.append(change2)
                elif change <= 0.98:
                    downs.append(change2)

#                retdict[cdate] = change

#            if cdate == stopdate:
#                break
        u = None
        d = None
        l = None
        try:
            if len(ups) > 10:
                u = round(statistics.mean(ups),3)
        except:
            pass

        try:
            if len(downs) > 10:
                d = round(statistics.mean(downs),3)
        except:
            pass

        try:
            l = round(seen[-1] / seen[-60],3)
        except:
            pass

        ud_dict[astock] = u,d,l

    z.setp(ud_dict, "ud_dict")
#        return retdict

def compare(stocks):
    retdict = dict()
    for idx, astock in enumerate(stocks):
        seen = list()
        for i, row in enumerate(buy.getRows(astock, start)):
            try:
                c_close = float(row[z.closekey])
                cdate = row['Date']
            except:
                continue
            seen.append(c_close)
            if len(seen) > length:
                change = round(c_close/seen[i-length],3)
                retdict[cdate] = change

            if cdate == stopdate:
                break

        return retdict


if __name__ == '__main__':
#    genUlt(["IVV"])
    stocks = z.getp("listofstocks")
    genUlt(stocks)
#    print("ivvdict : {}".format( ivvdict ))
#    compare(['KO', 'OXY'])
#    genUlt(["KO"])
