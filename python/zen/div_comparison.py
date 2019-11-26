import z
import zen
from sortedcontainers import SortedSet

# do the top 30 dividend large cap stocks do better than top 30 large cap non dividends
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
        avg.append(last[astock])
    return round(sum(avg)/len(avg),3)


stocks = z.getStocks("IVV")
print (len(stocks))
divs = SortedSet()
nons = SortedSet()
for astock in stocks:
    try:
        mc1 = int(zen.getMCRank(astock))

        beta, pe, mc, div = zen.getChangeStats(astock)
        if div:
            divs.add((mc1, astock))
        else:
            nons.add((mc1, astock))

    except Exception as e:
        print("astock: {}".format( astock))
#        z.trace(e)
        continue

z.setp(nons[:30], "stocks_30_no_div")
z.setp(divs[:30], "stocks_30_div")

print ("NONS")
print (nons[:30])

print ("DIVS")
print (divs[:30])

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




