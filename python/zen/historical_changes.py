import z
import rows
import queue
import buy
import sliding
import statistics
import table_print
from scipy import stats

debug = None
if debug:
    print ("debugging {}".format(debug))

savingallg = False
start = 60
each = 10
istart = -1*start
req = start - 20
dates = z.getp("dates")
days_at_a_time = 5
modme = start - days_at_a_time + 1
iterations = 2
firstdate = dates[-300]
print("firstdate : {}".format( firstdate ))

recovdate = "2020-03-23"
#print("firstdate : {}".format( firstdate ))
#exit()
special = dict()
def proc(astock, days_at_a_time, orderchg):
    global special
    if debug:
        print("days_at_a_time: {}".format( days_at_a_time))

    closes = sliding.WindowQueue(days_at_a_time)
    lows = sliding.WindowQueue(days_at_a_time, needMin=True)
    highs = sliding.WindowQueue(days_at_a_time, needMax=True)

    saved_dates = list()
    lowChanges = list()
    highChanges = list()
    betas = list()
    rc = None
    chgs = list()
    prevclose = None
#    print("firstdate: {}".format( firstdate))
    for i, row in enumerate(buy.getRows(astock, firstdate)):
        try:
            c_low = float(row['Low'])
            c_high = float(row['High'])
            if days_at_a_time == 5:
                betas.append(round(c_high / c_low,4))
            date = row['Date']
            c_close = float(row[z.closekey])
        except:
            print("no low? astock: {}".format( astock))
            return None

        if days_at_a_time == 5 and prevclose:
            chgs.append(round(c_close/prevclose,3))

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
            first_close = closes.get()
            lowest = lows.get_minimum()
            chg = round(lowest / first_close,3)
            lowChanges.append(chg)

            highest = highs.get_maximum()
            chg2 = round(highest / first_close,3)
            highChanges.append(chg2)

            if debug and days_at_a_time == 5:
                print("cdate {} close.get{} lowest:{}".format( date, first_close, lowest, highest))
                print("\tcloses : {}".format( closes.main ))
                print("\tlowes : {}".format( lows.main ))
                print("\thighs : {}".format( highs.main ))
                print("\tLchg : {} Hchg : {}".format( chg, chg2 ))

    try:
        high = max(lowChanges)
    except:
        return None
    low = min(lowChanges)
    m1 = round(statistics.median(lowChanges),3)
    latest_change =  ( closes.main[-1]/ closes.main[-1*days_at_a_time] )
    percentile = round(100 - stats.percentileofscore(lowChanges, latest_change, kind ='strict'),4)

#    if days_at_a_time == 15:
#        print("lowChanges: {}".format( len(lowChanges)))
#        print("lowChanges: {}".format( lowChanges))
#        print("m1 : {}".format( m1 ))

    m2 = round(statistics.median(highChanges),3)
    mh = round((m1 + high )/2,4)
    boughts = [1 if change < m1 else 0 for change in lowChanges]
    bom = round(sum(boughts)/len(boughts),3)

    boughts = [1 if change < mh else 0 for change in lowChanges]
    bomh = round(sum(boughts)/len(boughts),3)

    boc = "NA"
    if orderchg:
        boughts = [1 if change < orderchg else 0 for change in lowChanges]
        boc = round(sum(boughts)/len(boughts),3)

    ab = round(sum(betas)/len(betas),3) if betas else 0
    ratio = round(bomh/(mh*mh*mh),4) if days_at_a_time == 15 else 0
    beta21 = round(m2/m1,4) if days_at_a_time == 15 else 0
    if debug:
        print("ratio : {}".format( ratio ))
        print("beta21 : {}".format( beta21 ))

#    if savingallg and days_at_a_time == 15 and c_close >= 10:
#        buy.addSortedHigh("beta21", beta21, astock, savingall=True)

    if savingallg and days_at_a_time == 15 and c_close >= 5:
        buy.addSortedHigh("median_gains", m2, astock)

    dc = None
    dp = None
    dp2 = None
    if days_at_a_time == 5:
        if debug:
            print("closes: {}".format( closes.main))
        try:
            if args.args.live:
                live = z.getLiveData(astock, key = "price", force = True)
                print("live : {}".format( live ))
                dc =  round(( live / closes.main[-1] ),4)
            else:
                dc = round( closes.main[-1]/ closes.main[-2] ,4)

            dp = round(100 - stats.percentileofscore(chgs, dc, kind ='strict'),1)

            nchgs = [b for b in chgs if b < 1 ]
            if debug:
                print("nchgs : {}".format( nchgs ))
            dp2 = round(100 - stats.percentileofscore(nchgs, dc, kind ='strict'),1)
        except:
            pass

        if debug:
            print("dc : {}".format( dc ))
            print("dp : {}".format( dp ))
            print("chgs: {}".format( chgs))
    return percentile, latest_change, round(m1 * c_close,2), m1, mh, bomh, boc, m2, dc, dp, dp2, beta21, ab, ratio, rc

