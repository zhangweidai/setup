import pandas as pd
from util import targetPrice, setp, getStocks

targets = dict()
for astock in getStocks():
    targets[astock] = targetPrice(getTestItems(simple=True))
setp(targets, "targets")
