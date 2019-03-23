import util
util.getCsv.csvdir = "historical"
df = util.getCsv("W")

total = 0
consecdrop = 0
dropped = False
dropstreak = 0
maxdrop = 0
streaks = []
percentdown = 0.065
compar = 1-percentdown
for idx,row in df.iterrows():
    drop = row["Close"] / row["Open"]
    if dropped:
        if drop < 1:
            consecdrop += 1
            dropstreak += 1
        else:
            dropped = False
            if dropstreak > maxdrop:
                maxdrop = dropstreak
            streaks.append(dropstreak)
            dropstreak = 0

        total+=1
    if drop < compar:
        dropstreak += 1
        dropped = True
print("consecdrop: {}".format(consecdrop))
print("total: {}".format(total))
print("perc: {}".format(consecdrop/total))
print("maxdrop : {}".format( maxdrop ))
print("average : {}".format( sum(streaks)/len(streaks) ))
