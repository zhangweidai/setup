import util
import operator
from collections import defaultdict
#util.getCsv.csvdir = "historical"
spdf = util.getCsv("SPY")
#stocks = util.getStocks(ivv=True)
stocks = util.getStocks()
every = 5
bought_low = defaultdict(int)
bought_high = defaultdict(int)
lowpaid = 0
highpaid = 0

offsets = defaultdict(lambda:None)
avgchangel = list()
avgchangeh = list()
avgchangels = list()
avgchangehs = list()
lastcount = len(spdf)-1

tracks = 10
original = 1000
spend = original
threshold = 1.07
fee = 10
miniport = dict()
def doit():
    for idx,row in spdf.iterrows():
        if idx % 5:
            continue
        cdate = row["Date"]
        theday = dict()
        minv = 10
        lowstock = None
        for astock in stocks:
            df = util.getCsv(astock)
            if df is None:
                print("astock: {}".format( astock))
                continue
    
            if offsets.get(astock) == None:
                dates = list(df["Date"])
                try:
                    starti = dates.index(cdate)
                    offsets[astock] = idx-starti
                except:
                    continue
    
            off = offsets[astock]
            if off == None:
                continue
    
            myidx = idx - off
            try:
                change = round(df.at[myidx,"Close"]/df.at[myidx,"Open"],3)
            except:
                continue
    
            if change < minv:
                lowstock = astock
                minv = change
    
#        df = util.getCsv(lowstock)
#        if len(df)-1 != lastcount:
#            continue

        stock_count = len(miniport)
        if stock_count < tracks:
            if lowstock not in miniport:
                myidx = idx - offsets[lowstock]
                miniport[lowstock] = buySomething(myidx, lowstock)
        else:
            sell(cdate)

    print("lastcount : {}".format( lastcount ))
    portvalue()

def portvalue():
    total = 0
    for astock in miniport:
        cprice = util.getPrice(astock)
        item = miniport[astock]
        cvalue = (cprice * item[0])-fee
        total += cvalue

    print("total : {}".format( total ))
    print("change : {}".format(util.formatDecimal( total/(tracks*original))))

def sell(cdate):
    global spend
    print ("\tselling time")
    sold = None
    print("cdate: {}".format( cdate))
    for astock in miniport:
        cprice = util.getPrice(astock, cdate)
        item = miniport[astock]
        cvalue = (cprice * item[0])-fee
        soldvalue = cvalue/item[1]
        if soldvalue > threshold:
            print("selling : {} {}".format(astock, cvalue))
            spend = cvalue
            sold = astock
            break
    if sold:
        del miniport[astock]

def buySomething(myidx, lowstock):
    df = util.getCsv(lowstock)
    bought = round(df.at[myidx + 1,"Open"])
    count = round((spend-fee)/bought,3)
    print("bought: {}".format( bought))
    print("lowstock: {}".format( lowstock))
    print("count: {}".format( count))
    return [count, spend]

doit()
