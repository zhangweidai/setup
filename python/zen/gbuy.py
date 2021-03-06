debug = None
import z
import args
import os
import numpy
import buy
import one_year_moving_average

mcmap = z.getp("mcdic2")
import prob_up_1_year

revmcs = list()

billion = 1000000000
million = 1000000
year = 2021

mcdata = z.getp("mcdata")
def saveQuick():
    z.getp.cache_clear()

    portFolioValue= z.getp("ports")

    z.setp(portFolioValue, "quick")

    return
#    quick = z.getp("savePs")

    print("quick : {}".format( len(quick )))
    quick = [ stock[1] for stock in quick ]

    print("quick : {}".format( len(quick )))
    quick += list(portFolioValue.keys())

    print("quick : {}".format( len(quick )))
    orders = z.getp("orders")
    quick += list(orders)
    print("quick : {}".format( len(quick )))

    quick += z.getp("top95")

    print("quick : {}".format( len(quick )))
    quick = list(set(quick))

    print("quick : {}".format( len(quick )))
    try:
        quick.remove("TMUSR")
    except:
        pass

    z.setp(quick, "quick")

    if len(quick) > 600:
        print ("TOO MANY in QUICK")

#mcs = z.getp("mcs")
#if not mcs:
#    savemeinfo = z.getp("savemeinfo2")
#    for pair in savemeinfo.values():
#        try:
#            mc = pair["Market Cap"]/billion
#            mcs.append(mc)
#        except:
#            pass

divdict = z.getp("mcdivdict")
problems = set()

def updateStocks():
    global problems
    import datetime
    import math
    import csv

    already_updated = 0
    try:
        now = datetime.datetime.now()
        consecutive_misses = 0

        cdate_missing = list()
        current_cday = None
        added = False
        for astock in stocks:
            apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
            if not os.path.exists(apath):
                import regen_stock
                regen_stock.process(astock)
                continue

            try:
                csvdate = datetime.datetime.fromtimestamp(os.path.getmtime(apath))
                csvday = csvdate.day
                csvmonth = csvdate.month
                ttoday = datetime.date.today().day
                tmonth = datetime.date.today().month

                if csvday >= ttoday and tmonth == csvmonth:
                    consecutive_misses = 0
                    already_updated += 1
                    continue

#                    readFile = open(apath)
#                    lines = readFile.readlines()
#                    readFile.close()
#                    if lines[-1].split(",")[0] == lines[-2].split(",")[0]:
#                        w = open(apath,'w')
#                        w.writelines([item for item in lines[:-1]])
#                        w.close()
            except Exception as e:
                problems.add(astock)
                z.trace(e)
                exit()
                continue

            for row in csv.DictReader(open(apath)):
                pass

            try:
                date = row['Date']
                cclose = row['Adj Close']
            except:
                continue

            import gbuy_old

