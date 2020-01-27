import util
import numpy as np
from collections import defaultdict
from scipy import stats
lengm = 7 * 12
def doit(df, durdays):
    subtotal = list()
    for idx in df.index:
        if idx % 2:
            continue
        if idx > durdays:
            opened = df.at[idx-durdays, "High"]
            close = df.at[idx, "Close"]
            change = round(close/opened, 5)
            subtotal.append(change)
    return round(sum(subtotal)/len(subtotal),5)

listx = range(1, lengm, 2)
def getScore(astock):
    df = util.getCsv(astock, save=False)
    listy = []
    for month in listx:
        durdays = month * 21
        listy.append(doit(df, durdays))
 
    maxv = max(listy)
    idx = listy.index(maxv)
    when = listx[idx] 
    bar = [str(i) for i in listy]
    items = "|".join(bar)
    slope, intercept, r_value, p_value, std_err = stats.linregress(listx,listy)
    ret = [astock,1+(round(slope * r_value,5)*10), when, maxv, items]
    ret = [str(i) for i in ret]
    return "{}\n".format(",".join(ret))

from filelock import FileLock
def getScoreLocked(astock):
    try:
        score = getScore(astock)
    except:
        return

    with FileLock("myfile.txt.lck"):
        path = util.getPath("report/scores_new.csv")
        open(path,"a").write(score)
        print ("written " + astock)

def getEm():
    stocks = util.getStocks()
    print("stocks : {}".format(len(stocks)))
    path = util.getPath("report/scores2.csv")
    with open(path, "a") as f:
#        row = ",".join(["Ticker", "Score", "Months", "Value", "Values"])
#        f.write(row)
#        f.write("\n")
#        f.flush()
        for i,astock in enumerate(stocks):
#            if i < 83: 
#                continue
            print (i)
            try:
                f.write(getScore(astock))
                f.flush()
            except Exception as e:
                print ('FailedWrite: '+ str(e))
                print("problem astock: {}".format( astock))
                pass
            break

#    util.writeFile(saved, ["Score", "Months", "Value", "Values"], directory="report", name = "scores")
#getEm()
#print (getScore("AMD"))
#print (getScore("IUSG"))
#print (getScore("SPY"))
