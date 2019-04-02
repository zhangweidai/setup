#import dask.bag as db
#db.read_text('*.json').map(json.loads).pluck('name').frequencies().compute()

import z
import dask.dataframe as dd
import dask
import pandas as pd
import os

dask.config.set(scheduler='threads')

def getName(path):
    return os.path.splitext(os.path.basename(path))[0]

def convertToDask():
    path = z.getPath("historical")
    print ("reading")
    dfd = dd.read_csv('{}/*.csv'.format(path), include_path_column = True)
    dfd = dfd.drop(['Volume', 'Adj Close', 'High','Low'], axis=1)
    dfd['path'] = dfd['path'].map(lambda x: getName(x))

    dfd['Change'] = dfd.Close/dfd.Open
    dfd['Change'] = dfd['Change'].map(lambda x: round(x,4))
    createRollingData(dfd)

def getModes():
    return ['C3', 'C6', 'C12', 'C30', 'S30', 'S12','A4', "Change"]

def createRollingData(dfd):
    print (dfd.npartitions)
    for indx in range(dfd.npartitions):
        print("indx: {}".format( indx))
        computed = dfd.get_partition(indx).compute()

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

        name = computed.path[0]
        path = z.getPath("calculated2/{}.csv".format(name))
        computed.to_csv(path)

if __name__ == '__main__':
    convertToDask()
