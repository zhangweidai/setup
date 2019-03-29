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

def doit(astock):
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
    
        if monthd == 0:
            monthd = month
            monthlist = list()
        elif monthd != month:
            leng = int(len(monthlist)/2)
            if leng > 6:
                first = z.avg(monthlist[0:leng])
                second = z.avg(monthlist[leng:])
                tally[(first>second) ] += 1
            monthlist = list()
            monthd = month
        else:
            close = df.at[i,"Close"]
            monthlist.append(close) 

for etf in z.getEtfList():
    doit(etf)
print("tally: {}".format( tally))
