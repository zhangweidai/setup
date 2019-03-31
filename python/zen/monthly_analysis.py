import z
#dates = z.getp("dates")

#for year in range(2015, 2020):
#    for month in range(1,13):
#        day = 1
#        while ( "{}-0{}-0{}".format(year,month,day) not in dates):
#            day += 1
#        date = "{}-{}-{}".format(year,month,day)
#        idx = dates.index(date)
#        print(df[idx:idx +5])
#        raise SystemExit

        
monthlist = list()
from collections import defaultdict
tally = defaultdict(int)
monthtally = defaultdict(list)
daytally = defaultdict(list)

annualtally = defaultdict(int)
annualcounted = defaultdict(int)
cyear = 0
cyearidx = 0
def doit(astock):
    global cyear, cyearidx
    monthd = 0
    df = z.getCsv(astock)
    if df is None:
        print("astock: {}".format( astock))
        return

    dates = df["Date"].tolist()
    for i,date in enumerate(dates):
        tokens = date.split("-")
        month = tokens[1]
        day = tokens[2]
        year = tokens[0]
#        if int(year) <= 2015:
#            continue
        if cyear != year:
            print("cyearidx : {}".format( cyearidx ))
            cyearidx = 0
            cyear = year
            z.breaker(2)
        else:
            cyearidx += 1

    
        if monthd == 0:
            monthd = month
            monthlist = list()

        close = df.at[i,"Close"]
        opend = df.at[i,"Open"]
        if opend < close:
            annualtally[year]+=1
        annualcounted[year]+=1

        daytally[day].append(close)
        monthlist.append(close) 
        if monthd != month:

            leng = int(len(monthlist)/2)
            if leng > 6:
                monthtally[monthd].append(z.avg(monthlist))
                first = z.avg(monthlist[0:leng])
                second = z.avg(monthlist[leng:])
                tally[(first>second) ] += 1
            monthlist = list()
            monthd = month

for etf in z.getEtfList():
    doit(etf)

#for etf in z.getStocks("IVV"):
#    doit(etf)


print("tally: {}".format( tally))

import matplotlib.pyplot as plt
for month,values in monthtally.items():
    avg = z.avg(values)
    print("month: {} {}".format( month,avg))
    plt.scatter(month,avg , color="blue")
#plt.show()
sortme = list()
for month,values in daytally.items():
    avg = z.avg(values)
    print("day: {} {}".format( month, avg))
    sortme.append([month, avg])

import operator
sorted_xs2 = sorted(sortme, key=operator.itemgetter(1))
print("sorted_xs2 : {}".format( sorted_xs2 ))

totally = defaultdict(list)
print("annualcounted: {}".format( annualcounted))
for i,counted in enumerate(annualcounted):
    print("counted : {} {}".format( counted, round(annualtally[counted]/annualcounted[counted],2 )))
