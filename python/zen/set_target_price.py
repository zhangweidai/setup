import pandas as pd
from util import targetPrice, setp, getStocks, getPath

targets = dict()
for astock in getStocks():
    path = getPath("csv/{}.csv".format(astock))
    df = pd.read_csv(path)
    values = df['Close'].tolist()
    targets[astock] = targetPrice(values)
setp(targets, "targets")
