import util
import operator

util.getCsv.csvdir = "historical"
def getDroppers():
    stocks = util.getStocks()
    print("stocks : {}".format( len(stocks)))
    st = dict()
    for astock in stocks:
        df = util.getCsv(astock)
        change = df["Close"].iloc[-1] / df["Close"].iloc[-2] 
        st[astock] = round(change,3)
    sorted_x = sorted(st.items(), key=operator.itemgetter(1))
    for change in sorted_x[:10]:
        print("change {} : {}".format( change[0], 
                    util.formatDecimal(change[1])))
getDroppers()

raise SystemExit

df = util.getCsv("W")

total = 0
consecdrop = 0
dropped = False
dropstreak = 0
maxdrop = 0
streaks = []
percentdown = 0.065
compar = 1-percentdown
for idx,row in df.iterrows():
    drop = row["Close"] / row["Open"]
    if dropped:
        if drop < 1:
            consecdrop += 1
            dropstreak += 1
        else:
            dropped = False
            if dropstreak > maxdrop:
                maxdrop = dropstreak
            streaks.append(dropstreak)
            dropstreak = 0

        total+=1
    if drop < compar:
        dropstreak += 1
        dropped = True
print("consecdrop: {}".format(consecdrop))
print("total: {}".format(total))
print("perc: {}".format(consecdrop/total))
print("maxdrop : {}".format( maxdrop ))
print("average : {}".format( sum(streaks)/len(streaks) ))
