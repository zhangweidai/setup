import z
import csv
import dask
import pandas as pd
import dask.dataframe as dd
from dask import delayed
#dates.setdefault(SortedSet)
#bar = SortedSet([(13, "C")])
#bar.add((23,"BA"))
#bar.add((24,"BA"))
#bar.add((14,"SPY"))
##bar.add((13,"C"))
#bar.add((44,"SPY"))
#bar.discard(bar[3])
#print(bar)

from collections import OrderedDict
from sortedcontainers import SortedSet
keeping = 10
discardlocation = int(keeping/2)
inputf_dict = dict()
def process(astock, col, dates):
    path = z.getPath("historical/{}.csv".format(astock))
    inputf_dict[astock] = csv.DictReader(open(path))

    inputf = inputf_dict[astock]
    for row in inputf:
        val = float(row[col])
        try:
            dates[row['Date']].add((val, astock))
        except:
            dates[row['Date']] = SortedSet([(val, astock)])

        if len(dates[row['Date']]) > keeping:
            dates[row['Date']].discard(dates[row['Date']][discardlocation])

dates = OrderedDict()
stocks = z.getStocks("IVV", reset=True)
for astock in stocks:
#    print("astock : {}".format( astock ))
#    if astock not in inputf_dict:
#    path = z.getPath("historical/{}.csv".format(astock))
#    inputf_dict[astock ] = csv.DictReader(open(path))
    process(astock, "Open", dates)
#z.setp(dates, "dates_open")
#print(dates)
#print(dates)

#raise SystemExit
#import dask.dataframe as dd
#df = pd.DataFrame({'x': [1, 2, 3, 4, 5],'y': [1., 2., 3., 4., 5.]})
#ddf = dd.from_pandas(df, npartitions=2)
#
#def myadd(df, a, b=1):
#    return df.x + df.y + a + b
#res = ddf.head(npartitions=2, compute=True)
#print("res : {}".format( res ))
#raise SystemExit
#import os
#def getName(path):
#    return os.path.splitext(os.path.basename(path))[0]

#path = z.getPath("delme")
#dfd = dd.read_csv('{}/*.csv'.format(path), include_path_column = True)
#dfd['path'] = dfd['path'].map(lambda x: getName(x))
##dfd = dd.read_csv('{}/{}*.csv'.format(path, 'strategy_report'), include_path_column = True)
#bag = dfd.get_partition(0).to_bag()
#for what in bag:
#    print("what : {}".format( what[0] ))
#raise SystemExit
#mapping = dict()
#for indx in range(dfd.npartitions):
##    mapping[indx] = dfd.get_partition(indx)['path'].compute()[0]
#    path = dfd.get_partition(indx)['path'].compute()[0]
#    name = os.path.splitext(os.path.basename(path))[0]
#    mapping[name] = indx
#
#print(mapping)
#def dfdGetter(date, column, astock):
#    idx = mapping[astock]
#    bar = dfd.partitions[idx]['Date'].compute()
#    baridx = bar[bar == date].index[0]
#    bar = dfd.partitions[idx][column].compute()
#    return bar[baridx]
#
#print (dfdGetter("2019-03-20", "Open", "BA"))
#raise SystemExit
#
#bar = dfd.partitions[0].compute().head()
#print("bar : {}".format( bar.columns ))
#
#raise SystemExit
#print(bar.compute()["Close"][0])
##print(bar.compute())
#bar = dfd.get_partition(0)
#print(bar.compute()["Close"][0])
##print (dfd.info())
##df2 = dfd.compute(scheduler='threads')
##print (df2.info())
##print (dfd.known_divisions)
##print("df : {}".format( dfd.divisions ))
##print("df : {}".format( df ))
#
#
#
##path = z.getCsv("IJH", asPath=True)
##df = dd.read_csv(path)
##df2 = df[df.Date == '2019-03-29'].Close
##df_dates = df.Date.values
##print("df_dates : {}".format( df_dates ))
##print (df2.compute())
##raise SystemExit
##
##import random
##def function(data):
##    x = random.randrange(0,5)
##    return data[1]*x
##
##df['Multiple'] = list(map(function, enumerate(df['Close'])))
##print(df.tail())
##print (z.getStocks.etfs.keys())
##print(len(stocks))
#
##stocks = z.getStocks("ITOT")
##print(len(stocks))
