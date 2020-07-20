# how often does it beat ivv given 50 days? 
# how often is 1 year up?
import z
import queue
import buy
import sliding
import statistics
from sortedcontainers import SortedSet

debug = None
import args

ETF = "IVV"
etf_wc, etf_bc, etf_ly, etf_l2y, etf_avg = 0, 0, 0, 0, 0

start = 650
istart = -1*start
req = start - 20
dates = z.getp("dates")

sdate = dates[istart]

years = -1*252*4
asdate = dates[years]
indexdate_4 = dates.index(asdate)

#years2 = -1*252*2
#sdate2 = dates[years]
#
years8 = -1*252*8
asdate8 = dates[years8]
better_etf = list()

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
last_prices = dict()

def proc(astock):
    global etf_wc, etf_bc, etf_ly, etf_l2y, etf_avg, better_etf, last_prices
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
            myidx = dates.index(row['Date']) 
            index_adjust = myidx - dates.index(sdate)

        c_close = float(row[z.closekey])
        closes_50.add_tail(c_close)
        closes_252.add_tail(c_close)

        # ive got a year worth of closes_252
        if closes_50.full():
            interval_change = round(closes_50.main[-1]/closes_50.main[0],3)
            if debug:
                date = row["Date"]
#                print("etf_idx : {} date : {} interval_change : {} close : {}".format( etf_idx, date, interval_change, c_close ))
            try:
                beativv.append(1 if interval_change >= etfchanges[etf_idx + index_adjust] else 0)
            except:
                pass
            etf_idx += 1

        if closes_252.full():
            ups.append(1 if closes_252.main[0] < closes_252.main[-1] else 0)

    try:
        ivvcounts = len(beativv)
        ivvb = round(sum(beativv) / ivvcounts,3)
        if debug:
            print("beativv: {}".format( beativv))
    except Exception as e:
        ivvb = None
        print("problem astock: {}".format( astock))
#        z.trace(e)
#        exit()

#    if debug:
#        print("debuggin astock: {}".format( astock))
#        print("closes_252: {}".format( closes_252.main))

    consideration = list(closes_252.main)[:240]
    try:
        high = max(consideration)
    except:
        return
    low = min(consideration)
    dfh1y = round(c_close / high,3)
    gfl1y = round(c_close / low,3)

    if debug:
        print("dfh1y : {}".format( dfh1y ))
        print("gfl1y : {}".format( gfl1y ))

    wc, bc, avg, ly, l2y, avg8, newstock = annuals(astock)

    if args.args.bta and not newstock:
        buy.addPDic(astock, "ly", ly)
        buy.addPDic(astock, "l2y", l2y)
        buy.addPDic(astock, "avg", avg)
        buy.addPDic(astock, "wc", wc)

    last_prices[astock] = c_close
    count = len(ups)
    y1u = "NA"
    if count > 30:
        y1u = round(sum(ups) / count, 3)

    if astock == ETF:
        etf_wc, etf_bc, etf_ly, etf_l2y, etf_avg = wc, bc, ly, l2y, avg

    if ly != "NA":

        try:
            if wc > etf_wc and bc > etf_bc and ly > etf_ly and l2y > etf_l2y and avg > etf_avg:
                better_etf.append(astock)
        except:
            pass

        rank = buy.getMCRank(astock)
        if rank < 2600 and c_close > 1:
            buy.addSorted("ly", ly, astock)
            try:
                buy.addSorted("wc", wc, astock)
                buy.addSorted("bc", bc, astock)
                buy.addSorted("avg", avg, astock)
                buy.addSorted("ivvb", ivvb, astock)
                if avg8 != "NA":
                    buy.addSorted("avg8", avg8, astock)
            except:
                pass

    return y1u, ivvb, wc, bc, avg, ly, l2y, avg8, dfh1y, gfl1y

etf_dates = list()
missing_days = list()

