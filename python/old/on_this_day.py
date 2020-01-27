import z 
import datetime
import collections
tmonth = datetime.date.today().month
tday = datetime.date.today().day
dates = z.getp("dates")
spy = z.getCsv("SPY")
dlist = (spy["Date"].tolist())
avgdict = collections.defaultdict(list)
for ayear in range(2, 18):
    year = "200{}".format(ayear)
    if ayear >= 10:
        year = "20{}".format(ayear)
    date = "{}-0{}-{}".format(year,tmonth, tday) 
#    print("date : {}".format( date ))
    tomorrow = "{}-0{}-{}".format(year,tmonth, tday+1) 
#    print("tomorrow : {}".format( tomorrow ))
    try:
        idx =  dlist.index(date)
    except:
        continue

    opend =  spy.at[idx,"High"]
    close =  spy.at[idx,"Low"]
    avgdict["today"].append(close/opend)

    opend =  spy.at[idx+1,"High"]
    close =  spy.at[idx+1,"Low"]
    avgdict["tomorrow"].append(close/opend)

    opend =  spy.at[idx+2,"High"]
    close =  spy.at[idx+2,"Low"]
    avgdict["nextday"].append(close/opend)

for key,something in avgdict.items():
    maxv = round(max(something),4)
    avg = round(sum(something)/len(something) ,4)

    print("maxv : {}".format( maxv ))
    print("avg : {}".format( avg ))
    print("score : {}".format( round(avg + maxv,4)))





