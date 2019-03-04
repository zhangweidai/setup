from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import numpy as np
import pandas
import os
import util 

def generateTrainingData(stocks):
    dates = util.getNumberOfDates()
    allvalues = dict()
    for astock in stocks:
        path = util.getPath("csv/{}.csv".format(astock))
        allvalues[astock] = pandas.read_csv(path)['Avg'].tolist()

    for start in range(dates-149):
        end = start + 150
        percent_list = dict()
        for astock in stocks:
            values = allvalues[astock][start:end]
            try:
                percent_list[astock] = util.getMinimizedVector(values)
            except:
                print (astock)
                print (values)
                continue
        util.writeFile(percent_list, ["Final", "Dip"], "training_data", 
                       name=str(start).zfill(3))

generateTrainingData(util.getStocks("IVV", andEtfs = True, dev=True))
