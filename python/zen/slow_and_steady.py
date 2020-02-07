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

def proc(astock):
    prev_close = None
    total = 0
    total2 = 0
    count = 0 

    mc = buy.getFrom("latestmc", astock)
    if mc > 2200:
        return

    buy.clearSorted("hlchg")
    for idx, row in enumerate(rows.getRows(astock, dates[istart])):

#        if not idx % 100:
#            print("idx: {}".format( idx))

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

        prev_close = c_close

        buy.addSorted("hlchg", round(change,3), astock, keeping = 6)

    if c_close > 5 and count > 90:
        buy.addSortedLow("lowbeta", round(total,1), astock, keeping = 30)
        buy.addSortedHigh("highbeta", round(total2,1), astock, keeping = 30)
        return buy.getSorted("hlchg") 
    return None

def procs():
    stocks = z.getp("listofstocks")
    hldic = dict()
    prols = list()
    for astock in stocks:
        try:
            vals = proc(astock)
            sub = 0
            for ba, stock in vals[:3]:
                sub += ba
            bad = z.percentage(sub/3, 2)

            sub = 0
            for ba, stock in vals[-3:]:
                sub += ba
            good = z.percentage(sub/3, 2)
            answer = "{}/{}".format(bad, good)
            hldic[astock] = answer.replace('%',"")

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