#            if date == "2020-08-28":
#                already_updated += 1
#                continue

            df = gbuy_old.getDataFromYahoo(astock, date)
            if df is None:
                print("problem downloading: {}".format( astock))
                consecutive_misses += 1
                if consecutive_misses > 5:
                    problems.add(astock)
                    print("got 5 problems already problems : {}".format( problems ))
                    z.setp(problems, "problems")
                    exit()
                continue
            consecutive_misses = 0

            with open(apath, "a") as f:
                first = True
                for idx in df.index:
                    if first:
                        first = False
                        continue
                    cdate = str(idx.to_pydatetime()).split(" ")[0]

                    if date == cdate:
                        continue

                    try:
                        opend = round(df.at[idx, "Open"],3)
                        high = round(df.at[idx, "High"],3)
                        low = round(df.at[idx, "Low"],3)
                        closed = round(df.at[idx, "Close"],3)
                        adj = round(df.at[idx, "Adj Close"],3)
                        vol = df.at[idx, "Volume"]
                    except:
                        opend = round(df.at[idx, "Open"][0],3)
                        high = round(df.at[idx, "High"][0],3)
                        low = round(df.at[idx, "Low"][0],3)
                        closed = round(df.at[idx, "Close"][0],3)
                        adj = round(df.at[idx, "Adj Close"][0],3)
                        vol = df.at[idx, "Volume"][0]

                    try:
                        chg = round(adj/cclose,3)
                    except:
                        chg = 1

                    if not math.isnan(opend):
                        cclose = adj
                        added = True
                        f.write("{},{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol, chg))

            if not added:
                problems.add(astock)
                print ("problem with {}".format(astock))

    except Exception as e:
        print ("problem with gbuy_old")
        z.trace(e)
        print("problems: {}".format( problems))
        exit()

    print("already_updated : {}".format( already_updated ))

buy.setPartial("w30", 0.5)
buy.setPartial("chg30", 0.5)
buy.setPartial("l2y", 0.7)
buy.setPartial("md", 0.7)
buy.setPartial("avg", 1.1)

def doit():
    global stocks
    final_dic = dict()

    last_price = z.getp("last_price")
    if type(last_price) is not dict:
        last_price = dict()

    buy.updateDates()

    if not args.args.noupdate:
        updateStocks()

        if problems:
            import readchar
            print("problems: c/d ? {} {}".format( problems, len(problems)))
            key = readchar.readkey()
            if key == "d":
                import delstock
                delstock.batchdelete(problems)
                z.getp.cache_clear()
                stocks = z.getp("listofstocks")
                print("stocks : {}".format( len(stocks) ))
                print("continue y/n")
                key = readchar.readkey()
                if key == "n":
                    exit()
            if key != "c":
                exit()
            if key == "x":
                exit()

    if args.args.full:
        print ("generating volp")
        import volume_change
        volp = volume_change.proc(stocks)
    else:
        volp = z.getp("volp")

    import current
    last_price = dict()#z.getp("last_price")
    for idx, astock in enumerate(stocks):
        if not idx % 100:
            print("astock : idx {} {}".format( idx, astock ))

        try:
            items = mcmap[astock]
            mcp, revmcp, div = items[0], items[1], items[2]
        except:
            try:
                bar = divdict[astock]
                cap = bar[1]
                div = bar[0]
                revmcp = None
#                mcp = current.percentile(mcs, flip = True, considerate = cap)
            except:
                pass
    
        mymap = dict()
    
        args.args.bta = False

#        myvolp = volp.get(astock, 0)

#        print("mcdata : {}".format( mcdata.keys() ))
#        exit()
#    mcdata : Index(['language', 'region', 'quoteType', 'triggerable', 'quoteSourceName',
#       'currency', 'shortName', 'regularMarketPrice', 'regularMarketTime',
#       'regularMarketChange', 'regularMarketOpen', 'regularMarketDayHigh',
#       'regularMarketDayLow', 'regularMarketVolume', 'exchange', 'market',
#       'postMarketChangePercent', 'postMarketTime', 'postMarketPrice',
#       'postMarketChange', 'regularMarketChangePercent',
#       'regularMarketDayRange', 'regularMarketPreviousClose', 'bid', 'ask',
#       'bidSize', 'askSize', 'messageBoardId', 'fullExchangeName', 'longName',
#       'financialCurrency', 'averageDailyVolume3Month',
#       'averageDailyVolume10Day', 'fiftyTwoWeekLowChange',
#       'fiftyTwoWeekLowChangePercent', 'fiftyTwoWeekRange',
#       'fiftyTwoWeekHighChange', 'fiftyTwoWeekHighChangePercent',
#       'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'earningsTimestamp',
#       'earningsTimestampStart', 'earningsTimestampEnd', 'trailingPE',
#       'epsTrailingTwelveMonths', 'epsForward', 'epsCurrentYear',
#       'priceEpsCurrentYear', 'sharesOutstanding', 'bookValue',
#       'fiftyDayAverage', 'fiftyDayAverageChange',
#       'fiftyDayAverageChangePercent', 'twoHundredDayAverage',
#       'twoHundredDayAverageChange', 'twoHundredDayAverageChangePercent',
#       'marketCap', 'forwardPE', 'priceToBook', 'sourceInterval',
#       'exchangeTimezoneName', 'exchangeTimezoneShortName',
#       'gmtOffSetMilliseconds', 'priceHint', 'marketState',
#       'exchangeDataDelayedBy', 'esgPopulated', 'tradeable', 'price',
#       'firstTradeDateMilliseconds', 'trailingAnnualDividendRate',
#       'trailingAnnualDividendYield', 'dividendDate', 'displayName',
#       'ipoExpectedDate', 'ytdReturn', 'trailingThreeMonthReturns',
#       'trailingThreeMonthNavReturns'],
        div = mcdata['trailingAnnualDividendRate'].get(astock, 0)
#        print("{} div : {}".format( astock div ))

        try:
            md, md1, md2, mg, gddif, chg1, chg1p, chg30, chg30p, chg5, wc1, target, c_close, m30c, w30, dl =  current.proc(astock, store = False)
            y1u, ivvb, wc, bc, avg, ly, l2y, avg8, dfh1y, gfl1y = prob_up_1_year.proc(astock)
            ma, mav = buy.getFrom("mas", astock)
        except Exception as e:
            print("PROBLEM astock: {}".format( astock))
            import traceback
            traceback.print_exc()
            exit()
            continue

        try:
            ma1y, ma1yv, ma1c = one_year_moving_average.proc(astock)
#            ma1y, ma1yv, ma1c = buy.getFrom("avgs", astock)
        except Exception as e:
            ma1y, ma1yv, ma1c = "NA", "NA", "NA"

        if debug:
            print (y1u, ivvb, wc, bc, avg, ly, l2y, avg8, dfh1y, gfl1y)
            print (md, md1, md2, mg, gddif, chg1, chg1p, chg30, chg30p, chg5, wc1, target, c_close, m30c, w30, dl)
    
        if args.args.full:
            buy.addPDic(astock, "md", round((md + md1 + md2)/3,3))
            buy.addPDic(astock, "wc", wc)
            buy.addPDic(astock, "m30c", m30c)
            buy.addPDic(astock, "w30", w30)
            buy.addPDic(astock, "chg30", chg30)
            buy.addPDic(astock, "ly", ly)
            buy.addPDic(astock, "l2y", l2y)
            buy.addPDic(astock, "ivvb", ivvb)
            buy.addPDic(astock, "avg", avg)
            buy.addPDic(astock, "gddif", gddif)

            divscore = div * 65 if div else 0
            buy.addPDicRaw(astock, divscore)

            try:
                y1u_score = round(30  * y1u,3)
            except:
                y1u_score = 0
                
            buy.addPDicRaw(astock, y1u_score)

        if numpy.isnan(div):
            div = 0
        mymap["div"] = round(div,3) if div else 0
        mymap["md"] = md
        mymap["md1"] = md1
        mymap["md2"] = md2
        mymap["mg"] = mg
        mymap["gddif"] = gddif
        mymap["chg1"] = chg1
        mymap["chg1p"] = chg1p
        mymap["chg30"] = chg30
        mymap["chg30p"] = chg30p
        mymap["chg5"] = chg5
        mymap["target"] = target
        mymap["last"] = c_close
        mymap["y1u"] = y1u
        mymap["dl"] = dl
        mymap["ivvb"] = ivvb
        mymap["wc"] = wc
        mymap["bc"] = bc
        mymap["avg"] = avg
        mymap["ly"] = ly
        mymap["l2y"] = l2y
        mymap["avg8"] = avg8
        mymap["m30c"] = m30c
        mymap["w30"] = w30
        mymap["dfh1y"] = dfh1y
        mymap["gfl1y"] = gfl1y
        mymap['ma1y']  = ma1y
        mymap['ma1yv' ] = ma1yv
        mymap['ma1c'] = ma1c
        final_dic[astock] = mymap
        last_price[astock] = c_close
    
    if args.args.full:
        buy.savePs()
    saveQuick()

    z.setp(last_price, "last_price")

    for astock, valmap in final_dic.items():
        valmap['bta'] = buy.getFrom("savePsdic", astock)
        z.setpp(valmap, astock)

    z.savepp()
    print("stocks: {}".format( len(stocks)))

if __name__ == '__main__':
    if args.args.noupdate:
        coindata = z.getp("coins") 
        stocks = stocks + [ data['symbol'].upper() for data in coindata if data['market_cap_rank'] <= 60 ]
        print("stocks : {}".format( stocks ))
    doit()
