import z
import queue
import buy
import sliding
import statistics

start = 400
istart = -1*start
dates = z.getp("dates")

def proc(astock, startdate):
    prev_close = None
    closes = sliding.WindowQueue(15)
    lows = sliding.WindowQueue(15, needMin=True)
    mins = sliding.WindowQueue(15, needMin=True)

    c_target = None
    shares_bought = 0
    spent = 0
    days = 0

    for i, row in enumerate(buy.getRows(astock, startdate)):
        c_low = float(row['Low'])
        c_close = float(row[z.closekey])
        c_nclose = float(row['Close'])
        c_date = row['Date']

        if c_close != c_nclose:
            adjust = c_close / c_nclose
            c_low = round(c_low * adjust,2)

        closes.add_tail(c_close)
        lows.add_tail(c_low)

        if c_target and c_target > c_low:
            shares_bought += 1
            spent += c_target
            c_target = None
        else:
            days += 1

        if days >= 50:
            c_target = None
            days = 0

        if closes.full():
            first_close = closes.get()
            lowest = lows.get_minimum()
            chg = round(lowest / first_close,3)
            mins.add_tail(chg)

            if mins.get_size() >= 15:
                if c_target == None:
                    med_15 = statistics.median(mins.main) 
                    med_152 = mins.get_minimum()
                    at = round((med_15 + med_152)/2,3)
                    c_target = round(at * c_close,3)

    if not shares_bought:
        return "NA" 

    value  = shares_bought * c_close
    change = round(value/spent,3)
    return change

def procs():
    stocks = z.getp("listofstocks")
    strat = dict()
    startdate = dates[istart]
    print("startdate : {}".format( startdate ))
    for astock in stocks:
        try:
            strat[astock] = proc(astock, startdate)
        except Exception as e:
            z.trace(e)
            pass
    z.setp(strat, "strat", True)

if __name__ == '__main__':
    procs()
