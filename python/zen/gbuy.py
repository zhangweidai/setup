import z
import math
import readchar
import csv
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
        print("dl astock: {}".format( astock))
        df = pdr.get_data_yahoo([astock], start=cdate)
    except Exception as e:
        z.trace(e)
        exit()
        try:
            df = pdr.get_data_yahoo([astock], start=cdate)
        except Exception as e:
            z.trace(e)
            return None
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

problems = set()
def updateStocks():
    global problems
    import datetime
    stocks = z.getp("listofstocks")
    already_updated = 0
    try:
        now = datetime.datetime.now()
        consecutive_misses = 0

        cdate_missing = list()
        current_cday = None
        added = False
        for astock in stocks:
            apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
            try:
                csvdate = datetime.datetime.fromtimestamp(os.path.getmtime(apath))
                csvday = csvdate.day
                csvmonth = csvdate.month
                ttoday = datetime.date.today().day
                tmonth = datetime.date.today().month

                if csvday >= ttoday and tmonth == csvmonth:
                    consecutive_misses = 0
                    already_updated += 1

#                    readFile = open(apath)
#                    lines = readFile.readlines()
#                    readFile.close()
#                    if lines[-1] == lines[-2]:
#                        w = open(apath,'w')
#                        w.writelines([item for item in lines[:-1]])
#                        w.close()
            except:
                continue

            for row in csv.DictReader(open(apath)):
                pass

            try:
                date = row['Date']
                cclose = row['Adj Close']
            except:
                continue

            print("date: {}".format( date))
            df = getDataFromYahoo(astock, date)
            if df is None:
                print("problem downloading: {}".format( astock))
                consecutive_misses += 1
                if consecutive_misses > 5:
                    problems.add(astock)
                    print("problems : {}".format( problems ))
                    z.setp(problems, "problems")
                    exit()
                continue
            consecutive_misses = 0

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

                    try:
                        chg = round(adj/cclose,3)
                    except:
                        chg = 1

                    if not math.isnan(opend):
                        cclose = adj
                        added = True
                        f.write("{},{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol, chg))

            if not added:
                problems.add(astock)
                print ("problem with {}".format(astock))

    except Exception as e:
        print ("problem with gbuy")
        z.trace(e)
        exit()
    print("already_updated : {}".format( already_updated ))


def saveQuick():
    portFolioValue= z.getp("ports")
    quick = z.getp("savePs")
    quick = [ stock[1] for stock in quick ]
    quick += list(portFolioValue.keys())
    orders = z.getp("orders")
    quick += list(orders.keys())
    quick = list(set(quick))
    z.setp(quick, "quick")

if __name__ == '__main__':
    import args
    args.args.bta = True

    import datetime
    cdate = dates[-1].split("-")
    day_of_week = datetime.datetime(int(cdate[0]), int(cdate[1]),int(cdate[2])).weekday()

    if day_of_week == 4:
        args.args.noupdate = True

#    import argparse
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--noupdate', nargs='?', const=True, default=False)
#    parser.add_argument('--quick', nargs='?', const=True, default=True)
#    args = parser.parse_args()
#    print("args : {}".format( args ))

#    if args.quick == True:
#        z.getp.quick_list = True

#    stocks = z.getp("listofstocks")
    try:
        if not args.args.noupdate:
            updateStocks()
            buy.updateDates()

        print ("prob up 1 year")
        import prob_up_1_year
        prob_up_1_year.procs(stocks)

        import current
        print ("current")
        current.procs(stocks)

        buy.savePs()
        saveQuick()

#        print ("gained discout")
#        import gained_discount
#        gained_discount.genUlt()

#        print ("drop finder")
#        import drop_finder2
#        drop_finder2.procs()

#        import next_day_drop_after_gain
#        next_day_drop_after_gain.procs()

#        import historical_changes
#        historical_changes.generate()


#        print ("slow and steady")
#        import slow_and_steady
#        slow_and_steady.procs()

#        print ("recent stats")
#        import buy
#        buy.genRecentStats()

    except Exception as e:
        print ("problem with gbuy")
        z.trace(e)
        exit()

    if problems:
        print("delete problems: {}".format( problems))
        key = readchar.readkey()
        if key == "y":
            import gained_discount
            gained_discount.batchdelete(problems)

