import numpy as np
import pandas as pd
import timeit
from importlib import reload
import util
import math
import test
import numpy
#import debug
#debug.dipScore.mode = 2
#print(debug.dipScore())
#debug.dipScore.mode = 2
#print(debug.dipScore())
#raise SystemExit

df = util.getCsv("BA")
interval  = 15
def Test_get_value():
    for i in df.index:
        if i < start or i > end:
            continue
        if i % interval or i == 0:
            continue
        val = df.get_value(i,'Date')
        print("val : {}".format( val ))

def Test_panp():
    for i,row in df.iterrows():
        if idx < start or idx > end:
            continue
        if idx % interval or idx == 0:
            continue
        val = row['Date']
        print("val : {}".format( val ))


Test_panp()
Test_get_value()
raise SystemExit
#def Test_pan1():
#    reload(util)
def Test_pant():
    reload(test)

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
    for method in methods:
        if not "Test" in method:
            continue
        print (method)
        answer = timeit.timeit("{}()".format(method), 
                    setup="from __main__ import {}".format(method),
                    number=10000)
        print (round(answer,4))

