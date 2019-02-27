import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import pandas

def regress(items):
    i = 0
    x = []
    for b in items:
        i+=1
        x.append(i)
    x = np.asarray(x)
    y = np.asarray(items)
    sub = sum(items)/len(items)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    rs = r_value**2
    normalized_err = (std_err/sub)
    if normalized_err == 0:
        normalized_err = 0.0001
    score = rs/normalized_err
    return score

def averageRegress(items):
    count = int(len(items)/3)
    first = items[:count]
    second = items[count:count*2]
    three = items[count*2:]
    f1 = regress(first) / 1.618033
    f2 = regress(second) 
    f3 = regress(three) * 1.618033
    return (f1 + f2 + f3)

from collections import deque
def dipsCounted(items):
    SIZE = 6
    dipping = 1
    currentStack = deque([])
    for price in items:
        currentStack.append(price)
        if len(currentStack) == SIZE:
            start = currentStack[0] + currentStack[1]
            end = currentStack[-1] + currentStack[-2]
            tdip = (end/start)
            if tdip < 1:
                dipping += (1-tdip)
            currentStack.popleft()
    return dipping

import math
def getFactors(items):
    one = (items[-50] + items[-50])/2
    two = (items[-180] + items[-181])/2
    final = (items[-1] + items[-2])/2

    return round((((final/two)+1)/7)+(((final/one)+1)/2),5)

def getScore(items):
    num =  averageRegress(items)
    bottom = dipsCounted(items)
    return (num,bottom)

def getData(filename):
    path = "{}/analysis/gg_{}.csv".format(os.getcwd(), filename)
    trend = pandas.read_csv(path)
    whatdict = trend.to_dict('split')
    ret = dict()
    for company_data in whatdict['data']:
        ret[company_data[0]] = company_data[1:]
    return ret

def writeFile(dictionary, cols):
    df = pandas.DataFrame.from_dict(dictionary, orient = 'index', columns=cols)
    path = "{}/analysis/gg_{}.csv".format(os.getcwd(), cols[0])
    df.to_csv(path)


def getDiscount(items):
    idx = -1 * (int(len(items)/4))
    tvec = items[idx:]
    average = sum(tvec)/len(tvec)
    num = (items[-1] + items[-2])/2
    return round(num/average,4)

