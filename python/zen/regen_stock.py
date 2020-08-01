import args
import z
z.getp.quick_list = False

import buy
import os
from sortedcontainers import SortedSet
import gbuy_old
import math

date = "2000-01-01"

def generateWorst30():
    dates = z.getp("dates")
    stocks = z.getp("listofstocks")
    yearlydic = z.getp("latestAnnual")
    answer = SortedSet()
    for idx,astock in enumerate(stocks):
        mcrank = buy.getMCRank(astock)
        try:
            if int(mcrank) > 320:
                continue
            price = buy.getPrice(astock, dates[-252])
            if price < 5:
                continue
        except Exception as e:
            continue

        try:
            annual = yearlydic[astock]
        except:
            print("missing annual for : {}".format( astock))
            continue

        answer.add((annual, astock))
        if len(answer) > 30:
            answer.remove(answer[-1])

    print("answer: {}".format( answer))
    z.setp(answer, "worst30")

problems = list()

def process(astock, one_at_a_time = True):
    dates = z.getp("dates")
    global problems
    try:
        latestprices = dict()
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
            print("cdate : {}".format( cdate ))
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

#            opend = df.at[idx, "Open"]
#            high = df.at[idx, "High"]
#            low = df.at[idx, "Low"]
#            closed = df.at[idx, "Close"]
#            adj = df.at[idx, "Adj Close"]
#            vol = df.at[idx, "Volume"]
            if not math.isnan(opend):
                f.write("{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol)) 

        if cdate != dates[-1]:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! MISSING TODAY {}".format(astock))

        stocks = z.getp("listofstocks")
        print("stocks : {}".format( stocks ))
        if astock not in stocks:
            import json_util
            json_util.parses([astock], addone = True)
            stocks.append(astock)
            z.setp(stocks, "listofstocks")

        
    except Exception as e:
        print ("problem with gbuy_old")
        z.trace(e)


if __name__ == '__main__':


#    stocks = z.getp("listofstocks")
#    for missing, astock in stocks:
#        process(astock, False)
#    exit()

#    import argparse
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--skips', default=False)
#    parser.add_argument('helpers', type=str, nargs='?', default = [])
#    args = parser.parse_args()
#    if not args.helpers:
#        exit()

#    args.args.full = True
    import json_util
    for astock in stocks:
        process(astock)
    json_util.parses(stocks, update=True, addone = True)


