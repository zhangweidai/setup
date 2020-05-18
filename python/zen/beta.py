import z
#import queue
import buy
#import sliding
#import statistics
import rows

start = 107
istart = -1*start
req = start - 30
dates = z.getp("dates")
print("dates : {}".format( dates[istart] ))
import math
from statistics import mean
from buy import getapd

def halfChange2(changes):
    half = math.ceil(len(changes)/2)
    half1 = changes[:half]
    half2 = changes[-1*half:]
    apd1 = getapd(half1)
    apd2 = getapd(half2)
    return apd1, apd2, round(apd2/apd1,3)


def halfChange(changes):
    half = math.ceil(len(changes)/2)
    half1 = changes[:half]
    half2 = changes[-1*half:]

    av1 = round(mean(half1),3)
    av2 = round(mean(half2),3)
    return av1, av2, round(av2/av1,3)

def proc(astock):
    prev_close = None
    total = 0
    total2 = 0
    count = 0 

    mc = buy.getFrom("latestmc", astock)
#    if mc > 400:
#        print("mc : {}".format( mc ))
#        return

    changes = list()
    pchanges = list()
    prices = list()
    for idx, row in enumerate(rows.getRows(astock, dates[istart])):

#        if not idx % 100:
#            print("idx: {}".format( idx))

        c_close = float(row[z.closekey])
        try:
            change = round(c_close / prev_close,3)
            pchange = (change) if (change > 1) else round(prev_close/c_close,3)

            changes.append(change)
            pchanges.append(pchange)
            prices.append(c_close)

        except:
            prev_close = c_close
            continue

    count = len(changes)
    if c_close <= 4 or count < 90:
        return None

    valu = round(sum(changes)/count,3)
    buy.addSorted("avgchg", valu, astock, keeping = 60)
    be = round(sum(pchanges)/count,3)
    buy.addSorted("beta", be, astock, keeping = 60)
    halfChange(pchanges)
    b1, b2, b3 = halfChange(pchanges)
    d1, d2, d3 = halfChange2(prices)
    values = [
        ("stock", astock),
        ("price", c_close),
        ("mc", mc),
        ("beta", be),
        ("1beta", b1),
        ("2beta", b2),
        (".5beta", b3),
        ("1apd", d1),
        ("2apd", d2), 
        ("capd", d3),
        ("apd", getapd(prices))
    ]
    table_print.store(values)
    table_print.use_percentages = ["apd", "1apd", "2apd", "capd"]
#    table_print.use_percentages = ["beta.1", "beta.2", "davg.1", "davg.2"]

    return None

import table_print
table_print.accurate = 2
proc("BA")
proc("SPG")
proc("IVV")
table_print.initiate()

#avgchg = buy.getSorted("avgchg")
#print("avgchg : {}".format( avgchg ))
#beta = buy.getSorted("beta")
#print("beta : {}".format( beta ))

table_print.printTable("two stock comparison")

exit()

def procs():
    stocks = z.getp("listofstocks")
#    stocks = ['FIT']
    hldic = dict()
    prols = list()
    for astock in stocks:
        try:
            vals = proc(astock)
            sub = 0
            for ba, stock in vals[:3]:
                sub += ba
            bv = sub/3
#            print("bv : {}".format( bv ))
            bad = z.percentage(bv, 2)

            sub = 0
            for ba, stock in vals[-3:]:
                sub += ba
            gv = sub/3
#            print("gv : {}".format( gv ))
            good = z.percentage(gv, 2)
            ratio = round((gv-1)/(1-bv),2)
#            print("ratio : {}".format( ratio ))
            answer = "{}/{}".format(bad, good)
            hldic[astock] = answer.replace('%',""), ratio

        except Exception as e:
            prols.append(astock)
            pass

    z.setp(hldic, "hldic", True)
    if len(stocks) > 10:
        z.setp(hldic, "hldic", True)
        z.setp( buy.getSorted("lowbeta") , "lowbeta")
        z.setp( buy.getSorted("highbeta") , "highbeta")
#    print("prols: {}".format( prols))
#    print("prols: {}".format( len(prols)))

if __name__ == '__main__':
    procs()
