import z
import zen
import os
import csv
import datetime

def update(path, astock):
    names = []
    with open(path, 'r+') as fd:
        fd.seek(0)
        fd.truncate()
        bar = fd.readline()
        fd.seek(len(bar))
        fd.truncate()
        fd.write("hello\nbar\n")
    return

def bar():

    skipped = False
    for row in csv.DictReader(open(path)):
        break
#    prices[astock] = row['Open'], row[closekey]
#
    t = os.path.getmtime(path)
    csvdate = datetime.datetime.fromtimestamp(t)
    csvday = csvdate.day
    csvmonth = csvdate.month
    ttoday = datetime.date.today().day
    tmonth = datetime.date.today().month

#    if csvday >= ttoday and tmonth == csvmonth:
#        return
#
    df = getDataFromYahoo(astock, row['Date'])
    if df is None:
        problems.append(astock)
#    
#    skipped = False
#    added = False
#    with open(path, "a") as f:
#        for idx in df.index:
#            if not skipped:
#                skipped = True
#                continue
#    
#            cdate = str(idx.to_pydatetime()).split(" ")[0]
#            opend = df.at[idx, "Open"]
#            high = df.at[idx, "High"]
#            low = df.at[idx, "Low"]
#            closed = df.at[idx, "Close"]
#            adj = df.at[idx, "Adj Close"]
#            vol = df.at[idx, "Volume"]
#            added = True
#            f.write("{},{},{},{},{},{},{}\n".format(\
#                        cdate, opend, high, low, closed, adj, vol))
#
#            prices[astock] = opend, adj
#
#    if not added:
#        problems.append(astock)
#
#    if where == "historical":
#        zprep.setStockDays() 
#
##    if problems:
##        attempts += 1
##        update(where=where, problems=problems, attempts=attempts, prices=prices)
#
#    return True


def updateDics(listOfFiles, path):
    for idx,entry in enumerate(listOfFiles):
        if not idx % 100:
            print("idx: {}".format( idx))

        tpath = "{}/{}".format(path,entry)
        rows = list()
        with open(tpath) as f:
            rows = f.readlines()
        rows.append("")
        rows.reverse()
        rows[-1], rows[0] = rows[0], rows[-1]
        path = z.getPath('flipped/{}'.format(entry))
        with open(path, 'w') as outfile:
            outfile.write("".join(str(item) for item in rows[:-1]))

        return


path = z.getPath('historical')
listOfFiles = os.listdir(path)
#updateDics(listOfFiles, path)

def updates(listOfFiles, path):
    for idx,entry in enumerate(listOfFiles):
        path = z.getPath('flipped/{}'.format(entry))
        astock = os.path.splitext(entry)[0]
        update(path, astock)
        return

updates(listOfFiles, path)
