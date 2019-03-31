#import dask.bag as db
#db.read_text('*.json').map(json.loads).pluck('name').frequencies().compute()

import z
import dask.dataframe as dd
import pandas as pd
import dask
import pandas as pd
import dask.dataframe as dd
from dask import delayed

import os
def getName(path):
    return os.path.splitext(os.path.basename(path))[0]

dfd = None
values = None
datedics = None
foo = None
wow = None
#def readSaved(read=True):
#    global dfd, values, datedics, foo, wow
#    dfd = dd.read_csv(bagspath)
#    values = dfd.groupby('Date').apply(list, meta = ("Close", "f8"))
#    print(values.compute().tolist())

def getDF(astock):
    try:
        idx = getDF.partition_mapping[astock]
    except:
        getDF.partition_mapping = z.getp("partition_mapping")
        idx = getDF.partition_mapping[astock]
    return dfd.get_partition(idx)
getDF.partition_mapping = dict()

def computeme(grp_obj):
    print("grp_obj: {}".format( grp_obj))
#    gr_size = grp_obj.size()
    return len(grp_obj)

calced=None
def convertToDask(save=False):
    global dfd, values, pre, calced
    path = z.getPath("delme")
    dfd = dd.read_csv('{}/*.csv'.format(path), include_path_column = True)
    dfd = dfd.drop(['Volume', 'Adj Close', 'High','Low'], axis=1)

    dfd['path'] = dfd['path'].map(lambda x: getName(x))
    dfd['Change'] = dfd.Close/dfd.Open
    dfd['Change'] = dfd['Change'].map(lambda x: round(x,4))


#    calced = dfd.groupby('path').apply(computeme)
#    print(calced )

    pre = dfd.groupby(['Date','path']).agg({'Change':['min']})
    values = pre.compute()

    foo = values.reset_index(level=["path"]).drop(columns=['Change'], level=0)
    getHighLowStocks.ret = foo.groupby(['Date']).agg(lambda x: \
            tuple(x)).applymap(list).reset_index().set_index(['Date'])

    newpath = z.getPath("data/end.csv")
    getHighLowStocks.ret.to_csv(newpath)


dates = z.getp("dates")
def getCsvValue(date, astock, column, days_before = 0, looped = 0):
    if days_before:
        date =  dates[dates.index(date) - days_before]
        
    try:
        return dfd[(dfd.Date == date) & (dfd.path == \
            astock)][column].compute().array[0]
    except:
        if looped >= 3:
            return None
        try:
            looped += 1
            days_before = 1
            return getCsvValue(date, astock, column, days_before, looped)
        except Exception as e:
            pass
    return None
    
#    return bar[(bar.Date == date) & (bar.path == astock)][column].compute().array[0]

temp = None
def getHighLowStocks(date, count):
    global temp
    if getHighLowStocks.ret is None:
        newpath = z.getPath("data/end.csv")
        getHighLowStocks.ret = pd.read_csv(newpath)
        getHighLowStocks.ret = getHighLowStocks.ret.reset_index().set_index(\
                               ['Date']).drop(columns=['index'])
        temp = eval(getHighLowStocks.ret.loc[date].values[0])
        return temp[-1*count:], temp[:count]
    temp = getHighLowStocks.ret.loc[date]
    temp = (temp.tolist()[0])
    return temp[-1*count:], temp[:count]
getHighLowStocks.ret = None

def createRollingData():
    for indx in range(dfd.npartitions):
        computed = dfd['path'].get_partition(indx).compute()
        name = computed[0]
        computed = dfd.get_partition(indx).compute()
        computed['3D'] = (computed.Close/computed.Open.shift(3))\
            .map(lambda x: round(x,4))
        computed['6D'] = (computed.Close/computed.Open.shift(6))\
            .map(lambda x: round(x,4))
        computed['12D'] = (computed.Close/computed.Open.shift(12))\
            .map(lambda x: round(x,4))
#        dfdk['3D'] = dfd['path'].map
#        (lambda x: round(x,3))
#        print("name : {}".format( name ))
#        part = dfd.get_partition(indx)
#        name = str(part['path'].compute()[0])

#        print(part.columns)
        computed['4DA'] = computed.Change.rolling(4).mean()\
            .map(lambda x: round(x,4))
        print(computed)
        path = z.getPath("calculated/{}.csv".format(name))
        computed.to_csv(path)
#        getDF.partition_mapping[name] = indx
#    z.setp(getDF.partition_mapping, "partition_mapping")

convertToDask()
createRollingData()
def getHighLowStocksSpecial(date, mode, count):

print (getHighLowStocksSpecial("2000-01-18", 1))
#print(getDF("BA").compute())
#print (getHighLowStocks("2000-01-18", 1))
#print (getHighLowStocks(
#print (getCsvValue("2000-01-18", "BA", "Open"))
#print (getCsvValue("2000-01-18", "BA", "Open", days_before=3))
#print (getCsvValue("2000-01-18", "BA", "Open", days_before=10))
#readSaved()

raise SystemExit

print(mapping)
def dfdGetter(date, column, astock):
    idx = mapping[astock]
    bar = dfd.partitions[idx]['Date'].compute()
    baridx = bar[bar == date].index[0]
    bar = dfd.partitions[idx][column].compute()
    return bar[baridx]

print (dfdGetter("2019-03-20", "Open", "BA"))
raise SystemExit

bar = dfd.partitions[0].compute().head()
print("bar : {}".format( bar.columns ))

raise SystemExit
print(bar.compute()["Close"][0])
#print(bar.compute())
bar = dfd.get_partition(0)
print(bar.compute()["Close"][0])
#print (dfd.info())
#df2 = dfd.compute(scheduler='threads')
#print (df2.info())
#print (dfd.known_divisions)
#print("df : {}".format( dfd.divisions ))
#print("df : {}".format( df ))



#path = z.getCsv("IJH", asPath=True)
#df = dd.read_csv(path)
#df2 = df[df.Date == '2019-03-29'].Close
#df_dates = df.Date.values
#print("df_dates : {}".format( df_dates ))
#print (df2.compute())
#raise SystemExit
#
#import random
#def function(data):
#    x = random.randrange(0,5)
#    return data[1]*x
#
#df['Multiple'] = list(map(function, enumerate(df['Close'])))
#print(df.tail())
#print (z.getStocks.etfs.keys())
#print(len(stocks))

#stocks = z.getStocks("ITOT")
#print(len(stocks))
