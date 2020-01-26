import z
import operator

def getDroppers():
    stocks = z.getStocks()
    print("stocks : {}".format( len(stocks)))
    st = dict()
    for astock in stocks:
        df = z.getCsv(astock)
        leng = len(df)-1
        change = df.at[leng,"Close"] / df.at[leng-1,"Close"]
        st[astock] = round(change,3)
    sorted_x = sorted(st.items(), key=operator.itemgetter(1))
    for change in sorted_x[:10]:
        print("change {} : {}".format( change[0], 
                    z.formatDecimal(change[1])))
#getDroppers()
#raise SystemExit

df = z.getCsv("SPY")

total = 0
consecdrop = 0
dropped = False
dropstreak = 0
maxdrop = 0
streaks = []
percentdown = 0.065
compar = 1-percentdown
ups = []
from collections import defaultdict
datesdict = defaultdict()
for idx in df.index:
    date = df.at[idx,"Date"] 
    change = df.at[idx,"Close"] / df.at[idx, "Open"]

    if change < 1:
        ups.append((date, change))

    if dropped:
        if change < 1:
            consecdrop += 1
            dropstreak += 1
        else:
            dropped = False
            if dropstreak > maxdrop:
                maxdrop = dropstreak
            streaks.append(dropstreak)
            dropstreak = 0

        total+=1
    if change < compar:
        dropstreak += 1
        dropped = True

#sorteddates = sorted(ups, key=operator.itemgetter(1), reverse=True)
#for date in sorteddates:
#    if "2019" in date[0]:
#        print("date :{} {}".format(date[0],  z.percentage(date[1]) ))
#        z.breaker(5)
#    if "2018" in date[0]:
#        print("date :{} {}".format(date[0],  z.percentage(date[1]) ))

sorteddates = sorted(ups, key=operator.itemgetter(1), reverse=False)
for date in sorteddates:
    if "2019" in date[0]:
        print("date :{} {}".format(date[0],  z.percentage(date[1]) ))
        z.breaker(5)
    if "2018" in date[0]:
        print("date :{} {}".format(date[0],  z.percentage(date[1]) ))

#print(upsorted[-10:])
print("consecdrop: {}".format(consecdrop))
print("total: {}".format(total))
print("perc: {}".format(consecdrop/total))
print("maxdrop : {}".format( maxdrop ))
print("average : {}".format( sum(streaks)/len(streaks) ))
