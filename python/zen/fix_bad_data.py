import util
util.getStocks.totalOverride=True
stocks = util.getStocks()
problems = []
for astock in stocks:
    df = util.getCsv(astock)
    vals = []
    for idx in range(len(df)-1):
        start = df.at[idx,"Close"]
        end = df.at[idx+1,"Close"]
        change = start/end
        if change > 5:
            problems.append(astock)
            break
print("problems : {}".format( problems ))
