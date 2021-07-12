import z
import queue
import buy
import sliding
import statistics

debug = None
debug = "BA"
if debug:
    print ("debugging {}".format(debug))

start = 60
each = 10
istart = -1*start
req = start - 20
dates = z.getp("dates")
que = 12
firstdate = dates[istart*15]

def proc(astock):
    closes = sliding.WindowQueue(que)
    lows = sliding.WindowQueue(que, needMin=True)
    mins = list()
    answers = list()
    prevbuy = None
    bought = None
    boughts = list()
    c_close = None
    dailys = list() 

    for i, row in enumerate(buy.getRows(astock, firstdate)):
        try:
            c_low = float(row['Low'])
        except:
            print("firstdate: {}".format( firstdate))
            print("astock: {}".format( astock))
            print("no low? astock: {}".format( astock))
            return "NA", "NA", "NA"


        if c_close and c_close > c_low:
            daily_low = round(c_low/c_close,3)
            dailys.append(daily_low)

        c_close = float(row[z.closekey])
        date = row['Date']
#        print("date : {}".format( date ))
#        print("c_close : {}".format( c_close ))

        closes.add_tail(c_close)
        lows.add_tail(min(c_low, c_close))
        if bought == False and (c_low < prevbuy or c_close < prevbuy):
#            print("date {} buytgt : {} c_low: {} ".format( date, prevbuy, c_low ))
            bought = True

        if closes.full():
            first_close = closes.get()
            lowest = lows.get_minimum()
            chg = round(lowest / first_close,3)
            if chg < 1:
                mins.append(chg)

        bar = len(mins)
        if bar and not bar % 52:
#            print("mins: {}".format( mins))
            med_15 = statistics.median(mins)
            means = statistics.mean(mins)
            useme = round(min((med_15 , means)),3)
            tgt_15 = round(useme * c_close,2)
            answers.append((useme, tgt_15))
            
            if bought == True:
                boughts.append(1)
                if debug:
                    print("yes {} ".format(date))
            elif bought == False:
                boughts.append(0)
                if debug:
                    print("no {} ".format(date))
            if debug:
                print("date {} cprice {} {} buytarget:{} can it drop {}".format(date, c_close, "bought" if bought else "nope", tgt_15, z.percentage(round(tgt_15/c_close,3))))

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
    boughtsanswer = "NA"
    try:
        adl = round((statistics.mean(dailys) + statistics.median(dailys))/2,3)
    except:
        adl = "NA"

    if len(boughts) >= 5:
        boughtsanswer = round(statistics.mean(boughts),3)
    try:
        return answers[-1][0], answers[-1][1], boughtsanswer, adl
    except:
        print("astock: {}".format( astock))
    return "NA", "NA", "NA", "NA"


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
    except:
        pass
    if not debug:
        z.setp( low_target, "low_target")

if __name__ == '__main__':
    procs()
