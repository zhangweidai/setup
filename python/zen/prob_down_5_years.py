import z
import buy

# starting 2014 and looking at 1 year intervals, what's the probability you'd be up at least 3 percent
dates = z.getp("dates")
yearago = dates[-152]
print("yearago : {}".format( yearago ))

def getetfChanges():
    prices = list()
    for row in buy.getRows("IVV", yearago):
        prices.append(float(row[close]))
    last = prices[-1]
    changes = [ round(last / openp,3) for openp in prices[:-5] ]
    return round(sum(changes),3), len(changes)
#    return changes

close = z.closekey
def prob():
    global close, args

    bar, leng = getetfChanges()

    lens = len(dates)
    sdate = "2014-01-02"
    didx = dates.index(sdate)
    ayear = 252
    startTime = -1*(lens-didx)
    endTime = (-1*ayear)+1
    
    month3 = lens-int(3.8*(ayear/12)) 
    month3 = dates[month3]

    stocks = []
    try:
        if args.helpers:
            stocks = [args.helpers]
        else:
            stocks = z.getp("listofstocks")
    except:
        stocks = z.getp("listofstocks")

#    print("stocks : {}".format( len(stocks) ))
#    print("stocks : {}".format( stocks ))
    starting = "2014-01-02"
    sdate = "2014-01-02"
    
    prob_down = dict()
    problems = set()
    monDict = dict()
    ivvCompare = dict()

    for idx, astock in enumerate(stocks):

        if not idx % 100:
            print("idx: {}".format( idx))

#        print("starting: {}".format( starting))
        cdict = dict()
        started = False
        prices = list()
        try:
            for row in buy.getRows(astock, starting):
                cdate = row['Date']
                if cdate == yearago:
                    started = True

                cprice = float(row[close])
                if started:
                    prices.append(cprice)

                cdict[cdate] = cprice
                
        except Exception as e:
            continue

        try:
            last = prices[-1]
            changes = [ round(last / openp,3) for openp in prices[:-5] ]
            if len(changes) == leng:
                ivvCompare[astock] = round(sum(changes) / bar,3)
        except:
            pass
#        print("changes : {}".format( changes ))

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
                second = cdict[eday]
            except:
                try:
                    eday = dates[edate-1]
                    second = cdict[eday]
                except Exception as e:
                    if foundsomething:
                        problems.add(astock)
                    continue
    
            if eday == month3:
                month3Starting = True
    
            if month3Starting and second > month3High:
                month3High = second
    
            try:
                first = cdict[sday]
            except:
                try:
                    sday = dates[sdate-1]
                    first = cdict[sday]
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
    
    if len(stocks) > 1:
        print ("saving prob_down")
        z.setp(ivvCompare, "ivvCompare", printdata=True)
        z.setp(prob_down, "prob_down", printdata=True)
        z.setp(problems, "problems")
        z.setp(monDict, "monDict")
        print("prob_down_problems : {}".format( len(problems) ))

args = None    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('helpers', type=str, nargs='?', default = [])
    args = parser.parse_args()

    if args.helpers:
        args.helpers = args.helpers.upper()

    prob()
