import util
import update_csv
import os
import z
import csv
import datetime
import fix_yahoo_finance as yf
import zprep

closekey = z.closekey

from pandas_datareader import data as pdr
yf.pdr_override()
problems = list()
def getDataFromYahoo(astock, cdate):
#    print("astock: {}".format( astock))
    global problems
    df = None
    try:
        print("cdate: {}".format( cdate))
        print("astock: {}".format( astock))
        df = pdr.get_data_yahoo([astock], start=cdate)
        print("sdfa")
    except Exception as e:
        try:
            df = pdr.get_data_yahoo([astock], start=cdate)
        except Exception as e:
            #z.trace(e)
            problems.append(astock)
            if len(problems)>30:
                print("didn't finish problems: {}".format( problems))
                z.setp(problems, "problems")
                raise SystemExit
            return None
    
    for idx in df.index:
        try:
            change = df.at[idx, "Close"] / df.at[idx+1, "Close"]
            if change > 5 or change < 0.15 or df.at[idx, "Volume"] == 0:
                print ("may have problem {}".format(astock))
        except Exception as e:
#            z.trace(e)
            pass

        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            df.at[idx, label] = round(df.at[idx, label], 3)

    return df

def update(where= "historical", problems = [], attempts=0, prices = dict(), skips = list()):

    if attempts > 3:
        print ("tried too many times")
        print("problems : {}".format( problems ))
        return

    parentdir = util.getPath(where)
    print("updating : {}".format( parentdir ))

    listOfFiles = os.listdir(parentdir)
    for idx,entry in enumerate(listOfFiles):
        astock = os.path.splitext(entry)[0]
        if astock in skips:
            continue
        path = "{}/{}".format(parentdir,entry)

        if not idx % 100:
            print("idx : {}".format( idx ))
    
#        print("path: {}".format( path))
        for row in csv.DictReader(open(path)):
            pass
        prices[astock] = row['Open'], row[closekey]

        t = os.path.getmtime(path)
        csvdate = datetime.datetime.fromtimestamp(t)
        csvday = csvdate.day
        csvmonth = csvdate.month
        ttoday = datetime.date.today().day
        tmonth = datetime.date.today().month

        if csvday >= ttoday and tmonth == csvmonth:
            continue

        df = getDataFromYahoo(astock, row['Date'])
        if df is None:
            problems.append(astock)
            continue
    
        skipped = False
        added = False
        with open(path, "a") as f:
            for idx in df.index:
                if not skipped:
                    skipped = True
                    continue
        
                cdate = str(idx.to_pydatetime()).split(" ")[0]
                opend = df.at[idx, "Open"]
                high = df.at[idx, "High"]
                low = df.at[idx, "Low"]
                closed = df.at[idx, "Close"]
                adj = df.at[idx, "Adj Close"]
                vol = df.at[idx, "Volume"]
                added = True
                f.write("{},{},{},{},{},{},{}\n".format(\
                            cdate, opend, high, low, closed, adj, vol))

                prices[astock] = opend, adj

        if not added:
            problems.append(astock)

    if where == "historical":
        zprep.setStockDays() 

#    if problems:
#        attempts += 1
#        update(where=where, problems=problems, attempts=attempts, prices=prices)

    return True

if __name__ == '__main__':
#    import sys
#    import dask_help
    update()
#    update(where= "ETF")
    # use gbuy
#    try:
#        if len(sys.argv) > 1:
#            astock = sys.argv[1].upper()
#            zprep.downloadMissingHistory(astock)
#        else:
#            update()
#
#        z.getStocks.devoverride = "ITOT"
#        z.getStocks.extras = True
#        dask_help.historicalToCsv()
#
#    except Exception as e:
#        z.trace(e)
#        pass

    
    #z.setp(latest, "latestprices")
    
