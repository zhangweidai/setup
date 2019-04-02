#import dask.bag as db
#db.read_text('*.json').map(json.loads).pluck('name').frequencies().compute()

import z
import dask.dataframe as dd
import pandas as pd
import dask
import pandas as pd
import dask.dataframe as dd
from dask import delayed
import time

import os
def getName(path):
    return os.path.splitext(os.path.basename(path))[0]

dfd = None
datedics = None
foo = None
wow = None

def getDF(astock):
    try:
        idx = getDF.partition_mapping[astock]
    except:
        getDF.partition_mapping = z.getp("partition_mapping")
        idx = getDF.partition_mapping[astock]
    try:
        return convertToDask.dfdsaved.get_partition(idx)
    except:
        convertToDask(save=False)
        return convertToDask.dfdsaved.get_partition(idx)
getDF.partition_mapping = dict()

def convertToDask(save=True):
    path = z.getPath("delme2")
    print ("reading")
    dfd = dd.read_csv('{}/*.csv'.format(path), include_path_column = True)
    dfd = dfd.drop(['Volume', 'Adj Close', 'High','Low'], axis=1)
    dfd['path'] = dfd['path'].map(lambda x: getName(x))
    convertToDask.dfdsaved = dfd

    if save:
        dfd['Change'] = dfd.Close/dfd.Open
        dfd['Change'] = dfd['Change'].map(lambda x: round(x,4))

#        temp = temp.reset_index(level=["path"]).drop(columns=['Change'], level=0)
#        temp = temp.groupby(['Date']).agg(lambda x: \
#            tuple(x)).applymap(list).reset_index().set_index(['Date'])

#        newpath = z.getPath("dump")
#        dfd.to_csv(newpath)
        print ("creating rolling data")
        createRollingData(dfd)
        print ("done rolling data")

convertToDask.dfdsaved = None

def getCsvValue(date, astock, column, days_before = 0, looped = 0):
    global dfd
    if days_before:
        dates = z.getp("dates")
        date =  dates[dates.index(date) - days_before]

    setDFD()

    try:
        
        print ("sdf")
        ret = dfd.loc[('Date' == date) & ('path' == astock)]["Open"].compute().array[0]
#        ret = dfd[(dfd.Date == date) & (dfd.path == astock)][column].compute().array[0]
        print ("sdfA")
#        raise SystemExit
        return ret
    except:
        raise SystemExit
        if looped >= 3:
            return None
        try:
            looped += 1
            days_before = 1
            return getCsvValue(date, astock, column, days_before, looped)
        except Exception as e:
            pass
    return None


def getHighLowStocks(date, count, mode = "Change"):
    if getHighLowStocks.dfd is None:
        path = z.getPath("calcd")
        dfd = dd.read_csv('{}/*.csv'.format(path))
        getHighLowStocks.dfd = dfd
    ret = getHighLowStocks.dfd.get_partition(0)
    ret = ret.loc['Date' == date]['values'].compute()
    ret = eval(ret.values[0])
    return ret[-1*count:], ret[:count]
    

getHighLowStocks.dfd = None
getHighLowStocks.ret = dict()

def createRollingData(dfd):
    for indx in range(dfd.npartitions):
        computed = dfd.get_partition(indx).compute()
        name = computed.path[0]

        computed['C3'] = (computed.Close/computed.Open.shift(3))\
            .map(lambda x: round(x,4))
        computed['C6'] = (computed.Close/computed.Open.shift(6))\
            .map(lambda x: round(x,4))
        computed['C12'] = (computed.Close/computed.Open.shift(12))\
            .map(lambda x: round(x,4))
        computed['C30'] = (computed.Close/computed.Open.shift(30))\
            .map(lambda x: round(x,4))
        computed['S12'] = (computed.C12/computed.C3).map(lambda x: round(x,4))
        computed['S30'] = (computed.C30/computed.C6).map(lambda x: round(x,4))
        computed['A4'] = computed.Change.rolling(4).mean()\
            .map(lambda x: round(x,4))
        path = z.getPath("calculated/{}.csv".format(name))
        computed.to_csv(path)
        getDF.partition_mapping[name] = indx

#    z.setp(getDF.partition_mapping, "partition_mapping")
#    processCalculatedData()

def getModes():
    return ['C3', 'C6', 'C12', 'C30', 'S30', 'S12','A4', "Change"]

def setDFD():
    global dfd
    if dfd is None:
        print ("reading calculated")
        path = z.getPath("historical")
        dfd = dd.read_csv('{}/*.csv'.format(path))
        print ("done reading calculated")

from collections import defaultdict
import numpy as np
from numpy import nan

import dask
dask.config.set(scheduler='threads')
def processCalculatedDataOriginal():
    global dfd
    setDFD()
    types = getModes()
    dfd = dfd.drop(['Unnamed: 0'], axis=1)
#    print("dfd: {}".format( dfd.columns))
    for atype in types:
        print("atype : {}".format( atype ))
        pre = dfd.groupby(['Date']).apply(pd.DataFrame.sort_values, by=atype, meta=dfd._meta)
        print("atype : {}".format( atype ))
        values = pre.compute()[[atype,'path']]
        values = values.reset_index(level=['Date']).set_index(['Date'])
        values['path'] = values.groupby(['Date'])['path'].apply(lambda x: x.tolist())
        values['mode'] = atype
        values = values.drop([atype], axis=1)
        values = values[~values.index.duplicated(keep='first')]
        path = z.getPath("calcd/{}_mode.csv".format(atype))
        values.to_csv(path)

def what(atype , dx):
    bar = dx.sort_values(by=atype)[['path']].values.tolist()
    flat_list = [item for sublist in bar for item in sublist]
    return flat_list

def processCalculatedData():
    global dfd
    setDFD()
    types = getModes()
#    dfd = dfd.drop(['Unnamed: 0'], axis=1)
#    print("dfd: {}".format( dfd.columns))
    for atype in types:
        print("atype : {}".format( atype ))
        bar = dfd.groupby(['Date']).apply(lambda x : what(atype, x), \
                                         meta=(1,'int')).compute()
#        print (dfd.groupby(['Date'])[[atype,'path']].apply(what).compute())
#        print (dir(dfd.groupby(['Date'])))
#        print(pre)
#        print (pre[pre.index.duplicated()])
#        print(pre.values.compute())
#        print(type(pre.values))
#        values['path'] = values.groupby(['Date'])
#        .apply(pd.DataFrame.sort_values, by=atype, meta=dfd._meta)
#        raise SystemExit
#        print("atype : {}".format( atype ))
#        values = pre.compute()[[atype,'path']]
#        values = values.reset_index(level=['Date']).set_index(['Date'])
#        values['path'] = values.groupby(['Date'])['path'].apply(lambda x: x.tolist())
#        values['mode'] = atype
#        values = values.drop([atype], axis=1)
#        values = values[~values.index.duplicated(keep='first')]
        path = z.getPath("calcd/{}_mode.csv".format(atype))
        bar.to_csv(path, header=['values'])

if __name__ == '__main__':
#    start = time.time()
    convertToDask()
#    processCalculatedData()
#    end = time.time()
#    print ("Took %f ms" % ((end - start) * 1000.0))

    bar =  getHighLowStocks("2000-01-18", 2, "C3")
    print("bar : {}".format( bar ))
#    print (getHighLowStocks("2019-01-18", 2))
    print (getCsvValue("2000-01-18", "BA", "Close"))
#    print (getCsvValue("2000-01-18", "BA", "Open", days_before=3))
#    print (getDF("BA").compute())
#print (getCsvValue("2000-01-18", "BA", "Open", days_before=10))
