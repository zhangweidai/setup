import os
import z
import csv
import yfinance as yf
from pandas_datareader import data as pdr

closekey = z.closekey
yf.pdr_override()
problems = list()
def getDataFromYahoo(astock, cdate):
    global problems
    df = None
    try:
        print("astock: {}".format( astock))
        df = pdr.get_data_yahoo([astock], start=cdate)
    except Exception as e:
        try:
            df = pdr.get_data_yahoo([astock], start=cdate)
        except Exception as e:
            problems.append(astock)
            return None
    
    for idx in df.index:
        try:
            change = df.at[idx, "Close"] / df.at[idx+1, "Close"]
            if change > 5 or change < 0.15 or df.at[idx, "Volume"] == 0:
                print ("may have problem {}".format(astock))
        except Exception as e:
            pass

        for label in ["Open", "Close", "High", "Low", "Adj Close"]:
            df.at[idx, label] = round(df.at[idx, label], 3)

    return df
