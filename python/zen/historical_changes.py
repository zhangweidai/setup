import z
import rows
import queue
import buy
import sliding
import statistics
import table_print

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

def proc(astock, days_at_a_time, orderchg):
    if debug:
        print("days_at_a_time: {}".format( days_at_a_time))

    closes = sliding.WindowQueue(days_at_a_time)
    lows = sliding.WindowQueue(days_at_a_time, needMin=True)
    highs = sliding.WindowQueue(days_at_a_time, needMax=True)

    lowChanges = list()
    highChanges = list()
    betas = list()
    rc = None
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

        if debug and i == 0:
            print("first date:{}  c_close: {}".format( date, c_close ))

        if date == recovdate:
            rc = c_close

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

    high = max(lowChanges)
    low = min(lowChanges)
    m1 = round(statistics.median(lowChanges),3)
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

    if savingallg and days_at_a_time == 15 and c_close >= 10:
        buy.addSortedHigh("beta21", beta21, astock, savingall=True)

    return low, m1, mh, bomh, boc, m2, beta21, ab, ratio, rc

cats = ["low", "med1", "medh", "bomh", "boc", "med2"]
better = set(z.getp("better_etf"))
torys = z.getp("torys")
def procs(stocks, title, savingall = False):
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
        table_print.use_percentages.append("orderchg")
        table_print.use_percentages.append("recover")

        rc = None

        for days_at_a_time in [5, 15, 30]:
            try:

                if savingall:
                    answer = proc(astock, days_at_a_time, chg)
                    drop_data[(astock, days_at_a_time)] = answer
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
                    if "bo" not in cat :
                        table_print.use_percentages.append(display)
                    else:
                        table_print.use_often.append(display)

#                if debug:
#                    print("display : {}".format( display ))
#                    print("answer : {}".format( answer[i] ))
                values.append((display, answer[i]))

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
    buy.saveSorted("beta21")

if __name__ == '__main__':
#    procs(better, "saveall")
#    table_print.initiate()
#    exit()
#    generate()
#    exit()

    beta = z.getp("beta21")
    beta = [item[1] for item in beta]
    procs(beta,"beta21")
    table_print.initiate()
    exit()

    if debug:
        procs([debug],"owned")
        exit()

    owned = z.getp("ports")
    procs(owned.keys(),"owned")

    orders = z.getp("orders")
    stocks = orders.keys()
    procs(stocks,"orders")

    procs(better,"better")
    procs(["VOO", "VUG"],"etfs")


    table_print.initiate()
