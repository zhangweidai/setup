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
#    if z.getStocks.devoverride:
#        directory = "delme"

    path = z.getPath(convertToDask.directory)
    print ("reading")
    dfd = dd.read_csv('{}/*.csv'.format(path), include_path_column = True)
    dfd = dfd.drop(['Adj Close', 'High', 'Low'], axis=1)
    dfd['path'] = dfd['path'].map(lambda x: getName(x))

    dfd['Change'] = dfd.Close/dfd.Open
    dfd['Change'] = dfd['Change'].map(lambda x: round(x,4))
    createRollingData(dfd)
convertToDask.directory = "historical"

def getModes():
    if getModes.override:
        return getModes.override
    return ['C3', 'C6', 'C12', 'C30', 'S30', 'S12','A4', "Change", "Volume"]
getModes.override = None

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

        computed['Volume'] = computed.Volume.rolling(5).mean()\
            .map(lambda x: round(x,4))

        name = computed.path[0]
        path = z.getPath("{}/{}.csv".format(createRollingData.dir, name))
        computed.to_csv(path)
createRollingData.dir = "calculated"

#if __name__ == '__main__':
##    z.getStocks.devoverride = True
#    convertToDask.directory = "historical"
#    createRollingData.dir = "historicalCalculated"
#    convertToDask()

if __name__ == '__main__':
    import sys
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "buy":
                convertToDask.directory = "csv"
                createRollingData.dir = "csvCalculated"
                convertToDask()
    except Exception as e:
        print (str(e))
        pass

