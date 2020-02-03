import z
#import queue
import table_print
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
    score = 0

    mc = buy.getFrom("latestmc", astock)
    if mc > 2000:
        return

    upd, c_close, wcc, lchange, diff, min5, last5, meandrop, dayup, maxup, maxdown, lowFromHigh, high, last = buy.getFrom("recentStats", astock)

    extra = 0
    try:
        y1w2, y1m2, y1l, y1l2 = buy.getYearly2(astock)
        if y1w2 > .95:
            extra += .2
        if y1l > 1:
            extra += .2
        if y1l2 > 1:
            extra += .2
        if y1m2 > 1:
            extra += .2
    except:
        pass

    ivv = buy.getFrom("ivvCompare", astock)
    ivv2 = buy.getFrom("ivvDaily", astock)
    probu =  buy.getLongProbDown(astock)

    try:
        val = ivv if ivv < 1.4 else 1.4 
        score = round(val + ivv2 + probu + dayup + extra, 2)
    except Exception as e:
        score = 0

    buy.addSortedHigh("highscore", round(score,1), astock, keeping = 40)

def procs():
    buy.init()
    stocks = z.getp("listofstocks")
#    stocks = ["BA"]
    for astock in stocks:
        try:
            proc(astock)
        except:
            pass
    bar = buy.getSorted("highscore")
    print("bar : {}".format( bar ))
    z.setp(bar, "highscore")
    buy.multiple("highscore")
    table_print.initiate()

if __name__ == '__main__':
    procs()
