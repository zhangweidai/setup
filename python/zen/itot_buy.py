import z
import zen
import dask_help
import csv
import util

from sortedcontainers import SortedSet
def lowSale():
    z.getStocks.devoverride = "ITOT"
    dask_help.convertToDask.directory = "history"
    dask_help.createRollingData.dir = "historyCalculated"
    
    savedlow = dict()
    sorts = SortedSet()
    for astock in z.getStocks():
        path = z.getPath("{}/{}.csv".format("historical", astock))
        for row in csv.DictReader(open(path)):
            closep = float(row['Close'])
        if closep < 10.0:
            data = util.getLiveData(astock, andkey='sharesOutstanding')
            savedlow[astock] = data
            if float(data[0]) > 0.0:
                sorts.add((data[0]*data[1], astock))

    count = int(len(sorts)/12)
    print("count : {}".format( count ))

    z.setp(savedlow,"savedlow")
    z.setp(sorts,"savedlowsorts")
    print("sorts: {}".format( sorts))

    zen.whatAboutThese(sorts[:count])
    zen.whatAboutThese(sorts[-1*count:])
lowSale()
raise SystemExit
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
