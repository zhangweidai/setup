import z
stocks = z.getStocks()
problems = []
for astock in stocks:
    df = z.getCsv(astock)
    if df is None:
        problems.append(astock)
        continue
    vals = []
    for idx in range(len(df)-1):
        start = df.at[idx,"Close"]
        end = df.at[idx+1,"Close"]
        change = start/end
        if change > 5 or change < 0.15:
            problems.append(astock)
            break
print("problems : {}".format( problems ))
print("problems : {}".format( len(problems)))
