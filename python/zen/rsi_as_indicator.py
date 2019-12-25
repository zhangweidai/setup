import z
import zen
import buy
from sortedcontainers import SortedSet

def getRsi(seen):
    ups = list()
    downs = list()
    for val in seen:
        if val > 1.0:
            ups.append(val)
        elif val < 1.0:
            downs.append(val)

    if len(downs) == 0:
        return 100

    total = len(seen) + 1
    m1 = sum(ups)/total
    m2 = sum(downs)/total
    return round(100-(100/(1+ (m1/m2))),1)

# do the dividend large cap stocks do better than non dividends

stocks = z.getp("listofstocks")
print("stocks : {}".format( len(stocks)))
#stocks = ["AGM", "AGS"]
#print (len(stocks))
divs = SortedSet()
nons = SortedSet()
dates = z.getp("dates")
count = 13
preday = 5
rsi_indicator_dic = dict()
rsi_high = SortedSet()
for j, astock in enumerate(stocks):
    seen = list()
    rsid = dict()
    rseen = list()

    if not j % 100:
        print("count: {}".format( j))

    try:
        prev = None
        for i, row in enumerate(buy.getRows(astock, dates[0])):
            c_close = round(float(row[z.closekey]),2)
            try:
                change = round(c_close/prev,4)
            except:
                prev = c_close
                continue
            seen.append(change)
            if len(seen) > count:
                seen.pop(0)
                try:
                    rsi = getRsi(seen)
                except:
                    print("{} problems: {}".format(astock, seen))
                    continue
                rseen.append((rsi, c_close))
#                rsid[row['Date']] = round(rsi,1)
            prev = c_close
    except Exception as e:
        z.trace(e) 
        pass

    tally = list()

    for i, pair in enumerate(rseen):
        rsi = pair[0]
        try:
            if rsi <= 20:
                if pair[1] < rseen[i+preday][1]:
                    tally.append(1)
                else:
                    tally.append(-1)
            elif rsi >= 80:
                if pair[1] > rseen[i+preday][1]:
                    tally.append(1)
                else:
                    tally.append(-1)
        except:
            pass
    try:
        lental = len(tally)
        if lental < 50:
            continue
        valid = abs(round(sum(tally)/lental,3))
    except:
        continue
    rsi_indicator_dic[astock] = valid
    rsi_high.add((valid, astock))
    if len(rsi_high) > 30:
        rsi_high.remove(rsi_high[0])
z.setp(rsi_indicator_dic, "rsi_indicator_dic")
z.setp(rsi_high, "rsi_high", True)

