import z 
import matplotlib.pyplot as plt

import operator
import random
import sys
from random import sample
import numpy as np
from collections import defaultdict

dates = z.getp("dates")
interval = 7
num_days = len(dates)
print("num_days : {}".format( num_days ))
etfsource = "IUSG"
stocks = z.getStocks(etfsource)
#stocks.sort()

def getBuyStocks(idxdate, mode, howmany=1):
    thedayh=dict()
    thedayl=dict()
    thedayll=dict()
    for astock in stocks:

        df = z.getCsv(astock)
        if df is None:
            print("problem astock: {}".format( astock))
            continue

        df_dates = df["Date"].tolist() 
        try:
            starti = df_dates.index(idxdate)
            if not starti:
                print("did not find start date astock: {} {}".\
                        format( astock, idxdate))
                continue
        except Exception as e:
            print(df_dates.iloc[-1])
            print (str(e))
            print("astock: {}".format( astock))
            raise SystemExit
            continue

        try:
            close = df.at[starti,"Close"]
            if close < 2:
                continue

            changeh = round(close/df.at[starti-3,"Open"],3) 
            changel = round(close/df.at[starti-3,"Open"] - 
                     (close/df.at[starti-8,"Open"])/2,3)
            changell = round(close/df.at[starti-3,"Open"],3)

        except Exception as e:
            print ("str(e)")
            print (str(e))
            continue

        if changeh > 1:
            thedayh[astock] = round(changeh,4)
        if changel < 1:
            thedayl[astock] = round(changel,4)
        if changell < 1:
            thedayll[astock] = round(changell,4)

    sorted_xl = sorted(thedayl.items(), key=operator.itemgetter(1))
    sorted_xll = sorted(thedayll.items(), key=operator.itemgetter(1))
    sorted_xh = sorted(thedayh.items(), key=operator.itemgetter(1))

    try:
        if mode == "high":
            return sample(sorted_xh[-6:],2)
        elif mode == "low":
            return sample(sorted_xl[:6],2)
        elif mode == "lowlow":
            return sample(sorted_xll[:6],2)
    except:
        print("sorted_xl: {}".format( sorted_xl))
        print("sorted_xh: {}".format( sorted_xh))
        raise SystemExit

    try:
        return [sample(sorted_xh[-6:],howmany), sample(sorted_xl[:6],howmany)]
    except:
        print("orted_xl: {}".format( sorted_xl))
        print("orted_xh: {}".format( sorted_xh))
        raise SystemExit

print(getBuyStocks("2019-03-27", mode="both", howmany=3))
