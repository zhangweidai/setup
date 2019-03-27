import z 
import matplotlib.pyplot as plt

days = z.getp("dates")
num_days = len(days)
print("num_days : {}".format( num_days ))

spdf = z.getCsv("SPY")
stocks = z.getStocks()

ayear = 252
years = 6
duration = int (years * ayear)
#problems = set()

def doit(month, day):
#    global problems
    idx = (month * 22)  + day

    qdate = days[idx]
    edate = days[idx + duration]

    up, ups, down, downs, total, totals = 0,0,0,0,0,0

    for astock in stocks:
        df = z.getCsv(astock)
        try:
            dates = list(df["Date"])
        except:
#            problems.add(astock)
            continue

        try:
            starti = dates.index(qdate)
            endi = dates.index(edate)
        except:
#            problems.add(astock)
            continue

        try:
            opened = df.at[starti, "High"]
            closed = df.at[endi, "Low"]
            change = closed / opened
            if change < 1:
                down += change
                downs += 1

            if change > 1:
                up += change
                ups += 1

            total += change
            totals += 1
        except:
            print("astock : {}".format( astock ))
            continue

    return round(total/totals,3), round(up/ups,3), round(down/downs,3)

def doits(tlist, ulist, dlist, avg = None , end  = None):
    lastmonth = int(((duration)/ayear)*12)
    montht = int((num_days/ayear)*12)-lastmonth-9
    ylist = range(1, montht)

    if type(avg) is not bool:
        if avg and end:
            ylist = ylist[avg: end]
        elif avg:
            ylist = ylist[-1*avg:]

    xlist = list()
    ts = list()
    ds = list()
    us = list()
    for month in ylist:
        for i in range(1,10,2):
            t,u,d = doit(month,i)
            ts.append(t)
            us.append(u)
            ds.append(d)

    if avg:
        tlist.append(round(sum(ts)/len(ts),3))
        ulist.append(round(sum(us)/len(us),3))
        dlist.append(round(sum(ds)/len(ds),3))

    plt.show()

def more_doits():
    global stocks
#    global problems
    ylist = ["USMV", "IVV", "IUSG", "ITOT", "IUSG-IVV", "USMV/IUSG", "IUSG|USMV"]
    tlist = list()
    ulist = list()
    dlist = list()
    for etf in ylist:
        print("etf : {}".format( etf ))
#        problems = set()
        stocks = z.getStocks(etf, reset=True, simple = True, preload=True)
        doits(tlist, ulist, dlist, avg = 4)

    plt.scatter(ylist, tlist, color="blue")
    plt.scatter(ylist, ulist, color="green")
    plt.scatter(ylist, dlist, color="red")
    plt.show()

more_doits()
