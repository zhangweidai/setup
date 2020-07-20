
debug = None
import numpy as np
import z
import rows
import queue
import buy
import sliding
import statistics
import table_print
from scipy import stats
import args

if debug:
    print ("debugging {}".format(debug))
start = 60
each = 10
istart = -1*start
req = start - 20
dates = z.getp("dates")
days_at_a_time = 22
months6 = days_at_a_time * 6

half = int(days_at_a_time / 2)
iterations = 2
firstdate = "2018-03-23"
recovdate = "2020-03-23"
special = dict()

def percentile(array, flip = False, neg_only=False):
    if neg_only :
        consideration = array[:-1]

        if array[-1] < 1:
            nchgs = [b for b in consideration if b < 1 ]
            return round(100-stats.percentileofscore(nchgs, array[-1], kind ='strict'),1)
        else:
            nchgs = [b for b in consideration if b > 1 ]
            return round(stats.percentileofscore(nchgs, array[-1], kind ='strict'),1)

    if not flip:
        return round(100 - stats.percentileofscore(array[:-1], array[-1], kind ='strict'),1)

    return round(stats.percentileofscore(array[:-1], array[-1], kind ='strict'),1)

recent_size = 4
def proc(astock, title):
    global special
    if debug:
        print("days_at_a_time: {}".format( days_at_a_time))

    closes6m = sliding.WindowQueue(months6)

    closes = sliding.WindowQueue(days_at_a_time)
    changes = sliding.WindowQueue(days_at_a_time)
    lows = sliding.WindowQueue(days_at_a_time, needMin=True)
    highs = sliding.WindowQueue(days_at_a_time, needMax=True)

    saved_dates = list()
    betas = list()
    rc = None
    prevclose = None

    betas = list()
    one_day_changes = list()
    lowChanges = list()
    highChanges = list()
    one_month_changes = list()
    drop_froms = list()
    one_year_changes = list()
    month6_changes = list()

    mc = buy.getFrom("latestmc", astock, 9999)
    bta = args.args.bta

    for i, row in enumerate(buy.getRows(astock, firstdate)):
        try:
            c_low = float(row['Low'])
            c_high = float(row['High'])
            date = row['Date']
            c_close = float(row[z.closekey])
        except:
            print("no low? astock: {}".format( astock))
            return None

        if prevclose:
            one_day_changes.append(round(c_close/prevclose,3))

        prevclose = c_close

        if debug and i == 0:
            print("first date:{}  c_close: {}".format( date, c_close ))

        if date == recovdate:
            rc = c_close
        saved_dates.append(date)

        if bta and mc < 1500 and mc > 500:
            closes6m.add_tail(c_close)

        closes.add_tail(c_close)
        lows.add_tail(min(c_low, c_close))
        highs.add_tail(max(c_high, c_close))

        if closes6m.full():
            first_close = closes.get()
            chg = round(c_close / first_close,3)
            month6_changes.append(chg)

        if closes.full():

            close_list = list(closes.main)

            first_close = closes.get()
            lowest = lows.get_minimum()
            chg = round(lowest / first_close,4)
            lowChanges.append(chg)

            highest = highs.get_maximum()
            chg2 = round(highest / first_close,4)
            highChanges.append(chg2)

            monthchg = round( closes.main[-1]/ first_close ,3)
            beta = round(highest/lowest,2)

            one_month_changes.append(monthchg)
            betas.append(beta)

            drop_from = round(close_list[-1]/max(close_list[:-1]),3)
            drop_froms.append(drop_from)
