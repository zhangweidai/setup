import z
import queue
import buy
import sliding
import statistics

debug = None
#debug = None
if debug:
    print ("debugging {}".format(debug))

start = 60
each = 10
istart = -1*start
req = start - 20
dates = z.getp("dates")
que = 12
firstdate = dates[istart*7]
print("firstdate : {}".format( firstdate ))

def proc(astock):
    prev_close = None
    gains = list()
    closes = list()
    for i, row in enumerate(buy.getRows(astock, firstdate)):
        if i == 0 and row["Date"] != firstdate:
            if debug:
                print ("too new")
            return None

        c_close = float(row[z.closekey])
        if not prev_close:
            prev_close = c_close
        else:
            change = round(c_close/prev_close, 3)
            prev_close = c_close
            gains.append(change)
            buy.addSorted("a", change, i, 10)

        closes.append(c_close)

    sort = buy.getSorted("a")
    highs = list()
    avgs = list()
    for high,idx in sort[-5:]:
        if debug:
            print("idx : {}".format( idx ))
            print("high: {}".format( high))
        try:
            highs.append(high)
            highprice = closes[idx]
        except:
            continue

        try:
            after_changes = [ round(price/highprice,3) for price in closes[idx+1:idx+8] ]
            avgs.append(round(statistics.mean(after_changes),3))
            if debug:
                print("closes : {}".format( closes[idx:idx+7] ))
                print("after_changes : {}".format( after_changes ))
        except:
            pass

    if debug:
        print("avgs: {}".format( avgs))
        print("highs : {}".format( highs ))
    if not highs or not avgs:
        return None

    try:
        hi = round(statistics.mean(highs),3)
        lo = round(statistics.mean(avgs),3)
    except:
        return None
    return hi, lo


def procs():
    stocks = [debug.upper()] if debug else z.getp("listofstocks")
    low_target = dict()
    highs = list()
    lows = list()
    for astock in stocks:
        
        try:
            a,b = proc(astock)
            low_target[astock] = a,b
        except Exception as e:
            print("astock: {}".format( astock))
            continue

        rank =  buy.getMCRank(astock)
        if rank < 1000:
            highs.append(a)
            lows.append(b)

    if highs and lows:
        hi = round(statistics.mean(highs),3)
        lo = round(statistics.mean(lows),3)
        if not debug:
            z.setp(low_target, "prob_drop", True)
        print("hi : {}".format( hi ))
        print("lo : {}".format( lo ))

if __name__ == '__main__':
    procs()
