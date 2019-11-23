import zen
import z
import util
from sortedcontainers import SortedSet
import os

dates = z.getp("dates")
ago = dates[-500]
print("ago : {}".format( ago ))
ago5 = dates[-8]

def dosomething():
    savedSort = SortedSet()
    parentdir = util.getPath("historical")
    listOfFiles = os.listdir(parentdir)
    for idx,entry in enumerate(listOfFiles):
        try:
            astock = os.path.splitext(entry)[0]
            mcrank = zen.getMCRank(astock)
            if int(mcrank) > 700:
                continue
            ago_price = zen.getPrice(astock, ago)
#            print("ago_price : {}".format( ago_price ))
            ago5_price = zen.getPrice(astock, ago5)
#            print("ago5_price : {}".format( ago5_price ))
#            print("ago5_price : {}".format( ago5_price ))
#            print("ago_price : {}".format( ago_price ))
            last = zen.getPrice(astock)
#            print("last : {}".format( last ))
#            print("last : {}".format( last ))
            change1 = round(ago5_price/ago_price,3)
#            print("change1 : {}".format( change1 ))
            if change1 > 4 or change1 < 1:
                continue
#            print("change1 : {}".format( change1 ))
            change2 = round(last/ago5_price,3)
#            print("change2 : {}".format( change2 ))
            if change2 < .825 or change2 > 1:
                continue
#            print("change2 : {}".format( change2 ))
            score = (change1 * 5) + (1-change2) * 8
#            print("score : {}".format( score ))
            savedSort.add((score, astock))
        except:
            pass

    print("savedSort : {}".format( savedSort[-30:] ))
    z.setp(savedSort[-30:], "gained_discount");
#    print("savedSort : {}".format( savedSort[:2] ))
#        z.breaker(5)


if __name__ == '__main__':
    dosomething()
