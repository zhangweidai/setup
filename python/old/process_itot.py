import csv
import util
import z

path = util.getPath("holdings/ITOT_holdings2.csv")
print("path : {}".format( path ))
tickers = set()
for row in csv.DictReader(open(path, mode='r', encoding='utf-8-sig')):
    tickers.add(row['Ticker'])
print("tickers: {}".format( tickers))

bar = set(z.getp("listofs"))
foo = tickers.difference(bar)
print (len(foo))
print("foo : {}".format( foo ))
print (" ".join(foo))
