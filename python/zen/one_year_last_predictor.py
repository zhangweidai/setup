import z
import buy
from sortedcontainers import SortedSet
wanted = 60
half = 30
def doit():
    stocks = z.getp("listofstocks")
    sset = SortedSet()
    for i, astock in enumerate(stocks):

        rank = buy.getMCRank(astock)
        if rank < 800:
            continue
        y1w2, y1m2, y1l, y1l2 = buy.getYearly2(astock)
        if y1l2 == "NA":
            y1l2 = i
        sset.add((y1l2, astock))
        if len(sset) > wanted:
            sset.remove(sset[half])

    z.setp(sset[-30:], "y1l2_big")
    z.setp(sset[:30], "y1l2_small")
#    z.setp(sset[-30:]
    print("sset: {}".format( sset))

if __name__ == '__main__':
#    doit()
    sset = SortedSet()
    for i in range(30):
        sset.add(i)
        if len(sset) > wanted:
            sset.remove(sset[5])
    print("sset : {}".format(sset[-10:]))
