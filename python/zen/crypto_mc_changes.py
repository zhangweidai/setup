
#import gbuy_old
import z
import statistics
import datetime
from scipy import stats
z.showSaved = False
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

#sdate = '2020-01-01-00-00'
sdate = '01-01-2020'
sdate = 1577865600
sdate = 1546300800
import time
edate = int(time.time())

#data = cg.get_coins_markets(vs_currency="usd")
coindata = z.getp("coins") 
#print("data : {}".format( data ))
#exit()
import numpy as np
from Historic_Crypto import HistoricalData
from sortedcontainers import SortedSet
from collections import defaultdict
regen = False
if __name__ == '__main__':
    ret = SortedSet()
    rettotals = SortedSet()
    avgdrops = SortedSet()
    r3 = SortedSet()
    largest_one_day = dict()
    alldata = defaultdict(list)
    for astock in coindata:
        
        if astock['market_cap_rank'] > 60:
            continue


        name = astock['id']
        if "-btc" in name:
            continue
        if "-usd" in name:
            continue

        if "usd-c" not in name and name != "tether":
            continue
        print("name: {}".format( name))

        try:
            if regen:
                data = cg.get_coin_market_chart_range_by_id(name, "usd", sdate, edate)
                z.setp(data, name) 

            else:
                data = z.getp(name) 
                if data is None or regen:
                    data = cg.get_coin_market_chart_range_by_id(name, "usd", sdate, edate)
                    z.setp(data, name) 
        except:
            print("name: {}".format( name))
            pass


        last = None
        total = 0

        changes = list()
        prices = list()
        drops = list()
        print (data.keys())
        last = 0
        counts = list()
        for caps in enumerate(data['market_caps']):
            try:
                counts.append(caps[1][1] / last)
            except:
                pass
            last = caps[1][1]
        print("counts: {}".format( len(counts)))
        print("counts: {}".format( statistics.mean(counts)))
#        exit()

        for i, caps in enumerate(data['prices']):
            cvalue = caps[1]
            if cvalue:
                alldata[name].append(cvalue)

    alls = defaultdict(list)
    lastprices = dict()
    for pair in alldata.items():
        name = pair[0]
        values = pair[1]
        for i, price in enumerate(values):
            try:
                change = round(values[i+5]/price,4)
                alls[name].append(change)
            except:
                pass
        lastprices[name] = price

    ret = dict()
    for name, values in alls.items():
        ret[name] = (round(stats.percentileofscore(values, values[-1]),2), values[-1])

#    for name, percents in ret.items():
#        percentsr = percents[0]
#        if percentsr > 90 or percentsr < 10:
#            print("{} : {}".format( name, percents ))
#    print("alls: {}".format( alls))
#        print("price : {}".format( price ))
#        print("values : {}".format( values ))
#        exit()

#        for adata in data['prices']:
#            try:
#                cprice = adata[1]
#                prices.append(cprice)
#                change = round(cprice / last,4) 
#                if change < 1:
#                    drops.append(change)
#                total += change
#                changes.append(change)
#            except:
#                pass
#            last = adata[1]
#
#        mean = statistics.mean(prices)
#        mean = round(last / mean,3)
#        largest_one_day[name] = round(1-min(drops) ,2) * 100
#
#        averagedrop = statistics.mean(drops)
#        r3.add((mean, name))
#        std = np.std(changes)
#        ret.add((std, name))
#        rettotals.add((total, name))
#        avgdrops.add((averagedrop, name))
    
#    print("\nchange from mean: {}".format( r3))
#    print("\nadded changes: {}".format( rettotals))
#    print("\nstd: {}".format( ret))
#    print("\navgdrops: {}".format( avgdrops))
#    print("largest_one_day: {}".format( largest_one_day))
#        data = z.getp(namep)
#        if data is None:
#        data = HistoricalData(namep, 86400, sdate).retrieve_data()
