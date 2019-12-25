import z
import zen
import buy
from sortedcontainers import SortedSet

# do the dividend large cap stocks do better than non dividends

yearl = z.getp("yearlydic")
last = z.getp("latestAnnual")

def scoreIt(astock):
    global yearl
    try:
        one, two = yearl[astock]
        three = last[astock]
    except:
        return None
    return round((one + two + three)/3,3)

def scoreThem(stocks):
    avg = list()
    for astock in stocks:
        astock = astock[1]
        ans = scoreIt(astock)
        if ans:
            avg.append(ans)
    return round(sum(avg)/len(avg),3)

def scoreThemLast(stocks):
    avg = list()
    for astock in stocks:
        astock = astock[1]
        try:
            avg.append(last[astock])
        except:
            print ("no data for {}".format(astock))
            pass
    return round(sum(avg)/len(avg),3)


stocks = z.getp("listofs")
#print (len(stocks))
divs = SortedSet()
nons = SortedSet()
for astock in stocks:
    try:
        mc1 = int(buy.getFrom("latestmc", astock))
        if mc1 > 1000 or mc1 == 0:
            continue

        beta, pe, mc, div = zen.getChangeStats(astock)

        if div:
            divs.add((mc1, astock))
        else:
            nons.add((mc1, astock))

    except Exception as e:
        print("astock: {}".format( astock))
        z.breaker(20)
#        z.trace(e)
        continue

z.setp(nons[:30], "stocks_30_no_div")
z.setp(divs[:30], "stocks_30_div")

print ("NONS")
print (nons[:30])
print (len(nons))
print ("\n")
print ("DIVS")
print (divs[:30])
print (len(divs))

print("non: {}".format( nons[:1]))
print("div: {}".format( divs[:1]))

print ("No DIV : {}".format(scoreThem(nons[:30])))
print ("   DIV : {}".format(scoreThem(divs[:30])))

print ("No DIV : {}".format(scoreThemLast(nons[:30])))
print ("   DIV : {}".format(scoreThemLast(divs[:30])))

print ("\n")
print ("NONS")
print (nons[-30:])

print ("DIVS")
print (divs[-30:])

print("non: {}".format( nons[-1:]))
print("div: {}".format( divs[-1:]))

print ("No DIV : {}".format(scoreThem(nons[-30:])))
print ("   DIV : {}".format(scoreThem(divs[-30:])))

print ("No DIV : {}".format(scoreThemLast(nons[-30:])))
print ("   DIV : {}".format(scoreThemLast(divs[-30:])))




