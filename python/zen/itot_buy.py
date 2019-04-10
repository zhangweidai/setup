import z
import zen
import dask_help
import csv
import util

def lowSale():
    z.getStocks.devoverride = "ITOT"
    dask_help.convertToDask.directory = "history"
    dask_help.createRollingData.dir = "historyCalculated"
    
    savedlow = dict()
    for astock in z.getStocks():
        path = z.getPath("{}/{}.csv".format("historical", astock))
        for row in csv.DictReader(open(path)):
            closep = float(row['Close'])
        if closep < 10:
            savedlow[astock] = util.getLiveData(astock, andkey='sharesOutstanding')
    print("savedlow: {}".format( len(savedlow)))
    z.setp(savedlow,"savedlow")

from sortedcontainers import SortedSet
def sortedEtfPrice():
    z.online.online = False
    stocks = z.getStocks("IVV|IUSG")
    z.getStocks.devoverride = "ITOT"

    sorts = SortedSet()
    for astock in stocks:
        price = zen.getPrice(astock)
        if price:
            sorts.add((price, astock))

    zen.whatAboutThese(sorts[-16:])
    zen.whatAboutThese(sorts[:16])

def sortedDropPrice():
    z.getStocks.devoverride = "ITOT"
    dask_help.convertToDask.directory = "history"
    dask_help.createRollingData.dir = "historyCalculated"

    zen.setDropRanking()
    latestdrop = z.getp("{}latestdrop".format(z.getStocks.devoverride))
    zen.whatAboutThese(latestdrop[-15:])
#sortedDropPrice()
#sortedEtfPrice()
