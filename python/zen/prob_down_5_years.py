import z

dics = z.getp("stocks_bigdic")
stocks = dics.keys()
sdate = "2014-01-02"

dates = z.getp("dates")
lens = len(dates)
didx = dates.index(sdate)
ayear = 252
prob_down = dict()
problems = set()
for astock in stocks:
    above = 0
    total = 0
    for sdate in range(-1*(lens-didx),(-1*ayear)+1):
        edate = sdate + ayear - 1
        sday = dates[sdate]
        eday = dates[edate]

        try:
            first = dics[astock][sday]
        except:
            try:
                sday = dates[sdate-1]
                first = dics[astock][sday]
            except:
                problems.add(astock)
                continue
        try:
            second = dics[astock][eday]
        except:
            try:
                eday = dates[edate-1]
                second = dics[astock][eday]
            except:
                problems.add(astock)
                continue
        change = round(second/first,4)
        if change >= 1.04:
            above += 1
        total += 1
    try:
        prob_down[astock] = round(above/total,3)
    except:
        problems.add(astock)
        continue
print ("saving prob_down")
z.setp(prob_down, "prob_down")
#print("problems : {}".format( problems ))
print("problems : {}".format( len(problems) ))

