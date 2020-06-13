# how often does it beat ivv given 50 days? 
# how often is 1 year up?
import z
import queue
import buy
import sliding
import statistics

debug = None
debug = "UBER"

start = 650
istart = -1*start
req = start - 20
dates = z.getp("dates")

sdate = dates[istart]

def getetfChanges():
    changes = list()
    closes_50 = sliding.WindowQueue(50)
    for i, row in enumerate(buy.getRows("IVV", sdate)):
        c_close = float(row[z.closekey])
        closes_50.add_tail(c_close)
        if closes_50.full():
            changes.append(round(closes_50.main[-1]/closes_50.main[0], 3))
    return changes

etfchanges = getetfChanges()
#print("etfchanges : {}".format( etfchanges ))

def proc(astock):
    prev_close = None
    closes_252 = sliding.WindowQueue(252)
    ups = list()
    beativv = list()

    closes_50 = sliding.WindowQueue(50)
    etf_idx = 0

    firstdate = None
    index_adjust = 0
    for i, row in enumerate(buy.getRows(astock, sdate)):

        # adjust for first available date
        if i == 0:
            index_adjust = dates.index(row['Date']) - dates.index(sdate)

        c_close = float(row[z.closekey])
        closes_50.add_tail(c_close)
        closes_252.add_tail(c_close)

        # ive got a year worth of closes_252
        if closes_50.full():
            annual_change = round(closes_50.main[-1]/closes_50.main[0],3)
            if debug:
                date = row["Date"]
                print("etf_idx : {} date : {} annual_change : {} close : {}".format( etf_idx, date, annual_change, c_close ))
            try:
                beativv.append(1 if annual_change >= etfchanges[etf_idx + index_adjust] else 0)
            except:
                pass
            etf_idx += 1


        if closes_252.full():
            ups.append(1 if closes_252.main[0] < closes_252.main[-1] else 0)


    ivvcounts = len(beativv)
    ivvb = round(sum(beativv) / ivvcounts,3)
    if debug:
        print("beativv: {}".format( beativv))

    count = len(ups)
    return round(sum(ups) / count, 3), ivvb

def procs():
    stocks = [debug.upper()] if debug else z.getp("listofstocks")
    prob_dic = dict()
    for astock in stocks:
        try:
            prob_dic[astock] = proc(astock)
        except:
            pass
    if not debug:
        z.setp( prob_dic, "probs")
    else:
        print("prob_dic: {}".format( prob_dic))

if __name__ == '__main__':
    procs()
