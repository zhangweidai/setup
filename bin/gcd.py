#!/usr/bin/python3
import sys
import subprocess
#exchanges = ["bittrex", "binance_us", "kucoin", "ftx_us", "kraken", "gemini" 

exchanges = ["ftx_us", "kucoin"]

import util
import json
from collections import defaultdict
markets = defaultdict(list)
def getdata():
    try:
        for exchange in exchanges:
            print("exchange : {}".format( exchange ))
#            cmd = 'curl -X GET "https://api.coingecko.com/api/v3/exchanges/{}" -H accept: application/json > {}.data'.format(exchange, exchange)
#            cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            data = json.load(open("{}.data".format(exchange)))
            markets[exchange] = set([ coin['base'] for coin in data['tickers']])

        util.savep("markets", markets)
        print("markets: {}".format( markets))
    
    except Exception as e:
        print (e)
        print ("wrong usage")
        pass

#getdata()
bar = util.loadp("markets")
print("bar : {}".format( bar ))
lines = list()
import os
print (os.getcwd())
dones = set()
for market1 in exchanges:
    for market2 in exchanges:
        if market1 == market2:
            continue
        dont_do = "{}|{}".format(market2, market1)
        if dont_do in dones:
            continue
        dont_do = "{}|{}".format(market2, market2)
        dones.add(dont_do)
        dont_do = "{}|{}".format(market1, market1)
        dones.add(dont_do)

        addme = " ".join(bar[market1] & bar[market2])
        lines.append("{}\n{}\n\n".format(dont_do, addme))

print("lines: {}".format( lines))
with open("common.txt", "w") as f:
    what = "\n".join(lines)
    print("what : {}".format( what ))
    f.write("\n".join(lines))

