import timeit
import util

#import debug
#debug.dipScore.mode = 2
#print(debug.dipScore())
#debug.dipScore.mode = 2
#print(debug.dipScore())
#raise SystemExit

#df = util.getCsv("BA")
#interval  = 15
#start  = 1005
#end  = 1030
def igest_2():
    for i in df.index:
        if i < start or i > end:
            continue
#        if i % interval:
#            continue
        val = df['Date'].iloc[-1]
        val = df['Close'].iloc[-1]
        val = df['Open'].iloc[-1]
        val = df['Low'].iloc[-1]
        val = df['High'].iloc[-1]
import zprep
import z
def doit(stocks):
    for astock in stocks:
        pass

#stocks = z.getStocks()
def doitg():
    global stocks
    for astock in stocks:
        pass
import csv
def process2(astock, col, date):
    if process2.inputf is None:
        path = z.getPath("delme2/{}.csv".format(astock))
        process2.inputf = csv.DictReader(open(path))
    for row in process2.inputf:
        if row['Date'] == date:
            return row[col]
process2.inputf = None
def process(astock, col, date):
    path = z.getPath("delme2/{}.csv".format(astock))
    inputf = csv.DictReader(open(path))
    for row in inputf:
        if row['Date'] == date:
            return row[col]
#        print("row : {}".format( row[col] ))
#        print("col: {}".format( col))
#        myset[row[col]] = row["Date"]

import test
from collections import OrderedDict

def Test1():
    dates = OrderedDict()
    for astock in test.stocks:
        test.process(astock, "Open", dates, True)

def Test2():
    dates = OrderedDict()
    for astock in test.stocks:
        test.process(astock, "Open", dates, False)

#print("process2: {}".format(process("BA", "Open", "2000-01-18")))
#raise SystemExit

#def Test_1():
#    doitg()
#
#def Test_2():
#    global stocks
#    doit(stocks)

def est_1():
    endi = df.tail(1).index.item()
    for idx in df.index:
        if idx < start or idx > end:
            continue
        val = df.at[endi, 'Date']
        val = df.at[endi, 'Close']
        val = df.at[endi, 'Open']
        val = df.at[endi, 'Low']
        val = df.at[endi, 'High']
def est_3():
    endi = len(df)-1
    for idx in df.index:
        if idx < start or idx > end:
            continue
        val = df.at[endi, 'Date']
        val = df.at[endi, 'Close']
        val = df.at[endi, 'Open']
        val = df.at[endi, 'Low']
        val = df.at[endi, 'High']



#def Test_slow():
#    for i,row in df.iterrows():
#        if i < start or i > end:
#            continue
##        if i % interval:
##            continue
#        val = row["Close"]
#        val = row["Open"]
#        val = row["Low"]
#        val = row["High"]
#
#Test_3()
#raise SystemExit
#def Test_1():
#    for idx in df.index:
#        if idx < start or idx > end:
#            continue
#        val = df['Date'][df.index[-1]]
#        val = df['Close'][df.index[-1]]
#        val = df['Open'][df.index[-1]]
#        val = df['Low'][df.index[-1]]
#        val = df['High'][df.index[-1]]

#        val = df.at[endi, "Close"]
#        val = df.at[endi, "Open"]
#        val = df.at[endi, "Low"]
#raise SystemExit
#def Test_panpold():
#    for idx,row in df.iterrows():
#        if idx < start or idx > end:
#            continue
#        if idx % interval or idx == 0:
#            continue
#        val = row['Date']
#        val = row['Close']
#        val = row['Open']
#        val = row['Low']


#Test_panp()
#print("Test_panp:")
#
#Test_get_value()
#raise SystemExit
#def Test_pan1():
#    reload(util)
#def Test_pant():
#    reload(test)

#en_de = {"red" : "rot", "green" : "grun", "blue" : "blau", "yellow": "gelb"}

#df = util.getCsv("BA")
#def Test_pan1():
#    pd.Index(df["Date"]).get_loc("2018-12-28")
#util.getStocks.totalOverride = True
#df = util.getCsv("SPY")
#stocks = util.getStocks()
#print("stocks : {}".format( len(stocks)))
#print("stocks : {}".format( len(df)))
#def Test_pan2():
#    global df
#    for idx,row in df.iterrows():
#        if idx % 50:
#            continue
#        for astock in stocks:
#            df = util.getCsv(astock)
#            try:
#                list(df["Date"]).index("2018-12-28")
#            except:
#                pass

#Test_pan2()
#def Test_pan1():
#    for x in range(0,3000):
#        b = [i for i in range(100)]
#        helper(b)
#
#car = None
#def Test_pan2():
#    global car
#    for x in range(0,3000):
#        car = [i for i in range(100)]
#        helper2()
#
#def helper(bar):
#    accum = 0
#    for b in bar:
#        accum += b
#
#def helper2():
#    accum = 0
#    for b in car:
#        accum += b


#    try:
#        b = [i for i in range(100000)]
#    except:
#        pass
#
#def Test_pan5():
#    try:
#        b = [i for i in range(100000)]
#    except:
#        pass


#def Test_pan1():
#    pd.DataFrame([en_de]).to_csv("name.csv")
#def Test_num1():
#    np.save("what", en_de)
#def Test_num2():
#    np.load("what.npy")
#def Test_pickle():
#    pickle.dump(en_de, open("delme", "wb"))
#def Test_pickle2():
#    pickle.load(open("delme", "rb"))
#def Test_pan2():
#    pd.read_csv("name.csv")

#from math import sqrt
#def Test1(needed = 30):
#    return [round(sqrt(i), 2) for i in range(needed)]
#b = Test1()
#pickle.dump(b, open("delme", "wb"))
#def Test2():
#    return pickle.load(open("delme", "rb"))

if __name__ == '__main__':
    methods = dir()
    times = list()
    names = list()
    for method in methods:
        if not "Test" in method:
            continue

        print (method)
        names.append(method)
        answer = timeit.timeit("{}()".format(method), 
                    setup="from __main__ import {}".format(method),
                    number=400)
        times.append(answer)
        print (round(answer,4))

    if len(times) > 1:
        mint = min(times)
        maxt = max(times)
        idx = times.index(mint)
        from termcolor import colored
        msg = "\n{} is {:.2%} faster".format(names[idx], (maxt/mint)-1)
        print (colored(msg, "green"))
