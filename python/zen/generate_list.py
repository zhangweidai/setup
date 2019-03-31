import z 
import operator
from random import sample

def getScore(idxstart, df):
    minid = 10
    realstart = idxstart-15
    dips = 0 
    gains = 0 
    for idx in range(realstart, idxstart):
        bought = df.at[idx,"Close"]
        now = df.at[idx+1,"Close"]
        change = now/bought
        if change < 1:
            dips += 1-change
        else:
            gains += change

    bought = df.at[realstart,"Close"]
    now = df.at[idxstart,"Close"]
    change = now/bought
    s1 = -1
    if change > 1 and dips:
        s1 = ((change-1)*100)/dips

    bought = df.at[idxstart-4,"Close"]
    now = df.at[idxstart-2,"Close"]
    change = now/bought

    s2 = -1
    if change < 1:
        s2 = round((1-change)*gains,3)

    return s1,s2

#    return round(dips+change,3)
#    return round(dips+change,3)

def getBuyStocks(idxdate, mode, howmany = 2):
    thedayl=dict()
    thedayll=dict()
    thedays1=dict()
    thedays2=dict()
    for astock in getBuyStocks.stocks:
        df = z.getCsv(astock)
        if df is None:
            print("problem astock: {}".format( astock))
            continue

        df_dates = df["Date"].tolist() 
        try:
            starti = df_dates.index(idxdate)
            if not starti:
                continue
        except Exception as e:
#            print ('port: '+ str(e))
#            print("astock: {}".format( astock))
            continue

        try:
            close = df.at[starti,"Close"]
            if close < 2:
                continue
        except Exception as e:
            print ('port: '+ str(e))
            print("idxdate: {}".format( idxdate))
            print("starti: {}".format( starti))
            print("df: {}".format(len( df)))
            print("df_dates: {}".format(len( df_dates)))
            exit()

        try:
            opened = df.at[starti-3,"Open"]
            changel = round((close/opened) - (close/df.at[starti-8,"Open"])/2,3)
            changell = round(close/opened,3)
            s1,s2 = getScore(starti, df)
        except Exception as e:
            continue

#        if changeh > 1:
#            thedayh[astock] = round(changeh,4)
        if changel < 1:
            thedayl[astock] = round(changel,4)
        if changell < 1:
            thedayll[astock] = round(changell,4)

        thedays1[astock] = s1
        thedays2[astock] = s2

    sorted_xl = sorted(thedayl.items(), key=operator.itemgetter(1))
    sorted_xll = sorted(thedayll.items(), key=operator.itemgetter(1))

    sorted_xs1 = sorted(thedays1.items(), key=operator.itemgetter(1))
    sorted_xs2 = sorted(thedays2.items(), key=operator.itemgetter(1))

    try:
#        if mode == "high":
#            return sample(sorted_xh[-6:],2)
        if mode == "special1":
            return sample(sorted_xs1[-15:],howmany)
        elif mode == "special2":
            return sample(sorted_xs2[-15:],howmany)
        elif mode == "low":
            return sample(sorted_xl[:15],howmany)
        elif mode == "lowlow":
            return sample(sorted_xll[:15],howmany)
    except Exception as e:
        print ('port: '+ str(e))
        print("mode : {}".format( mode ))
        print("idxdate: {}".format( idxdate))
        return []

    print ("shoudlntget here")
    raise SystemExit
getBuyStocks.stocks = []


if __name__ == '__main__':
    import matplotlib.pyplot as plt
#    dates = z.getp("dates")
#    num_days = len(dates)
#    print("num_days : {}".format( num_days ))
    etfsource = "IUSG"
    getBuyStocks.stocks = z.getStocks(etfsource)
#    print(getBuyStocks("2019-03-27", mode="lowlow"))
#    print(getBuyStocks("2019-03-28", mode="special1", howmany=4))
    print(getBuyStocks("2019-03-28", mode="special2", howmany=4))
    print(getBuyStocks("2019-03-28", mode="lowlow", howmany=4))
#    print(getBuyStocks("2019-03-27", mode="special2", howmany=4))

