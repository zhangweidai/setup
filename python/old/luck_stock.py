import util 
import matplotlib.pyplot as plt

util.getStocks.totalOverride = "IUSG"
stocks = len(util.getStocks(reset = True , simple = True))
print("stocks : {}".format( stocks ))
raise SystemExit
util.getCsv.savedReads = util.getp("allcsvs")
#util.getStocks.totalOverride=True
#util.getStocks.totalOverride = "IVV"
spdf = util.getCsv("SPY")
stocks = util.getStocks()
num_days = len(spdf)-1

print("stocks : {}".format( len(stocks)))
print("num_days : {}".format( num_days ))

ayear = 252
years = 3
duration = int (years * ayear)

problems = set()
def doit(month):
    global problems
    idx = (month * 22) 
    qdate = spdf.at[idx,"Date"]
    edate = spdf.at[idx + duration,"Date"]
    ups = 0
    totals = 0

    for astock in stocks:
        df = util.getCsv(astock)
        try:
            dates = list(df["Date"])
        except:
            problems.add(astock)
            continue

        try:
            starti = dates.index(qdate)
            endi = dates.index(edate)
        except:
            problems.add(astock)
            continue

        try:
            opened = df.at[starti, "High"]
            closed = df.at[endi, "Low"]
            change = closed / opened
#            if change < 1:
            ups += change
            totals += 1
        except:
            print("astock : {}".format( astock ))
            continue
    return round(ups/totals,3)

#print (doit(1))
#raise SystemExit

def doits(avg = None , end  = None):
    lastmonth = int(((duration)/ayear)*12)
    montht = int((num_days/ayear)*12)-lastmonth-9
    ylist = range(1, montht)

    if type(avg) is not bool:
        if avg and end:
            ylist = ylist[avg: end]
        elif avg:
            ylist = ylist[-1*avg:]

    xlist = list()
    for month in ylist:
        xlist.append(doit(month))

    if avg:
        return round(sum(xlist)/len(xlist),3)

    plt.scatter(ylist, xlist, color="red")
    plt.show()

def more_doits():
    global stocks
    global problems
    x = list()
    ylist = ["IUSG", "ITOT", "IUSG|ITOT"]
    for etf in ylist:
        print("etf : {}".format( etf ))
        problems = set()
        util.getStocks.totalOverride = etf
        stocks = util.getStocks(reset=True, simple = True)
        print("stocks : {}".format( len(stocks)))
        x.append(doits(avg = True))
    print("x: {}".format( x))
    plt.scatter(ylist, x)
    plt.show()

#more_doits()
