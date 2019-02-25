from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import datetime
import stock_analyze

def getData(filename):
    path = "{}/analysis/gg_{}.csv".format(os.getcwd(), filename)
    trend = pandas.read_csv(path)
    whatdict = trend.to_dict('split')
    ret = dict()
    for company_data in whatdict['data']:
        ret[company_data[0]] = company_data[1:]
    return ret

trend_dict = getData("trending")
drop_dict = getData("365_drop")
json_dict = getData("json")
#print (trend_dict)
#print (drop_dict)
#print (json_dict)

#,%Down,%Up,Change
#gg_trending.csv
#{'MSFT': [0.25, 0.3329, 1.028]}

#gg_json.csv
#,Dividend,P:MC(big is good),BETA(small),MarketCap
#{'MSFT': [0.0151, '0.089076', 1.0863, 671267.940]}

#gg_356_drop.csv
#,Start,High,Low,Last,Drop,Recover,TotalChange,Score,HighDate,LowDate,DropTime
#{'MSFT': [74.31, 116.18, 72.92, 110.97, 0.628, 1.521, 1.493, 3.804, '2018-10-03', '2019-02-22', 179]}

recent_change_idx = 2
drop_idx = 4
l_idx = 2
h_idx = 1
la_idx = 3
score_idx = 7
dividend_idx = 0
beta_idx = 2
pmc_idx = 1
cap_idx = 3
#mine.process(
stocks = stock_analyze.getStocks("IVV")
#stocks = ["MSFT"]
ret_dict = dict()
import math
for astock in stocks:
    try: 
        cap  = round(json_dict[astock][cap_idx],4)
    except:
        cap = "NA"

    try: 
        pmc = json_dict[astock][pmc_idx]
    except:
        pmc = "NRP"

    if pmc == "NRP":
        pmc = 0
    else:
        pmc = round(float(pmc),4)

    try:
        discount  = trend_dict[astock][recent_change_idx]
    except:
        discount = 1
    if discount > 1:
        discount = discount * discount

    try:
        dropscore = drop_dict[astock][drop_idx]
        lows = drop_dict[astock][l_idx]
        highs = drop_dict[astock][h_idx]
        lasts = drop_dict[astock][la_idx]
    except:
        continue

    try:
        score = drop_dict[astock][score_idx]
    except:
        continue

    if score > 10:
        score = 10

    try:
        dividend = 10*json_dict[astock][dividend_idx]
    except:
        dividend = 0

    value = score + (1.5*dividend) + pmc

    final = round(value / discount, 4)
    ret_dict[astock] = [final, round(discount,4), round(dividend,4), cap, dropscore, lows, highs, lasts]

df = pandas.DataFrame.from_dict(ret_dict, orient = 'index', 
                                columns=["Final", "Recent Change", "Dividend", "MCap", "Drop", "Low", "High", "Last"])
path = "{}/analysis/gg_final.csv".format(os.getcwd())
df.to_csv(path)

