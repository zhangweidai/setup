import pandas as pd
from util import getTestItems, targetPrice, getPath

def dipScore(items):
    SIZE = 100
    currentStack = deque([])
    low = deque([])
    dips = []
    for i,price in enumerate(items):
        currentStack.append(price)
        if len(currentStack) == SIZE:
            start = (max(list(currentStack)[:3]))
            end = (min(list(currentStack)[-3:]))
            tdip = (end/start)
            if tdip < 1:
                dips.append(1-tdip)
            currentStack.popleft()
    return round(sum(dips),6)

path = getPath("csv/GOOG.csv")
df = pd.read_csv(path)
print (df)
df = df[:-100]
print (df)
#print (targetPrice(getTestItems(simple=True)))
