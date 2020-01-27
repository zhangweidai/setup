import z
import buy
from sortedcontainers import SortedSet

wanted = 60
half = 30
dic2 = z.getp("y1wm2");
anns = z.getp("listofstocks")
dic = z.getp("annuals")
print("dic : {}".format( len(dic) ))
def doit():
    stocks = z.getp("listofstocks")
    sset = SortedSet()
    sset2 = SortedSet()
    sset3 = SortedSet()
    for i, astock in enumerate(stocks):

        rank = buy.getMCRank(astock)
        if rank < 500 or rank > 2300:
            continue
        if buy.getPrice(astock) < 8:
            continue

        try:
            y1w2, y1m2, y1l, y1l2 = dic[astock]
        except:
            pass

        try:
            sset3.add((round(y1w2 + y1m2,4),astock))
        except:
            pass

        if len(sset3) > wanted :
            sset3.remove(sset3[half])

        try:
            y1wm2 = dic2[astock]
            sset2.add((y1wm2, astock))
            if len(sset2) > wanted:
                sset2.remove(sset2[half])
        except Exception as e:
            pass
#        if y1l2 == "NA":
#            y1l2 = i
        if type(y1l2) != float:
            continue
        sset.add((y1l2, astock))
        if len(sset) > wanted:
            sset.remove(sset[half])

    z.setp(sset[-30:], "y1l2_big")
    z.setp(sset[:30], "y1l2_small")

    z.setp(sset2[-30:], "y1wm2_big")
    z.setp(sset2[:30], "y1wm2_small")

    z.setp(sset3[:30], "worst_smallcalp", True)
    z.setp(sset3[-30:], "best_smallcalp", True)
#    z.setp(sset[-30:]

if __name__ == '__main__':
    doit()

