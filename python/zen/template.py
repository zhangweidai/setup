#full = True
import args
import os
import regen_stock
from sortedcontainers import SortedSet
year = "2020"
import z
import download_batch
import buy
from collections import defaultdict
if __name__ == '__main__':

#    stocks = z.getp("listofstocks")

    sdate = dates[-203]
    numbers = defaultdict(int)
    total = 0
    for astock in stocks:
        for i, row in enumerate(buy.getRows(astock, sdate)):
            numbers[row["Volume"][0]] += 1
            total += 1
    bar = SortedSet()
    print("numbers: {}".format( numbers))
    print("total : {}".format( total ))

    for eachnumber, value in numbers.items():
        bar.add( (round(value/total,3), eachnumber) )
#        print("eachnumber: {} {} ".format( eachnumber, 
    print("bar : {}".format( bar ))


#    stocks.remove("CELG")
#    z.setp(stocks, "listofstocks")
