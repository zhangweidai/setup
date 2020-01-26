import z
import buy

# starting 2014 and looking at 1 year intervals, what's the probability you'd be up at least 3 percent
dates = z.getp("dates")
yearago = dates[-161]
#print("yearago : {}".format( yearago ))
excludeDays = -5
def getetfChanges():
    prices_for_a_year = list()
    for row in buy.getRows("IVV", yearago):
        prices_for_a_year.append(float(row[close]))
    last = prices_for_a_year[-1]
    changes = [ round(last / openp,3) for openp in prices_for_a_year[:excludeDays] ]
    return round(sum(changes),3), len(changes), changes
#    return changes

close = z.closekey
def prob():
    global close, args

    bar, leng, ivvchanges = getetfChanges()

    lens = len(dates)
    sdate = "2014-01-02"
    starting = "2014-01-02"

    didx = dates.index(sdate)
    ayear = 252
    startTime = -1*(lens-didx)
    endTime = (-1*ayear)+1
    
    month3 = lens-int(3.8*(ayear/12)) 
    month3 = dates[month3]

    stocks = []
    if not stocks:
        try:
            if args.helpers:
                stocks = [args.helpers]
            else:
                stocks = z.getp("listofstocks")
        except:
            stocks = z.getp("listofstocks")
    
#    print("stocks : {}".format( len(stocks) ))
#    print("stocks : {}".format( stocks ))
    
    prob_down = dict()
    problems = list()
    ivvCompare = dict()
    ivvDaily = dict()

    for idx, astock in enumerate(stocks):

        if not idx % 100:
            print("idx: {}".format( idx))

#        print("starting: {}".format( starting))
        started = False
        prices_for_a_year = list()
        all_prices = list()
        idx = 0
        ups = list()
        try:
            for row in buy.getRows(astock, starting):
                cdate = row['Date']
                if cdate == yearago:
                    started = True

                cprice = float(row[close])
                if started:
                    prices_for_a_year.append(cprice)
                all_prices.append(cprice)

                if len(all_prices) > 252:
                    early = all_prices[idx]
                    idx += 1
                    ups.append(1 if cprice > early else 0)
                
        except Exception as e:
            print("exception 0 astock: {}".format( astock))
            problems.append(astock)
            continue

        try:
            last = prices_for_a_year[-1]
#            changes = [ round(last / aprice,3) for aprice in prices_for_a_year[:excludeDays] ]
            changes = list()
            ivvur = list()
            
            for i, aprice in enumerate(prices_for_a_year[:excludeDays]):
                cc = round(last / aprice,3) 
                changes.append(cc)
                civvchange = ivvchanges[i]
                ivvur.append(1 if cc >= civvchange else 0)
                
            if len(changes) == leng:
                ivvCompare[astock] = round(sum(changes) / bar,3)
                ivvDaily[astock] = round(sum(ivvur) / leng, 3)

        except:
            print("exception 1 astock: {}".format( astock))
            pass

        if len(ups) > 100:
            prob_down[astock] = round(sum(ups)/len(ups),3)
#        print("changes : {}".format( changes ))

        above = 0
        total = 0
        month3Starting = False
        month3High = 0
        foundsomething = False
    
    if len(stocks) > 1:
        print ("saving prob_down")
        z.setp(ivvCompare, "ivvCompare", printdata = True)
        z.setp(prob_down, "prob_down", printdata = True)
        z.setp(ivvDaily, "ivvDaily", printdata = True)
    else:
        print("ivvCompare: {}".format( ivvCompare))
        print("prob_down: {}".format( prob_down))
        print("ivvDaily: {}".format( ivvDaily))
    print("problems: {}".format( problems))
#        z.setp(problems, "problems")
#        print("prob_down_problems : {}".format( len(problems) ))

args = None    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('helpers', type=str, nargs='?', default = [])
    args = parser.parse_args()

    if args.helpers:
        args.helpers = args.helpers.upper()

    prob()
