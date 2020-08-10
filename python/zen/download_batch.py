import args
import z
z.getp.quick_list = False

import buy
import os
from sortedcontainers import SortedSet
import gbuy_old
import math

date = "2000-01-01"
dates = z.getp("dates")
import delstock
def process(astock, one_at_a_time = True):
    global problems
    try:
        problems = [] 
        print("date: {}".format( date))
        df = gbuy_old.getDataFromYahoo(astock, date)
        if df is None:
            problems.append(astock)
            print("problem dl astock: {}".format( astock))
            return

        lastyear = None
        f = None
        for idx in df.index:
            cdate = str(idx.to_pydatetime()).split(" ")[0]
            cyear = cdate.split("-")[0]
            if cyear != lastyear:
                if f is not None:
                    f.close()
                apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, cyear))
#                if os.path.exists(apath):
#                    continue
                lastyear = cyear                                                              
                f = open(apath, "w")
                f.write("Date,Open,High,Low,Close,Adj Close,Volume\n")

            try:
                opend = round(df.at[idx, "Open"],3)
                high = round(df.at[idx, "High"],3)
                low = round(df.at[idx, "Low"],3)
                closed = round(df.at[idx, "Close"],3)
                adj = round(df.at[idx, "Adj Close"],3)
                vol = df.at[idx, "Volume"]
            except:
                opend = round(df.at[idx, "Open"][0],3)
                high = round(df.at[idx, "High"][0],3)
                low = round(df.at[idx, "Low"][0],3)
                closed = round(df.at[idx, "Close"][0],3)
                adj = round(df.at[idx, "Adj Close"][0],3)
                vol = df.at[idx, "Volume"][0]

            if not math.isnan(opend):
                f.write("{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol)) 

        try:
            if cdate != dates[-1]:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! MISSING TODAY {}".format(astock))
                delstock.delstock(astock)
                exit()
        except:
            pass

        
    except Exception as e:
        print ("problem with gbuy_old")
        z.trace(e)
        exit()

def genNeeded():
    mcdic2 = z.getp("mcdic2")
    needed = list()
    bar = list()
    for astock,items in mcdic2.items():
        if items[0] >= 65 and astock not in stocks and not astock[-1].islower():

            try:
                info = buy.getFrom("savemeinfo2", astock)
                if info["Average Vol. (3m)"] < 15000:
                    continue
            except:
                pass

            needed.append(astock)
            bar.append((items[0],astock))
    return needed

if __name__ == '__main__':
    import args    

    needed = z.getp("temp_needed")
    stocks = z.getp("listofstocks")

    print("stocks: {}".format( len(stocks)))
    for astock in needed:
        print("astock : {}".format( astock ))
        process(astock)
        stocks.append(astock)
    print("stocks: {}".format( len(stocks)))
    z.setp(stocks, "listofstocks")


