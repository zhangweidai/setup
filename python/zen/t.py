import numpy as np
import pandas as pd
import timeit
import pickle

en_de = {"red" : "rot", "green" : "grun", "blue" : "blau", "yellow": "gelb"}

def Test_pan1():
    b = [i for i in range(100000)]

def Test_pan2():
    b = [i for i in range(100000)]

def Test_pan4():
    try:
        b = [i for i in range(100000)]
    except:
        pass

def Test_pan5():
    try:
        b = [i for i in range(100000)]
    except:
        pass


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
                    number=1000)
        print (round(answer,4))

