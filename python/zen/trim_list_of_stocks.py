full=True

from rows import *
def proc(y1):
    if y1:
        tokens = y1.split(" ")
        neg = -1 if (y1[0] == "-") else 1
        numb = next(neg * float(obj[:-1]) for obj in tokens if obj[-1]=='%')
        return numb

import args
args.args.full = True
import z
z.getp.quick_list = False
import buy
import os
from sortedcontainers import SortedSet
import math

dates = z.getp("dates")
import delstock
import investpy
usa = "united states"

yearago = dates[-252]


#"KO" : { 'Stock Symbol': 'KO', 'Prev. Close': 176.45, 'Todays Range': '173.6 - 181.1', 'Revenue': 78810000000.0, 'Open': 175.68, '52 wk Range': '89.07 - 391', 'EPS': '- 6.05', 'Volume': 28548036.0, 'Market Cap': 8060000000.0, 'Div': '8.22 (8.65%)', 'Average Vol. (3m)': 45769388.0, 'P/E Ratio': None, 'Beta': 1.44, '1-Year Change': '- 50.08%', 'Shares Outstanding': 564325344.0, 'Next Earnings Date': '29/07/2020'}

print("stocks: {}".format( len(stocks)))
last_prices = z.getp("last_prices")

if __name__ == '__main__':

    trimme = list()
    potential_trim = list()
    savemeinfo2 = z.getp("savemeinfo2")
    mcdic2 = z.getp("mcdic2")
    saved = list()

    mcps = list()
    noinfos = list()
    for astock in stocks:
        infos = None
        info = savemeinfo2.get(astock, None)
        if info:
            price = info.get("Prev. Close", "- 99%")

            y1 = info.get("1-Year Change", "- 99%")
            vol = info.get("Average Vol. (3m)", 0)
            dicitems = mcdic2[astock]
            mcp = dicitems[0]
            revp = dicitems[1]
            div = dicitems[2]

            y1 = proc(y1)

            if (vol < 12000 and mcp < 40) or (y1 and y1 < -90.00) or (mcp < 15 and y1 < -65) or (price < 2):
                if div or (revp and revp > 50):
                    saved.append(astock)
                    continue


                infos = [astock, vol, mcp, y1]
                mcps.append((mcp, astock))
                trimme.append(astock)
        else:
            rank = buy.getMCRank(astock)
            if rank > 2000:

                if buy.getFrom("ports", astock) or buy.getFrom("orders", astock):
                    continue

                yearagoprice = None
                for i, row in enumerate(getRows(astock, yearago)):
                    if i == 0 and yearago == row['Date']:
                        yearagoprice = float(row['Close'])
                        break
                try:
                    latest = last_prices.get(astock)
                    y1 = round( latest / yearagoprice ,3)
                    if y1 < .25 or (latest < 2 and y1 < .65):
                        noinfos.append((astock,y1))
                        trimme.append(astock)
                except:
                    print("astock: {}".format( astock))


        if infos:
            potential_trim.append(infos)

    print("noinfos: {}".format( noinfos))
    print("noinfos: {}".format( len(noinfos)))

    print("mcps: {}".format( sorted(mcps)))
    print("potential_trim: {}".format( potential_trim))
    print("potential_trim: {}".format( len(potential_trim)))

    print("new stocks: {}".format( len(stocks)))
#    import delstock
#    delstock.batchdelete(trimme)
    print("trimme: {}".format( len(trimme)))

    print("saved: {}".format( saved))
#    z.setp(stocks, "listofstocks")


