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

def proc(astock):
    prev_close = None
    total = 0
    total2 = 0
    count = 0 

    mc = buy.getFrom("latestmc", astock)
    if mc > 2000:
        return

    for idx, row in enumerate(rows.getRows(astock, dates[istart])):

        if not idx % 100:
            print("idx: {}".format( idx))

        c_close = float(row[z.closekey])
        try:
            change = c_close / prev_close
        except:
            prev_close = c_close
            continue

        addme = 0
        if prev_close > c_close:
            addme = prev_close - c_close
        else: 
            addme = c_close - prev_close

        total += addme
        total2 += abs(prev_close - c_close)
        count += 1

    if c_close > 5 and count > 90:
        buy.addSortedLow("lowbeta", round(total,1), astock, keeping = 30)
        buy.addSortedHigh("highbeta", round(total2,1), astock, keeping = 30)

def procs():
    stocks = z.getp("listofstocks")
    for astock in stocks:
        try:
            proc(astock)
        except:
            pass
    low = buy.getSorted("lowbeta")
    z.setp(low, "lowbeta")

    high = buy.getSorted("highbeta")
    z.setp(high, "highbeta")

if __name__ == '__main__':
    procs()