def annuals(astock):
    global etf_dates, missing_days
    closes_252 = sliding.WindowQueue(252)
    if debug:
        print("start: {}".format( asdate8))
    annual_list = list()

    started_annuals = False
    annualprices8 = list()

    i_adjust = 0
    newstock = False
    days_missing = 0
    first_date = None
    for i, row in enumerate(buy.getRows(astock, asdate8)):
        c_date = row["Date"]

        if astock == ETF:
            etf_dates.append(c_date)

        if i == 0:
            first_date = c_date

        if i == 0 and asdate8 != c_date:
            myidx = dates.index(c_date)
            index_adjust = myidx - dates.index(sdate)
            if debug:
                print("index_adjust : {}".format( index_adjust ))
                print("myidx : {}".format( myidx ))

            if myidx > indexdate_4:
                newstock = True

            # stock as not available 8 years ago
            i_adjust = dates.index(c_date) - dates.index(asdate8)
            if debug:
                print("i_adjust : {} first date {}".format( i_adjust, c_date ))


        if astock != ETF:
            adjusted = i + i_adjust
#            print("{} i {} {} etf_dates: {}".format( adjusted, i, i_adjust, len(etf_dates)))
#            print("c_date : {}".format( c_date ))
            if etf_dates and not days_missing and etf_dates[adjusted] != c_date:
                days_missing += 1

        c_close = float(row[z.closekey])

        if not (i+i_adjust) % 252:
            annualprices8.append(c_close)

        if c_date == asdate:
            started_annuals = True

        if started_annuals or newstock:
            closes_252.add_tail(c_close)
            if closes_252.full():
                annual_change = round(closes_252.main[-1]/closes_252.main[0],3)

                if annual_change > 3.2:
                    annual_change = 3.2

                annual_list.append(annual_change)
#                if debug:
#                    print("annual_change : {} date {}".format( annual_change, row["Date"] ))

    if days_missing > 20:
        missing_days.append((days_missing, astock))

    annualprices8.append(c_close)
    prevprice = None
    annuals8 = list()
    for price in annualprices8: 
        try:
            chg = round(price / prevprice, 3)
            annuals8.append(chg)
        except:
            pass
        prevprice = price

    if debug:
        print("annuals8: {}".format( annuals8))
    avg8 = round((statistics.mean(annuals8) + statistics.median(annuals8))/2,3) if len(annuals8) > 4 and days_missing < 20 else "NA"

    try:
        ly = annual_list[-1]
    except:
        ly = "NA"
        pass

    try:
        l2y = annual_list[-252]
    except:
        l2y = "NA"

    wc = "NA"
    bc = "NA"
    avg = "NA"
    if annual_list and (started_annuals or newstock):
        wc = min(annual_list)
        bc = max(annual_list)
        median = statistics.median(annual_list)
        mean = statistics.mean(annual_list)
        avg = round((median + median + mean) / 3,3)

    return wc, bc, avg, ly, l2y, avg8, newstock

import sys
def procs(astocks = None):
    global better_etf, missing_days

    if astocks:
        current_module = sys.modules[__name__]
        current_module.stocks = astocks
        
    try:
        stocks.pop(stocks.index(ETF))
    except:
        pass

    stocks.insert(0, ETF) 
    prob_dic = dict()
    for i, astock in enumerate(stocks):

        if not i % 100:
            print(": {}".format( astock))

        try:
            prob_dic[astock] = proc(astock)
        except Exception as e:
            print("problem astock: {}".format( astock))
            z.trace(e)
            pass

    if not debug:
        z.setp( prob_dic, "probs")
        for cat in buy.sortcats:
            buy.saveSorted(cat)
        z.setp(better_etf, "better_etf", True)
        z.setp(last_prices, "last_prices")
    else:
        print("prob_dic: {}".format( prob_dic))
        print("wc, bc, avg, ly, l2y, avg8")

if __name__ == '__main__':

    procs()
    if args.args.bta:
        buy.savePs()
