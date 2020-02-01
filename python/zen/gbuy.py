import z
import buy
import os
from sortedcontainers import SortedSet
import glob
import yfinance as yf
from pandas_datareader import data as pdr

year = "2020"

yf.pdr_override()
def getDataFromYahoo(astock, cdate):
    df = None
    try:
        print("astock: {}".format( astock))
        df = pdr.get_data_yahoo([astock], start=cdate)
    except Exception as e:
        try:
            df = pdr.get_data_yahoo([astock], start=cdate)
        except Exception as e:
            z.trace(e)
            return None
    
#    for idx in df.index:
#        print("idx : {}".format( idx ))
#        print("idx : {}".format( df.at[idx+1, "Close"] ))
#        try:
#            change = df.at[idx, "Close"] / df.at[idx+1, "Close"]
#            if change > 5 or change < 0.15 or df.at[idx, "Volume"] == 0:
#                print ("may have problem {}".format(astock))
#        except Exception as e:
#            z.trace(e)
#            pass

#        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
#            print (df.at[idx, label][0])
#        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
#            df.at[idx, label][0] = round(df.at[idx, label][0], 3)

    return df

def setlistofstocks():
    path = z.getPath("split/*/*{}.csv".format(year))
    files = glob.glob(path)
    stocks = [ os.path.splitext(os.path.basename(entry))[0].replace("_{}".format(year), "") for entry in files ]
    z.setp(stocks, "listofstocks")

    etfs = z.getEtfList()
    listofs = list()
    for astock in stocks:
        if astock in etfs:
            continue;
        listofs.append(astock)
    z.setp(listofs, "listofs")


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


#generateWorst30()
#exit()
if __name__ == '__main__':
    import argparse
    import csv
    import datetime

    parser = argparse.ArgumentParser()
    parser.add_argument('--skips', default=False)
    args = parser.parse_args()

    setlistofstocks()

    try:
        latestprices = dict()
        problems = [] 
        skips = list()
        if args.skips:
            skips = z.getp("problems")
            print("skips : {}".format( skips ))
        stocks = z.getp("listofstocks")

        import datetime
        now = datetime.datetime.now()
        missed = 0
        for astock in stocks:

            if astock in skips:
                continue

            apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
            try:
                t = os.path.getmtime(apath)
            except:
                continue

            csvdate = datetime.datetime.fromtimestamp(t)
            csvday = csvdate.day
            csvmonth = csvdate.month
            ttoday = datetime.date.today().day
            tmonth = datetime.date.today().month

            if csvday >= ttoday and tmonth == csvmonth:
                missed = 0
                continue

            for row in csv.DictReader(open(apath)):
                pass
            try:
                date = row['Date']
            except:
                continue

            print("date: {}".format( date))
            df = getDataFromYahoo(astock, date)
            if df is None:
                print("problem downloading: {}".format( astock))
                missed += 1
                if missed > 5:
                    problems.append(astock)
                    print("problems : {}".format( problems ))
                    z.setp(problems, "problems")
                    exit()
                continue
            missed = 0
            with open(apath, "a") as f:
                first = True
                for idx in df.index:
                    if first:
                        first = False
                        continue
                    cdate = str(idx.to_pydatetime()).split(" ")[0]
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
                    added = True
                    f.write("{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol))

        buy.updateDates()

        import prob_down_5_years
        prob_down_5_years.prob()

        import gained_discount
        gained_discount.dosomething()
        gained_discount.genUlt()


        import drop_finder
        drop_finder.procs()

        buy.genRecentStats()

    except Exception as e:
        print ("problem with gbuy")
        z.trace(e)
        exit()


