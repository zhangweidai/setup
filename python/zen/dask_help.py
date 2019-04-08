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
def convertToDask(simple = False):
    global dfd
    path = z.getPath(convertToDask.directory)
    print ("reading {}".format(path))
    dfd = dd.read_csv('{}/*.csv'.format(path), include_path_column = (not simple))

    if not simple:
        dfd = dfd.drop(['Adj Close'], axis=1)
        dfd['path'] = dfd['path'].map(lambda x: getName(x))

    dfd['Change'] = dfd.Close/dfd.Open
    dfd['Change'] = dfd['Change'].map(lambda x: round(x,4))

    print ("begin rolling")
    createRollingData()

    if not simple:
        import generate_list
        generate_list.regenerateHistorical()
convertToDask.directory = "historical"

def getModes():
    if getModes.override:
        return getModes.override
    return ['C3', 'C6', 'C12', 'C30', 'S30', 'C50', 'S12','A3', "P12", "Change", "Volume"]
getModes.override = None

def threader():
    global q
    while True:
        doone(q.get())
        q.task_done()
q = None
def createRollingData():
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
        q.put([indx])

    q.join()

def doone(indx):
    global dfd
    indx = indx[0]
    try:
        computed = dfd.get_partition(indx).compute()
        name = computed.path[0]
        path = z.getPath("{}/{}.csv".format(createRollingData.dir, name))

        computed['C3'] = (computed.Close/computed.Open.shift(3))\
            .map(lambda x: round(x,4))

        computed['C6'] = (computed.Close/computed.Open.shift(6))\
            .map(lambda x: round(x,4))

        computed['C12'] = (computed.Close/computed.Open.shift(12))\
            .map(lambda x: round(x,4))

        computed['C30'] = (computed.Close/computed.Open.shift(30))\
            .map(lambda x: round(x,4))

        computed['C50'] = (computed.Low/computed.High.shift(50))\
            .map(lambda x: round(x,4))

        computed['temp'] = computed.Close.map(lambda x: round(x**(.12),4))
        computed['P12'] = (computed.temp/computed.C12).map(lambda x: round(x,4))
        computed['S30'] = (computed.C30/(computed.C6*computed.Change)).map(lambda x: round(x,4))
        computed['S12'] = (computed.C12/computed.C3).map(lambda x: round(x,4))

        computed['A3'] = computed.Change.rolling(3).mean()\
            .map(lambda x: round(x,4))

        computed['Volume'] = computed.Volume.rolling(5).mean()\
            .map(lambda x: round(x,4))

        computed.to_csv(path)
        print("done indx : {}".format( indx ))

    except Exception as e:
        z.trace(e)
        pass

createRollingData.dir = "historicalCalculated"

#if __name__ == '__main__':
def historicalToCsv():
    import csv
    stocks = z.getStocks()
    howmany = 52
    dates = z.getp("dates")
    print("latest date : {}".format(dates[-1]))
    starti = dates[-1 * howmany]

    convertToDask.directory = "csv"
    createRollingData.dir = "csvCalculated"

    try:
        import shutil
        tpath = z.getPath("csv")
        shutil.rmtree(tpath)
        tpath = z.getPath("csvCalculated")
        shutil.rmtree(tpath)
    except:
        pass

    for astock in stocks:
        path = z.getPath("historical/{}.csv".format(astock))
        tpath = z.getPath("csv/{}.csv".format(astock))
#        if os.path.exists(tpath):
#            continue

        with open(tpath, "w") as f:
            f.write("Date,Open,Close,High,Low,Volume,path\n")
            starting = False
            for row in csv.DictReader(open(path)):
                cdate = row['Date']
                if cdate == starti:
                    starting = True
    
                if starting:
                    f.write("{},{},{},{},{},{},{}\n".format(\
                        cdate,row['Open'],row['Close'],row['High'],row['Low'],row['Volume'],astock))
    convertToDask(simple=True)

if __name__ == '__main__':
    import sys
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "buy":

                z.getStocks.devoverride = "IUSG"
                z.getStocks.extras = True
                historicalToCsv()

            if sys.argv[1] == "history":
                convertToDask.directory = "historical"
                createRollingData.dir = "historicalCalculated"
                convertToDask()

    except Exception as e:
        z.trace(e)
        pass

