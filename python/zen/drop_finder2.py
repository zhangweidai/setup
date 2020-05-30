import z
import queue
import buy
import sliding
import statistics

start = 60
each = 10
istart = -1*start
req = start - 20
dates = z.getp("dates")
que = 12
firstdate = dates[istart*15]
print("firstdate : {}".format( firstdate ))
def proc(astock):
    closes = sliding.WindowQueue(que)
    lows = sliding.WindowQueue(que, needMin=True)
    mins = list()
    answers = list()
    prevbuy = None
    bought = None
    boughts = list()

    for i, row in enumerate(buy.getRows(astock, firstdate)):
        try:
            c_low = float(row['Low'])
        except:
            print("no low? astock: {}".format( astock))
            return "NA", "NA", "NA"
        c_close = float(row[z.closekey])
        date = row['Date']
#        print("date {} c_low : {} c_close: {} cclose {}".format( date, c_low, c_close, c_cclose ))

        closes.add_tail(c_close)
        lows.add_tail(c_low)
        if bought == False and (c_low < prevbuy or c_close < prevbuy):
            bought = True

        if closes.full():
            first_close = closes.get()
            lowest = lows.get_minimum()
            chg = round(lowest / first_close,3)
            mins.append(chg)

        bar = len(mins)
        if bar and not bar % 52:
            med_15 = statistics.median(mins)
            means = statistics.mean(mins)
            useme = min((med_15 , means))
            tgt_15 = round(useme * c_close,2)
            answers.append((useme, tgt_15))
            
            if bought == True:
                boughts.append(1)
            elif bought == False:
                boughts.append(0)
#            else:
#                print("date {} cprice {} {} {}".format(date, c_close, "bought" if bought else "nope", tgt_15))

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
    if len(boughts) >= 5:
        boughtsanswer = statistics.mean(boughts)
    try:
        return answers[-1][0], answers[-1][1], boughtsanswer
    except:
        print("astock: {}".format( astock))
    return "NA", "NA", "NA"


def procs():
    stocks = z.getp("listofstocks")
#    stocks = ["BA"]
    low_target = dict()
    for astock in stocks:
        try:
            low_target[astock] = proc(astock)
        except Exception as e:
            z.trace(e)
            pass
    z.setp( low_target, "low_target")

if __name__ == '__main__':
    procs()
