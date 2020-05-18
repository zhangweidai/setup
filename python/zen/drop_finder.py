import z
import queue
import buy
import sliding
import statistics

start = 50
istart = -1*start
req = start - 20
dates = z.getp("dates")

def proc(astock):
    prev_close = None
    closes = sliding.WindowQueue(9)
    lows = sliding.WindowQueue(9, needMin=True)
    mins = list()

    for i, row in enumerate(buy.getRows(astock, dates[istart])):
        c_low = float(row['Low'])
        c_close = float(row[z.closekey])
        closes.add_tail(c_close)
        lows.add_tail(c_low)

        if closes.full():
            first_close = closes.get()
            lowest = lows.get_minimum()
            chg = round(lowest / first_close,3)
            mins.append(chg)

    if len(mins) >= req:
        med_15 = statistics.median(mins)
        means = statistics.mean(mins)
        useme = (med_15 + means) /2
        tgt_15 = round(useme * c_close,2)
        return useme, tgt_15

def procs():
    stocks = z.getp("listofstocks")
#    stocks = ["BA"]
    low_target = dict()
    for astock in stocks:
        try:
            low_target[astock] = proc(astock)
        except:
            pass
    z.setp( low_target, "low_target")

if __name__ == '__main__':
    procs()
