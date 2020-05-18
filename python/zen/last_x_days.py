import z
import buy
from rows import *

stocks = z.getp("listofstocks")
#stocks = ['BFB', "ZM"]
dates = z.getp("dates")
start = 30
istart = 30 * -1
two_from_start = start - 2
HIGHEST = 10000

for astock in stocks:

    mc = buy.getFrom("latestmc", astock)
    if mc > 688:
        continue

    high = 0
    lowFromHigh = None
    countd = 0

    for i, row in enumerate(getRows(astock, dates[istart])):
        try:
            c_open = float(row['Open'])
            c_close = float(row[z.closekey])
        except:
            print("astock: {}".format( astock))
            break
        date = row['Date']
            
        if c_open > high:
            high = c_open
            lowFromHigh = HIGHEST
#            print("new high date : {} {} ".format( date, high ))

        if c_open < lowFromHigh:
            lowFromHigh = c_open
#            print("new low : {} {}".format( date, lowFromHigh ))

        if c_close > high:
            high = c_close
            lowFromHigh = HIGHEST
#            print("new high date : {} {} ".format( date, high ))

        if c_close < lowFromHigh:
            lowFromHigh = c_close
#            print("new low : {} {}".format( date, lowFromHigh ))
        countd = i

    if countd >= start-1:
#        print("high : {}".format( high ))
#        print("lowFromHigh : {}".format( lowFromHigh ))
        change = round(lowFromHigh/high,3)
        buy.addSorted("recent_change", change, astock, keeping = 60)
#exit()
items = buy.getSorted("recent_change")
buy.init()
one = items[:30]
z.setp(one, "one")
#two = items[-30:]
buy.multiple(one)
#buy.multiple(two)
import table_print
table_print.initiate(allow_clearing=True)
print (one)
#print (two)
print (dates[istart])


