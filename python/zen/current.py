import z
import rows
import queue
import buy
import sliding
import statistics
import table_print
import args
from scipy import stats

debug = None
if debug:
    print ("debugging {}".format(debug))
start = 60
each = 10
istart = -1*start
req = start - 20
dates = z.getp("dates")
days_at_a_time = 22
half = int(days_at_a_time / 2)
iterations = 2
firstdate = dates[-333]
firstdate = "2018-03-23"
recovdate = "2020-03-23"
special = dict()

def percentile(array, flip = False, neg_only=False):
    if neg_only :
        if array[-1] > 1:
            return None
        consideration = array[:-1]
        nchgs = [b for b in consideration if b < 1 ]
        return round(100-stats.percentileofscore(nchgs, array[-1], kind ='strict'),1)

    if not flip:
        return round(100 - stats.percentileofscore(array[:-1], array[-1], kind ='strict'),1)
    return round(stats.percentileofscore(array[:-1], array[-1], kind ='strict'),1)

def proc(astock):
    global special
    if debug:
        print("days_at_a_time: {}".format( days_at_a_time))

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

        closes.add_tail(c_close)
        lows.add_tail(min(c_low, c_close))
        highs.add_tail(max(c_high, c_close))

        if closes.full():

            close_list = list(closes.main)

            first_close = closes.get()
            lowest = lows.get_minimum()
            chg = round(lowest / first_close,3)
            lowChanges.append(chg)

            highest = highs.get_maximum()
            chg2 = round(highest / first_close,3)
            highChanges.append(chg2)

            monthchg = round( closes.main[-1]/ first_close ,3)
            beta = round(highest/lowest,2)

            one_month_changes.append(monthchg)
            betas.append(beta)

            drop_from = round(close_list[-1]/max(close_list[:-1]),3)
            drop_froms.append(drop_from)
            if debug:
                print("drop_from : {}".format( drop_from ))
    
    drop_from = drop_froms[-1]
    drop_from_p = percentile(drop_froms)
    n_one_day_changes_p = percentile(one_day_changes, neg_only=True)
    beta = round(statistics.median(betas),2)

    one_month_negs = sum([1 if change < 1 else 0 for change in one_month_changes])
    pd1 = round(one_month_negs / len(one_month_changes),3)

    m1 = round(statistics.median(lowChanges),3)
    m2 = round(statistics.median(highChanges),3)
    r21 = round(m2/m1,3)
    target = round(c_close * m1,2)
    m30c = round(statistics.median(one_month_changes),3)

    chg30 = one_month_changes[-1]
    chg30p = percentile(one_month_changes, neg_only=True)

    if args.args.bta:
        buy.addPDic(astock, "m1", m1)
        buy.addPDic(astock, "r21", r21)
        buy.addPDic(astock, "beta", beta, True)
        buy.addPDic(astock, "m30c", m30c)
        buy.addPDic(astock, "pd1", pd1, True)
        return

    values = [
    ("stock",astock),
    ("price",c_close),
    ("target",target),
    ("m1",m1,'%'),
    ("m2",m2,'%'),
    ("r21",r21,'%'),
    ("mc", buy.getFrom("latestmc", astock, "")),
    ("beta",beta) ,
    ("chg1",one_day_changes[-1],'%'),
    ("chg1p", n_one_day_changes_p),
    ("dropF",drop_from,'%'),
    ("dropFP",drop_from_p),
    ("pd1",pd1,'o'),
    ("chg30",chg30, '%'),
    ("chg30p",chg30p),
    ("m30c",m30c, '%')  
    ]

    if not args.args.bta:
        values.append(("bta", buy.getFrom("savePsdic", astock)))
    table_print.store(values)

def procs(astocks = None):
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
            proc(astock)
        except Exception as e:
            print("problem astock: {}".format( astock))
            z.trace(e)
            pass

if __name__ == '__main__':
    table_print.mode = 1
    procs()
    table_print.initiate()
    if args.args.bta:
        buy.savePs()
