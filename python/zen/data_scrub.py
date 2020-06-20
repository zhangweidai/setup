# how often does it beat ivv given 50 days? 
# how often is 1 year up?
import z
import buy
import regen_stock
import gained_discount

debug = None
debug = "LLY"

dates = z.getp("dates")
years8 = -1*252*8
asdate8 = dates[years8]
index8 = dates.index(asdate8)
cdates = dates[index8:]
cdates.reverse()

def proc(astock):
    mdates = list()
    prev = None
    for i, row in enumerate(buy.getRows(astock, asdate8)):
        c_date = row['Date']
        buy.addSortedHigh("a", float(row['Chg']), c_date, 5)
        mdates.append(c_date)
    print (buy.getSorted("a"))
    mdates.reverse()
    prevdate = None
    for i,date in enumerate(mdates):
        if date != cdates[i]:
            return prevdate
        prevdate = date

def procs( cleanup = True):
    stocks = [debug.upper()] if debug else z.getp("listofstocks")

    prob_dic = dict()
    missmatch = dict()
    for i, astock in enumerate(stocks):

        if not i % 100:
            print("astock: {}".format( astock))

        try:
            miss = proc(astock)
            if miss:
                missmatch[astock] = miss
        except Exception as e:
            print("astock: {}".format( astock))
            z.trace(e)
            pass

    if not cleanup:
        return

    delets = list()
    cleanups = dict()
    for astock, date in missmatch.items():
        idx = cdates.index(date)
        if idx < 120:
            delets.append(astock)
        else:
            cleanups[astock] = date
    gained_discount.batchdelete(delets)
    for astock, date in cleanups.items():
        gained_discount.cleanup(astock, date)



if __name__ == '__main__':
    procs(False)
