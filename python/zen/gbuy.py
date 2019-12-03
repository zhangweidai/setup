import z
import buy
import os
from sortedcontainers import SortedSet

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
    try:
        latestprices = dict()
        problems = [] 
        skips = list()
#        if args.skips:
#            skips = z.getp("problems")
        stocks = z.getp("listofstocks")
        print("stocks : {}".format( len(stocks) ))
        if "IVV" in stocks:
            print("stocks : ")

        import datetime
        now = datetime.datetime.now()
        missed = 0
        for astock in stocks:
            print("astock : {}".format( astock ))

            apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, str(now.year)))
            if not os.path.exists(apath):
                continue

            t = os.path.getmtime(apath)
            csvdate = datetime.datetime.fromtimestamp(t)
            csvday = csvdate.day
            csvmonth = csvdate.month
            ttoday = datetime.date.today().day
            tmonth = datetime.date.today().month

            if csvday >= ttoday and tmonth == csvmonth:
                continue

            for row in csv.DictReader(open(apath)):
                pass
            date = row['Date']

            df = update_history.getDataFromYahoo(astock, date)
            if df is None:
                print("problem downloading: {}".format( astock))
                missed += 1
                if missed > 5:
                    exit()
                continue
            missed = 0
            with open(apath, "a") as f:
                for idx in df.index:
                    cdate = str(idx.to_pydatetime()).split(" ")[0]
                    opend = df.at[idx, "Open"]
                    high = df.at[idx, "High"]
                    low = df.at[idx, "Low"]
                    closed = df.at[idx, "Close"]
                    adj = df.at[idx, "Adj Close"]
                    vol = df.at[idx, "Volume"]
                    added = True
                    f.write("{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol))

        import prob_down_5_years
        prob_down_5_years.prob()

        import gained_discount
        gained_discount.dosomething()

        print("problems : {}".format( problems ))
#            generateWorst30()
#            import buyat
#            buyat.runmain()


    except Exception as e:
        print ("problem with gbuy")
        z.trace(e)
        exit()