cats = ["percentile", "change", "targetprice", "med1", "medh", "bomh", "boc", "med2"]
better = set(z.getp("better_etf"))
torys = z.getp("torys")
orders = z.getp("orders")
args = None
def procs(stocks, title, savingall = False, generate = False):
    global args
    try:
        args.args.live
    except:
        import args as args

    global savingallg
    savingallg = savingall
    drop_data = dict()
    for x,astock in enumerate(stocks):
        who = ""
        prev = buy.getFrom("last_prices", astock)
        try:
            order_price = orders[astock][0][1]
            chg = round(order_price / prev,3)
            who = "t" if astock in torys else "p"
        except:
            chg = None

        imbetter = "B" if astock in better else ""
        values = [("stock", astock),("close",prev), ("orderchg", chg), ("better", "{}{}".format(imbetter, who))]

        bar = buy.getFrom("howoftendic", astock, ["NA", "NA", "NA", "NA"])
        values.append(("off5", bar[0]))
        values.append(("off10", bar[1]))
        values.append(("off15", bar[2]))
        values.append(("off20", bar[3]))

        if x == 0:
            table_print.use_percentages.add("orderchg")
            table_print.use_percentages.add("dc")
            table_print.use_percentages.add("recover")
            table_print.use_often.add("off5")
            table_print.use_often.add("off10")
            table_print.use_often.add("off15")
            table_print.use_often.add("off20")

        rc = None

        for days_at_a_time in [5, 15, 30]:
            try:

                if savingall or generate:
                    answer = proc(astock, days_at_a_time, chg)
                    drop_data[(astock, days_at_a_time)] = answer
                    if savingall:
                        continue
                else:
                    answer = buy.getFrom("drop_data", (astock, days_at_a_time))
                rc = answer[-1]

            except Exception as e:
                z.trace(e)
                pass

            if days_at_a_time == 5:
                values.append(("ab", answer[-3]))

            for i,cat in enumerate(cats):
                display = "{}{}".format(days_at_a_time, cat)
                if x == 0 :
                    if "price" not in cat and "percentile" not in cat:
                        if "bo" not in cat :
                            table_print.use_percentages.add(display)
                        else:
                            table_print.use_often.add(display)

#                if debug:
#                    print("display : {}".format( display ))
#                    print("answer : {}".format( answer[i] ))
                values.append((display, answer[i]))

            if days_at_a_time == 5:
                values.append(("dc", answer[-7]))
                values.append(("dp", answer[-6]))
                values.append(("dp2", answer[-5]))

            if days_at_a_time == 15:
                values.append(("ratio21", answer[-4]))
                values.append(("ratio", answer[-2]))


        if not savingall:
            try:
                values.append(("recover", round(prev/rc,3)))
            except:
                print("stocks: {}".format( astock))
                print("answer: {}".format( answer))
                values.append(("recover", "NA"))

            table_print.store(values)

    if savingall:
        z.setp(drop_data, "drop_data")
    else:
        if debug:
            table_print.printTable(title)
        table_print.clearTable()


#    try:
#        print("drop_data: {}".format( drop_data))
#    except:
#        pass
#    if not debug:
#        z.setp(drop_data, "drop_data")
def generate():
    stocks = z.getp("listofstocks")
    procs(stocks, "saveall", True)
#    buy.saveSorted("beta21")
    buy.saveSorted("median_gains")

if __name__ == '__main__':
    import args
#    procs(better, "saveall")
#    table_print.initiate()
#    exit()
#    generate()
#    exit()

#    if args.stocks:
#        debug = args.stocks
    procs(args.stocks, "beta21", generate=True)
    table_print.initiate()
    exit()

#    beta = z.getp("beta21")
#    beta = [item[1] for item in beta]
#    procs(beta,"beta21", generate=True)

    if debug:
        procs([debug],"owned")
        exit()

#    owned = z.getp("ports")
#    procs(owned.keys(),"owned")

#    orders = z.getp("orders")
#    stocks = orders.keys()
#    procs(stocks,"orders")

    procs(better,"better", generate=True)
    table_print.initiate()
#    procs(["VOO", "VUG"],"etfs")


