import z
import buy
import os
from sortedcontainers import SortedSet
year = "2020"

import glob
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
    import update_history
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
#            if not os.path.exists(apath):
#                continue

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
            df = update_history.getDataFromYahoo(astock, date)
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
                    opend = df.at[idx, "Open"]
                    high = df.at[idx, "High"]
                    low = df.at[idx, "Low"]
                    closed = df.at[idx, "Close"]
                    adj = df.at[idx, "Adj Close"]
                    vol = df.at[idx, "Volume"]
                    added = True
                    f.write("{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol))

        buy.updateDates()

        import prob_down_5_years
        prob_down_5_years.prob()

        import gained_discount
        gained_discount.dosomething()
        gained_discount.genUlt()

        buy.genRecentStats()

#        print("problems : {}".format( problems ))
#        z.setp(problems, "problems")
#            generateWorst30()
#            import buyat
#            buyat.runmain()


    except Exception as e:
        print ("problem with gbuy")
        z.trace(e)
        exit()


