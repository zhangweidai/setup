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

dfd = None
def convertToDask(simple = False, missingonly = False):
    global dfd
    path = z.getPath(convertToDask.directory)
    print ("reading")
    dfd = dd.read_csv('{}/*.csv'.format(path), include_path_column = (not simple))

    if not simple:
        dfd = dfd.drop(['Adj Close', 'High', 'Low'], axis=1)
        dfd['path'] = dfd['path'].map(lambda x: getName(x))

    dfd['Change'] = dfd.Close/dfd.Open
    dfd['Change'] = dfd['Change'].map(lambda x: round(x,4))

    print ("begin rolling")
    createRollingData(missingonly)

    import generate_list
    generate_list.regenerateHistorical()
convertToDask.directory = "historical"

def getModes():
    if getModes.override:
        return getModes.override
    return ['C3', 'C6', 'C12', 'C30', 'S30', 'S50', 'S12','A4', "Change", "Volume"]
getModes.override = None

def threader():
    global q
    while True:
        doone(q.get())
        q.task_done()
q = None
def createRollingData(missingonly):
    global dfd, q
    import threading
    from queue import Queue
    q = Queue()
    for x in range(7):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    print (dfd.npartitions)
    for indx in range(dfd.npartitions):
        q.put([indx, missingonly])

    q.join()

def doone(indx):
    global dfd
    indx, missingonly = indx[0], indx[1]
    try:
        computed = dfd.get_partition(indx).compute()
        name = computed.path[0]
        path = z.getPath("{}/{}.csv".format(createRollingData.dir, name))
        if os.path.exists(path):
            return

        computed['C3'] = (computed.Close/computed.Open.shift(3))\
            .map(lambda x: round(x,4))

        computed['C6'] = (computed.Close/computed.Open.shift(6))\
            .map(lambda x: round(x,4))

        computed['C12'] = (computed.Close/computed.Open.shift(12))\
            .map(lambda x: round(x,4))

        computed['C30'] = (computed.Close/computed.Open.shift(30))\
            .map(lambda x: round(x,4))

        computed['S50'] = (computed.Open.shift(50)/computed.C3).map(lambda x: round(x,4))

        computed['S12'] = (computed.C12/computed.C3).map(lambda x: round(x,4))

        computed['S30'] = (computed.C30/computed.C6).map(lambda x: round(x,4))

        computed['A4'] = computed.Change.rolling(4).mean()\
            .map(lambda x: round(x,4))

        computed['Volume'] = computed.Volume.rolling(5).mean()\
            .map(lambda x: round(x,4))

        computed.to_csv(path)
        print("done indx : {}".format( indx ))

    except Exception as e:
        print (str(e))
        pass

createRollingData.dir = "historicalCalculated"

#if __name__ == '__main__':
def historicalToCsv():
    import csv
    z.getStocks.devoverride = "ITOT"
    z.getStocks.extras = True
    stocks = z.getStocks()
    howmany = 52
    dates = z.getp("dates")
    print("latest date : {}".format(dates[-1]))
    starti = dates[-1 * howmany]

    convertToDask.directory = "csv"
    createRollingData.dir = "csvCalculated"

    for astock in stocks:
        path = z.getPath("historical/{}.csv".format(astock))
        tpath = z.getPath("csv/{}.csv".format(astock))
        if os.path.exists(tpath):
            continue

        with open(tpath, "w") as f:
            f.write("Date,Open,Close,Volume,path\n")
            starting = False
            for row in csv.DictReader(open(path)):
                cdate = row['Date']
                if cdate == starti:
                    starting = True
    
                if starting:
                    f.write("{},{},{},{},{}\n".format(\
                        cdate,row['Open'],row['Close'],row['Volume'],astock))
    convertToDask(simple=True, missingonly=True)

if __name__ == '__main__':
    import sys
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "buy":
                historicalToCsv()

            if sys.argv[1] == "history":
                convertToDask.directory = "historical"
                createRollingData.dir = "historicalCalculated"
                convertToDask()

    except Exception as e:
        print (str(e))
        pass

