import z
from sortedcontainers import SortedSet
#def largemc(pair):
#    return pair[1] < 1110
#
#first, second = zip(*(filter(largemc, z.getp("latestmc").items())))
#z.setp(list(first), "mc2", True)
#
#def mc1(pair):
#    return pair[1] < 100
#first, second = zip(*(filter(mc1, z.getp("latestmc").items())))
#z.setp(list(first), "mc1", True)

import args
import current
import investpy
usa = "united states"
#stocks_list = investpy.stocks.get_stocks_list(country=usa)
#z.setp(stocks_list, "stocks_list", True)
#stocks_list = z.getp("stocks_list")
#problems = 0
#for astock in stocks_list:
#    print("astock : {}".format( astock ))
#    try:
#        savemeinfo[astock] = investpy.stocks.get_stock_information(astock, usa, as_json=True)
#    except Exception as e:
#        problems += 1
#        z.trace(e)
#        pass
#    if problems > 10:
#        break

#savemeinfo = z.getp("savemeinfo2")
#first, second = zip(*(
bar = dict()
billion = 1000000000
million = 1000000

#bar["man"] = {"name": "man", "mc" : 0.3 * billion}
#bar["foo"] = {"name": "foo", "mc" : 10 * billion}
bar = { 
"BA" : { 'Stock Symbol': 'BA', 'Prev. Close': 176.45, 'Todays Range': '173.6 - 181.1', 'Revenue': 78810000000.0, 'Open': 175.68, '52 wk Range': '89.07 - 391', 'EPS': '- 6.05', 'Volume': 28548036.0, 'Market Cap': 8160000000.0, 'Div': '8.22 (8.65%)', 'Average Vol. (3m)': 45769388.0, 'P/E Ratio': None, 'Beta': 1.44, '1-Year Change': '- 50.08%', 'Shares Outstanding': 564325344.0, 'Next Earnings Date': '29/07/2020'},
"AMD" : { 'Stock Symbol': 'AMD', 'Prev. Close': 176.45, 'Todays Range': '173.6 - 181.1', 'Revenue': 7881000000.0, 'Open': 175.68, '52 wk Range': '89.07 - 391', 'EPS': '- 6.05', 'Volume': 28548036.0, 'Market Cap': 12060000000.0, 'Div': '8.22 (8.65%)', 'Average Vol. (3m)': 45769388.0, 'P/E Ratio': None, 'Beta': 1.44, '1-Year Change': '- 50.08%', 'Shares Outstanding': 564325344.0, 'Next Earnings Date': '29/07/2020'},
KO" : { 'Stock Symbol': 'KO', 'Prev. Close': 176.45, 'Todays Range': '173.6 - 181.1', 'Revenue': 78810000000.0, 'Open': 175.68, '52 wk Range': '89.07 - 391', 'EPS': '- 6.05', 'Volume': 28548036.0, 'Market Cap': 8060000000.0, 'Div': '8.22 (8.65%)', 'Average Vol. (3m)': 45769388.0, 'P/E Ratio': None, 'Beta': 1.44, '1-Year Change': '- 50.08%', 'Shares Outstanding': 564325344.0, 'Next Earnings Date': '29/07/2020'}
} 

sorted_mc = SortedSet()

def rev(bar):
    return bar / million

def calcDiv(bar, last):
    try:
        return round(float(bar.split(" ")[0]) / last,3)
    except:
        return None

import buy
#rankOn = [("Revenue", rev), ("Div", div)]
mcs = list()
revmcs = list()
mcmap = dict()
for pair in bar.values():
    astock = pair["Stock Symbol"]
    mc = pair["Market Cap"]/billion

    mcs.append(mc)

    revmc = round(((pair["Revenue"] / million) / mc),3)
    revmcs.append(revmc)
    div = calcDiv(pair["Div"], pair["Prev. Close"])

    mcmap[astock] = mc, div, revmc

#print("stocks: {}".format( len(stocks)))
#print("mcs : {}".format( mcs ))
#
#for astock, items in mcmap.items():
#    mc, div, revmc = items[0], items[1], items[2]
#    print("revmc : {}".format( revmc ))
#    print("mc : {}".format( mc ))
#    print("astock: {}".format( astock))
#
#exit()
#for pair in stocks:
for astock, items in mcmap.items():

    mc, div, revmc = items[0], items[1], items[2]
    mymap = dict()
    mcp = current.percentile(mcs, flip = True, considerate = mc)
    revmcp = current.percentile(revmcs, flip = False, considerate = revmc)

    mymap["mcp"] = mcp
    mymap["revmcp"] = revmcp
    md, md1, md2, mg, gddif, chg1, chg1p, chg30, chg30p, chg5, wc1, target, c_close =  current.proc(astock, store = False)
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
    mymap["wc1"] = wc1
    mymap["target"] = target
    mymap["c_close"] = c_close

    print("mymap: {}".format( mymap))
    z.setpp(mymap, astock)

z.savepp()

buy.sortedSetToRankDict("latest_mc_dict", sorted_mc, reverse=True, printdata = True)


#import args
#print("stocks: {}".format( stocks))
