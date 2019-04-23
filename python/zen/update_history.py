import util
import update_csv
import os
import z
import csv
import datetime
import fix_yahoo_finance as yf
import zprep

from pandas_datareader import data as pdr
yf.pdr_override()
problems = list()
def getDataFromYahoo(astock, cdate):
    print("astock: {}".format( astock))
    global problems
    df = None
    try:
        df = pdr.get_data_yahoo([astock], start=cdate)
    except Exception as e:
        try:
            df = pdr.get_data_yahoo([astock], start=cdate)
        except Exception as e:
            z.trace(e)
            problems.append(astock)
#            raise SystemExit
            return None
    
    for idx in df.index:
        try:
            change = df.at[idx, "Close"]/df.at[idx+1, "Close"]
            if change > 5 or change < 0.15 or df.at[idx, "Volume"] == 0:
                print ("may have problem {}".format(astock))
        except Exception as e:
#            z.trace(e)
            pass

        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            df.at[idx, label] = round(df.at[idx, label], 3)

    return df

def update():
    parentdir = util.getPath("historical")
    print("parentdir : {}".format( parentdir ))
    listOfFiles = os.listdir(parentdir)
    for entry in listOfFiles:
        astock = os.path.splitext(entry)[0]
#        print("astock : {}".format( astock ))
        path = "{}/{}".format(parentdir,entry)
#        if "ZS" in path:
#            print("path : {}".format( path ))
    
        t = os.path.getmtime(path)
        csvdate = datetime.datetime.fromtimestamp(t)
        csvday = csvdate.day
        csvmonth = csvdate.month
        ttoday = datetime.date.today().day
        tmonth = datetime.date.today().month
#        if astock == "ZS":
#            print("ttoday : {}".format( ttoday ))
#            print("tmonth : {}".format( tmonth ))
        if csvday >= ttoday and tmonth == csvmonth:
            continue
    
        for row in csv.DictReader(open(path)):
            cdate = row['Date']
    
#        print("cdate : {}".format( cdate ))
#        raise SystemExit
#        if cdate == "2019-04-18":
#            continue
#            latest.append(astock)
#        continue

        df = getDataFromYahoo(astock, cdate)
        if df is None:
            print("this is not good updatehistory astock: {}".format( astock))
            raise SystemExit
            continue
    
        skipped = False
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
                f.write("{},{},{},{},{},{},{}\n".format(\
                            cdate, opend, high, low, closed, adj, vol))
    #            latest[astock] = closed 
    zprep.setStockDays() 
    return True

if __name__ == '__main__':
#    import sys
#    import dask_help
    update()
    print(problems)
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
    
