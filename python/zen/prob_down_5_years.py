import z
def prob():
    dates = z.getp("dates")
    lens = len(dates)
    sdate = "2014-01-02"
    didx = dates.index(sdate)
    ayear = 252
    startTime = -1*(lens-didx)
    endTime = (-1*ayear)+1
    
    month3 = lens-int(3.8*(ayear/12)) 
    month3 = dates[month3]
    
    dics = z.getp("stocks_bigdic")
    stocks = dics.keys()
    sdate = "2014-01-02"
    
    prob_down = dict()
    problems = set()
    monDict = dict()
    for astock in stocks:
        above = 0
        total = 0
        month3Starting = False
        month3High = 0
        foundsomething = False
        for sdate in range(-1*(lens-didx),(-1*ayear)+1):
            edate = sdate + ayear - 1
            sday = dates[sdate]
            eday = dates[edate]
    
            try:
                second = dics[astock][eday]
            except:
                try:
                    eday = dates[edate-1]
                    second = dics[astock][eday]
                except Exception as e:
                    if foundsomething:
                        problems.add(astock)
                    continue
    
            if eday == month3:
                month3Starting = True
    
            if month3Starting and second > month3High:
                month3High = second
    
            try:
                first = dics[astock][sday]
            except:
                try:
                    sday = dates[sdate-1]
                    first = dics[astock][sday]
                    foundsomething = True
                except Exception as e:
                    continue
    
            change = round(second/first,4)
            if change >= 1.03:
                above += 1
            total += 1
    
        monDict[astock] = month3High
        try:
            prob_down[astock] = round(above/total,3)
        except:
            problems.add(astock)
            continue
    
    print ("saving prob_down")
    z.setp(prob_down, "prob_down")
    z.setp(problems, "problems")
    z.setp(monDict, "monDict")
    print("prob_down_problems : {}".format( len(problems) ))
    
