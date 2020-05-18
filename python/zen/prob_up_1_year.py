import z
import queue
import buy
import sliding
import statistics

start = 650
istart = -1*start
req = start - 20
dates = z.getp("dates")

sdate = dates[istart]

def getetfChanges():
    changes = list()
    values = sliding.WindowQueue(50)
    for i, row in enumerate(buy.getRows("IVV", sdate)):
        c_close = float(row[z.closekey])
        values.add_tail(c_close)
        if values.full():
            changes.append(round(values.main[-1]/values.main[0], 3))
    return changes

etfchanges = getetfChanges()
#print("etfchanges : {}".format( etfchanges ))

def proc(astock):
    prev_close = None
    closes = sliding.WindowQueue(252)
    mins = list()
    ups = list()
    beativv = list()

    values = sliding.WindowQueue(50)
    c = 0

    for i, row in enumerate(buy.getRows(astock, sdate)):
        c_close = float(row[z.closekey])
        values.add_tail(c_close)
        closes.add_tail(c_close)

        if values.full():
            date = row["Date"]
            chg = round(values.main[-1]/values.main[0],3)
#            print("c : {} d : {} chg : {} close : {}".format( c, date, chg, c_close ))
            try:
                beativv.append(1 if chg >= etfchanges[c] else 0)
                c += 1
            except:
                pass


        if closes.full():
            ups.append(1 if closes.main[0] < closes.main[-1] else 0)


    ivvcounts = len(beativv)
    ivvb = round(sum(beativv) / ivvcounts,3)
#    print("beativv: {}".format( beativv))

    count = len(ups)
    if count < 300:
        return "NA", ivvb

    return round(sum(ups) / count,3), ivvb
#
#    if len(mins) >= req:
#        med_15 = statistics.median(mins)
#        means = statistics.mean(mins)
#        useme = (med_15 + means) /2
#        tgt_15 = round(useme * c_close,2)
#        return useme, tgt_15

def procs():
    stocks = z.getp("listofstocks")
#    stocks = ["BA"]
    prob_dic = dict()
    for astock in stocks:
        try:
            prob_dic[astock] = proc(astock)
        except:
            pass
#    print("prob_dic: {}".format( prob_dic))
    z.setp( prob_dic, "probs")

if __name__ == '__main__':
    procs()
