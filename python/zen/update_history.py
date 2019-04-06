import util
import update_csv
import os
import z
import csv
import fix_yahoo_finance as yf

from pandas_datareader import data as pdr
yf.pdr_override()
def getDataFromYahoo(astock, cdate):
    df = None
    try:
        df = pdr.get_data_yahoo([astock], start=cdate)
    except Exception as e:
        try:
            df = pdr.get_data_yahoo([astock], start=cdate)
        except Exception as e:
            print (str(e))
            raise SystemExit
            return None
    
    for idx in df.index:
        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            df.at[idx, label] = round(df.at[idx, label], 3)
    return df

parentdir = util.getPath("historical")
listOfFiles = os.listdir(parentdir)
for entry in listOfFiles:
    astock = os.path.splitext(entry)[0]
    path = "{}/{}".format(parentdir,entry)
    print("path : {}".format( path ))
    for row in csv.DictReader(open(path)):
        cdate = row['Date']

    df = getDataFromYahoo(astock, cdate)
    if df is None:
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

            latest[astock] = closed 

z.setp(latest, "latestprices")