#            if debug:
#                print("drop_from : {}".format( drop_from ))
    

    closes_list = list(closes.main)
    lows_list = list(lows.main)

    if args.args.live:
        live_price = z.getLiveData(astock, key = "price")
        one_day_changes.append(live_price/c_close)

        month_ago = list(closes.main)[-22]
        one_month_changes.append(live_price/month_ago)
        closes_list.append(live_price)
        lows_list.append(live_price)

    items = list()
    for i, close in enumerate(closes_list):
        consideration = closes_list[i:i+recent_size]
        consider2 = lows_list[i:i+recent_size]
        if len(consideration) == recent_size:
            chg = round(min(consider2)/ consideration[0],3)
            items.append(chg) 

    if month6_changes:
        buy.addSortedHigh("m6_m_m", statistics.median(month6_changes), astock, keeping = 40)

    try:
        rm1 = statistics.median(items)
    except:
        return

    drop_from = drop_froms[-1]
    drop_from_p = percentile(drop_froms)
    drop_from_p = drop_from_p if drop_from_p > 75 else None

    n_one_day_changes_p = percentile(one_day_changes, neg_only=True)
    n_one_day_changes_p = n_one_day_changes_p if n_one_day_changes_p > 75 else None
    beta = round(statistics.median(betas),2)

    one_month_negs = sum([1 if change < 1 else 0 for change in one_month_changes])
    pd1 = round(one_month_negs / len(one_month_changes),3)

    more20d = sum([1 if change < .80 else 0 for change in one_month_changes])

    wc1 = min(lowChanges)
    m1 = round(statistics.median(lowChanges),4)
    m2 = round(statistics.median(highChanges),4)
    r21 = round((((m2-1)*100)+(m1-1)*100),4)
    target = round(c_close * m1,2)
    m30c = round(statistics.median(one_month_changes),3)

    p20 = round(float(np.percentile(lowChanges, 20)),3)

    chg30 = one_month_changes[-1]
    chg30p = percentile(one_month_changes, neg_only=True)
    chg30p = chg30p if chg30p > 75 else None

    if bta:
        buy.addPDic(astock, "m1", m1)
        buy.addPDic(astock, "more20d", more20d)
        buy.addPDic(astock, "wc1", wc1)
        buy.addPDic(astock, "p20", p20)
        buy.addPDic(astock, "r21", r21)
#        buy.addPDic(astock, "beta", beta, True)
        buy.addPDic(astock, "m30c", m30c)
        buy.addPDic(astock, "pd1", pd1, True)
        return


    values = [
    ("stock",astock),
    ("price",c_close),
    ("target",target),
    ("m1",m1,'%'),
    ("rm1",rm1, '%'),
    ("m2",m2,'%'),
    ("r21",r21),
    ("wc1",wc1,'%'),
    ("p20",p20,'%'),
    ("more20d",more20d),
    ("mc", mc),
    ("beta",beta) ,
    ("chg1",one_day_changes[-1],'%'),
    ("chg1p", n_one_day_changes_p),
    ("dropf",drop_from,'%'),
    ("dropfp",drop_from_p),
    ("pd1",pd1,'o'),
    ("chg30",chg30, '%'),
    ("chg30p",chg30p),
    ("m30c",m30c, '%'),
    ("owned", buy.getFrom("ports",astock)) 
    ]

    try:
        order = buy.getFrom("orders", astock)[0]
        order,value = order[1], round(order[0])
        ochg = order/c_close
        values.insert(3, ("ochg", ochg, "%"))
        values.insert(4, ("value", value))
        loc = "_TO" if astock in z.getp("torys") else "_PO"
        values.append(("location", loc))
    except Exception as e:
        loc = ""
        ochg = "NA"
        value = "NA"
        values.insert(3, ("ochg", ochg, "%"))
        values.insert(4, ("value", value))
        values.append(("location", loc))

#        order = buy.getFrom("orders", astock)
#        print("order : {}".format( order ))
#        print("astock: {}".format( astock))
#        exit()

    if args.came_from_list:
        values.append((args.args.stocks, args.came_from_dict[astock], "%"))

    if not args.args.bta:
        values.append(("bta", buy.getFrom("savePsdic", astock)))
    table_print.store(values)

def procs(astocks = None, title = None):
    if astocks:
        import sys
        current_module = sys.modules[__name__]
        current_module.stocks = astocks
    try:
        args.args.live
    except:
        import args as args

    for x,astock in enumerate(stocks):
        try:
            proc(astock, title)
        except Exception as e:
            print("problem astock: {}".format( astock))
            z.trace(e)
            pass

    if args.args.bta:
        buy.saveSorted("m6_m_m")


if __name__ == '__main__':
    procs()
    if not debug:
        print ("NOT DEBUGGING")
        table_print.initiate()
        if args.args.bta:
            buy.savePs()
