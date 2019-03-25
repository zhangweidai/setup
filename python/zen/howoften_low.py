import util
import operator
from collections import defaultdict
util.getCsv.savedReads = util.getp("allcsvs")

#util.getStocks.totalOverride = "IUSG"
spdf = util.getCsv("SPY")
stocks = util.getStocks()
print("stocks : {}".format( len(stocks)))
lastcount = len(spdf)-1

ayear = 252
years = 2.2
duration = int (years * ayear)
highs = []
lows = []
total = 0
interval = 3

def getHighLowList(qdate):
    thedayh = dict()
    thedayl = dict()
    thedayll = dict()
#    tstocks = sample(stocks,400)
    for astock in stocks:

        df = util.getCsv(astock)
        if df is None:
            continue

        try:
            dates = list(df["Date"])
            starti = dates.index(qdate)
            if not starti:
                continue
        except:
            continue

        try:
            close = df.at[starti,"Close"]
            if close < 2:
                continue

            changeh = round(close/df.at[starti-3,"Open"],3) 
            changel = round(close/df.at[starti-3,"Open"] - close/df.at[starti-8,"Open"], 4)
            changell = round(close/df.at[starti-3,"Open"], 4)

        except Exception as e:
            continue

        if changeh > 1:
            thedayh[astock] = round(changeh,4)
        if changel < 1:
            thedayl[astock] = round(changel,4)
        if changell < 1:
            thedayll[astock] = round(changell,4)


    sorted_xl = sorted(thedayl.items(), key=operator.itemgetter(1))
    sorted_ll = sorted(thedayll.items(), key=operator.itemgetter(1))
    sorted_xh = sorted(thedayh.items(), key=operator.itemgetter(1))
    sh = sorted_xh[-12:]
    sl = sorted_xl[:12]
    sll = sorted_ll[:12]
    rh = list(zip(*sh))[0]
    rl = list(zip(*sl))[0]
    rll = list(zip(*sll))[0]
    return rh, rl, rll

#a = getHighLowList("2019-03-22")
def doit():

    report = defaultdict(int)
    report2 = defaultdict(int)
    for idx in range(9,lastcount-duration-1):
        if idx % interval:
            continue

        qdate = spdf.at[idx,"Date"]
        edate = spdf.at[idx+duration,"Date"]

        lists = getHighLowList(qdate)
        alls = [i for sub in lists for i in sub]

        for astock in stocks:
            if astock not in alls:
                continue

            df = util.getCsv(astock)

            dates = list(df["Date"])
            try:
                starti = dates.index(qdate)
                if not starti:
                    continue
            except:
                continue

            try:
                endi = dates.index(edate)
                if not endi:
                    continue
            except:
                continue

            group = 0
            for i,alist in enumerate(lists):
                if astock in alist:
                    group = i
                    continue

            try:
                opened = df.at[starti, "Open"]
                closed = df.at[endi, "Close"]
                change = closed / opened
                if change > 1.05:
                    report[group] += 1
                    report2[group] += change
            except:
                print("astock : {}".format( astock ))
                continue

    print(report)
    print(report2)

doit()

