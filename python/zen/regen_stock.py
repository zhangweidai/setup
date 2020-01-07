import z
import buy
import os
from sortedcontainers import SortedSet
import update_history

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
def process(astock):
    global problems
    try:
        latestprices = dict()
        problems = [] 
        df = update_history.getDataFromYahoo(astock, date)
        if df is None:
            problems.append(astock)
            return
#            print("astock: {}".format( astock))
#            print ("problem")
#            exit()
#        df = z.getp("temp")

        lastyear = None
        f = None
        for idx in df.index:
            cdate = str(idx.to_pydatetime()).split(" ")[0]
            cyear = cdate.split("-")[0]
            if cyear != lastyear:
                if f is not None:
                    f.close()
                apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, cyear))
                if os.path.exists(apath):
                    print("apath : {}".format( apath ))
                    continue
                lastyear = cyear                                                              
                f = open(apath, "w")
                f.write("Date,Open,High,Low,Close,Adj Close,Volume\n")

            opend = df.at[idx, "Open"]
            high = df.at[idx, "High"]
            low = df.at[idx, "Low"]
            closed = df.at[idx, "Close"]
            adj = df.at[idx, "Adj Close"]
            vol = df.at[idx, "Volume"]
            f.write("{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol))

    except Exception as e:
        print ("problem with gbuy")
        z.trace(e)
#        exit()

#generateWorst30()
#exit()
date = "2000-01-01"
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--skips', default=False)
    parser.add_argument('helpers', type=str, nargs='?', default = [])
    args = parser.parse_args()
    if not args.helpers:
        exit()

    astock = args.helpers.upper()
    process(astock)

#    listof = z.getp("listofstocks")
#    for astock in listof:
#        process(astock)
#    z.setp(problems, "problems", True)
