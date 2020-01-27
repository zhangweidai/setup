import util
import operator
from collections import defaultdict
util.getCsv.csvdir = "historical"
spdf = util.getCsv("SPY")
#stocks = util.getStocks(ivv=True)
stocks = util.getStocks()
every = 5
bought_low = defaultdict(int)
bought_high = defaultdict(int)
lowpaid = 0
highpaid = 0

offsets = defaultdict(lambda:None)
avgchangel = list()
avgchangeh = list()
avgchangels = list()
avgchangehs = list()
lastcount = len(spdf)-1
for idx in spdf.index:
    if idx % 5:
        continue
    cdate = spdf.at[idx, "Date"]
    theday = dict()
    maxv = 0
    minv = 10
    highstock = None
    lowstock = None
    for astock in stocks:
        df = util.getCsv(astock)
        if df is None:
            print("astock: {}".format( astock))
            continue

        if offsets.get(astock) == None:
            dates = list(df["Date"])
            try:
                starti = dates.index(cdate)
                offsets[astock] = idx-starti
            except:
                continue

        off = offsets[astock]
        if off == None:
            continue

        myidx = idx - off
        try:
            change = round(df.at[myidx,"Close"]/df.at[myidx,"Open"],3)
        except:
            continue

        if change > maxv:
            highstock = astock
            maxv = change
        if change < minv:
            lowstock = astock
            minv = change

#        theday[astock] = change
#    sorted_x = sorted(theday.items(), key=operator.itemgetter(1))
#    print("highstock : {}".format( highstock ))
#    print("lowstock : {}".format( lowstock ))

#    lowstock = sorted_x[0][0]
    df = util.getCsv(lowstock)

    myidx = idx - offsets[lowstock]
    bought = round(df.at[myidx + 1,"Open"])
    bought_low[lowstock] += 1
#    print("bought_low: {}".format( bought_low))
    lowpaid += bought

#    highstock = sorted_x[-1][0]
    df = util.getCsv(highstock)
    myidx = idx - offsets[highstock]
    bought = round(df.at[myidx + 1,"Open"])
    bought_high[highstock] += 1
#    print("bought_high: {}".format( bought_high))
    highpaid += bought

    if not idx % 160 and idx > 0 or idx == lastcount:
        try:
            lowb = util.calcPortfolio(bought_low, idx=cdate)
            highb = util.calcPortfolio(bought_high, idx=cdate)
        except:
            pass

        lowchange = lowb/lowpaid
        highchange = highb/ highpaid
        avgchangel.append(lowchange)
        avgchangeh.append(highchange)

        avgchangels.append(lowpaid)
        avgchangehs.append(highpaid)

        bought_low = defaultdict(int)
        bought_high = defaultdict(int)
        lowpaid = 0
        highpaid = 0

try:
    print("avgchangel: {}".format(util.formatDecimal(sum(avgchangel)/len(avgchangel))))
    print("avgchangeh: {}".format(util.formatDecimal(sum(avgchangeh)/len(avgchangeh))))
    
    print("avgchangels: {}".format(round(sum(avgchangels)/len(avgchangels))))
    print("avgchangehs: {}".format(round(sum(avgchangehs)/len(avgchangehs))))
except:
    pass

#print("bought_high: {}".format( bought_high))
#print("bought_low: {}".format( bought_low))
#print("lowpaid : {}".format( lowpaid ))
#print("highpaid : {}".format( highpaid ))
#    drop = row["Close"] / row["Open"]
