import math
import zen
import z
import util
from sortedcontainers import SortedSet
import os

dates = z.getp("dates")
ago500 = dates[-500]
ago200 = dates[-200]
ago190 = dates[-190]
ago100 = dates[-100]
print("ago190 : {}".format( ago190 ))
print("ago100 : {}".format( ago100 ))
print("ago500 : {}".format( ago500 ))
ago5 = dates[-13]

def dosomething():
    savedSort = SortedSet()
    low_high_sort = SortedSet()
    parentdir = util.getPath("historical")
    listOfFiles = os.listdir(parentdir)
    for idx,entry in enumerate(listOfFiles):

        if not idx % 100:
            print("idx: {}".format( idx))

        try:
            astock = os.path.splitext(entry)[0]
            mcrank = zen.getMCRank(astock)
            if int(mcrank) > 1234:
                continue
            ago500_price = zen.getPrice(astock, ago500)
            ago200_price = zen.getPrice(astock, ago200)
#            print("ago500_price : {}".format( ago500_price ))
            ago5_price = zen.getPrice(astock, ago5)
#            print("ago5_price : {}".format( ago5_price ))
#            print("ago5_price : {}".format( ago5_price ))
#            print("ago500_price : {}".format( ago500_price ))
            last = zen.getPrice(astock)
            change1 = round(ago5_price/ago500_price,3)

            ago190_price = zen.getPrice(astock, ago190)
            changelow = round(ago190_price/ago500_price,3)
            if changelow < 0.80:
                change2 = round(last/ago190_price,3)
                if change2 > 1.1 and change2 < 4:
                    change2  = math.sqrt(change2)
                    score = (changelow * 3) - (change2-1)
                    low_high_sort.add((score, astock))

            if change1 > 4 or change1 < 1:
                continue

            if int(mcrank) > 720:
                continue

            change2 = round(last/ago5_price,3)
            if change2 < .825 or change2 > 1:
                continue
            score = round((change1) + (1-change2) * 1.41,5)
            savedSort.add((score, astock))
        except:
            pass

    print("savedSort : {}".format( savedSort[-30:] ))
    z.setp(savedSort[-30:], "gained_discount");

    print("lowhighSort : {}".format( low_high_sort[:30] ))
    z.setp(low_high_sort[:30], "low_high_sort");
#    print("savedSort : {}".format( savedSort[:2] ))
#        z.breaker(5)


if __name__ == '__main__':
    dosomething()
