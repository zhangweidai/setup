import z
import rows
import queue
import buy
import sliding
import statistics

debug = None
if debug:
    print ("debugging {}".format(debug))

start = 60
each = 10
istart = -1*start
req = start - 20
dates = z.getp("dates")
que = 12
modme = start - que + 1
iterations = 14
firstdate = dates[istart*iterations]
print("firstdate : {}".format( firstdate ))

def proc(astock):
    closes = sliding.WindowQueue(que)
    lows = sliding.WindowQueue(que, needMin=True)
    mins = list()
    answers = list()
    prevbuy = None
    bought = None
    boughts = list()
    boughts_avgs = list()
    c_close = None
    dailys = list() 

    citerations = iterations
    myfirstdate = firstdate

    # grab a first date that mods into 60
    for i, row in enumerate(rows.getRowsRange(astock, count = 2, date=myfirstdate)):
        pass
    mydate = row['Date']
    while mydate != myfirstdate and citerations > 5:
        citerations -= 1
        myfirstdate = dates[istart*citerations]
        for i, row in enumerate(rows.getRowsRange(astock, count = 2, date=myfirstdate)):
            pass
        mydate = row['Date']

    if mydate != myfirstdate:
        return "NA", "NA", "NA", "NA", "NA"

    for i, row in enumerate(buy.getRows(astock, myfirstdate)):
        try:
            c_low = float(row['Low'])
        except:
            print("no low? astock: {}".format( astock))
            return "NA", "NA", "NA", "NA", "NA"

        date = row['Date']

        if c_close and c_close > c_low:
            daily_low = round(c_low/c_close,3)
            dailys.append(daily_low)

        c_close = float(row[z.closekey])

        closes.add_tail(c_close)
        lows.add_tail(min(c_low, c_close))
        if bought == False and (c_low < prevbuy or c_close < prevbuy):
#            print("date {} buytgt : {} c_low: {} ".format( date, prevbuy, c_low ))
            bought = True

        if closes.full():
            first_close = closes.get()
            lowest = lows.get_minimum()
            chg = round(lowest / first_close,3)
            if chg <= 1:
                mins.append(chg)
            else:
                print ("HUH!?!?!?!")
                exit()

        lenmins = len(mins)
#        if debug:
#            print("{}, lenmins : {} {}".format( i, lenmins , date))
        if lenmins and not lenmins % modme:
            med_15 = statistics.median(mins)
            means = statistics.mean(mins)
            useme = round(min((med_15 , means)),3)
            tgt_15 = round(useme * c_close,2)
            answers.append((useme, tgt_15))
            
            candrop = round(tgt_15/c_close,3)

            if bought == True:
                boughts.append(1)
                if debug:
                    print("yes {} ".format(date))
                boughts_avgs.append(candrop)
            elif bought == False:
                boughts.append(0)
                if debug:
                    print("no {} ".format(date))
                boughts_avgs.append(candrop)

            if debug:
                print("date {} cprice {} {} buytarget:{} can it drop {}".format(date, c_close, "bought" if bought else "nope", tgt_15, z.percentage(candrop)))

            bought = False
            prevbuy = tgt_15
            closes.clear()
            lows.clear()
            mins = list()

#    if len(mins) >= req:
#        med_15 = statistics.median(mins)
#        means = statistics.mean(mins)
#        useme = (med_15 + means) /2
#        tgt_15 = round(useme * c_close,2)
    often = "NA"
    try:
        adl = round((statistics.mean(dailys) + statistics.median(dailys))/2,3)
    except:
        adl = "NA"

    if debug:
        print("boughts: {}".format( boughts))
        print("boughts_avgs: {}".format( boughts_avgs))

    if len(boughts) >= 5:
        often = round(statistics.mean(boughts),3)

    try:
        avgtgt = round(statistics.mean(boughts_avgs) ,3)
        tgt9 = answers[-1][1]
        med9 = answers[-1][0]
        return med9, tgt9, often, adl,  avgtgt
    except:
        print("astock: {}".format( astock))
    return "NA", "NA", "NA", "NA", "NA"


def procs():
    stocks = [debug.upper()] if debug else z.getp("listofstocks")
    low_target = dict()
    for astock in stocks:
        try:
            low_target[astock] = proc(astock)
        except Exception as e:
            z.trace(e)
            pass
    try:
        print("low_target: {}".format( low_target))
        print("            med9, tgt9, often, adl,  avgtgt")
    except:
        pass
    if not debug:
        z.setp( low_target, "low_target")

if __name__ == '__main__':
    procs()
