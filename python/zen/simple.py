
#import gbuy_old
import z
import statistics
z.showSaved = False
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

#sdate = '2020-01-01-00-00'
sdate = '01-01-2020'
sdate = 1577865600
edate = 1615955902

#data = cg.get_coins_markets(vs_currency="usd")
coindata = z.getp("coins") 
#print("data : {}".format( data ))
#exit()
import numpy as np
from Historic_Crypto import HistoricalData
from sortedcontainers import SortedSet
from collections import defaultdict
if __name__ == '__main__':
    ret = SortedSet()
    rettotals = SortedSet()
    avgdrops = SortedSet()
    r3 = SortedSet()
    largest_one_day = dict()
    alldata = defaultdict(SortedSet)
    for astock in coindata:
        if astock['market_cap_rank'] > 60:
            continue
        name = astock['id']
        data = z.getp(name) 
        if data is None:
            data = cg.get_coin_market_chart_range_by_id(name, "usd", sdate, edate)
            z.setp(data, name) 

        last = None
        total = 0

        changes = list()
        prices = list()
        drops = list()
        print (data.keys())
        for caps in data['market_caps']:
            alldata[caps[0]].add((caps[1], name))

        for adata in data['prices']:
            try:
                cprice = adata[1]
                prices.append(cprice)
                change = round(cprice / last,4) 
                if change < 1:
                    drops.append(change)
                total += change
                changes.append(change)
            except:
                pass
            last = adata[1]

        mean = statistics.mean(prices)
        mean = round(last / mean,3)
        largest_one_day[name] = round(1-min(drops) ,2) * 100

        averagedrop = statistics.mean(drops)
        r3.add((mean, name))
        std = np.std(changes)
        ret.add((std, name))
        rettotals.add((total, name))
        avgdrops.add((averagedrop, name))
    
    print("\nchange from mean: {}".format( r3))
    print("\nadded changes: {}".format( rettotals))
    print("\nstd: {}".format( ret))
    print("\navgdrops: {}".format( avgdrops))
    print("largest_one_day: {}".format( largest_one_day))
#        data = z.getp(namep)
#        if data is None:
#        data = HistoricalData(namep, 86400, sdate).retrieve_data()
