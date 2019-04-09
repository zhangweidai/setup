import threading
from queue import Queue
import z
import worst_duration
import random
import sell_threader
import zen
import dask_help
from collections import defaultdict
import matplotlib.pyplot as plt

sell_threader.setTranscript.enabled = False
sell_threader.buySellSim.tracks = 30
#dask_help.getModes.override = ["Volume"]

z.getStocks.devoverride = "ITOT"
zen.getSortedStocks.get = "low"

use_q = True
testpoints = 140
print("testpoints : {}".format( testpoints ))
years = 2

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        sell_threader.buySellSim(q.get())
        q.task_done()

dates = z.getp("dates")
num_days = len(dates)

ayear = 252
duration = int (years * ayear)

starti = num_days-(duration*4)
endi = num_days-duration
startd = dates[starti]
print("startd : {}".format( startd ))
endd = dates[endi]
print("endd : {}".format( endd ))

prices_only = False
if zen.getSortedStocks.get == "price":
    prices_only = True

zen.setSortedDict()

q = Queue()
for x in range(7):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

print("num_days : {} - {} {}".format( num_days, startd, endd ))
played = 0
def calcPortfolio(droppage, mode, price, typed = None):
    global played
    for tries in range(testpoints):
        start = random.randrange(starti, endi)
        end = start + duration
        played += 1
        if use_q:
            q.put([droppage, start, end, mode, price, typed])
        else:
            sell_threader.buySellSim([droppage, start, end, 
                    mode, price, typed])

def getColors():
    return ["blue", "red", "green", "black", 'cyan', 'brown', 
            'orange', 'pink', 'magenta', 'olive', "indigo", "teal", "silver"]

ylist = [i/100 for i in range(60,90,5)]
numy = len(ylist)
price = -1
pricelist = [price]
if zen.getSortedStocks.get == "price":
    pricelist = [i for i in range(4)]

    for droppage in ylist:
        for price in pricelist:
            calcPortfolio(droppage, mode="Change", price=price)

else:
    for droppage in ylist:
        for typed in ["low", "high", "both"]:
            for mode in dask_help.getModes():
                calcPortfolio(droppage, mode=mode, price=price, typed=typed)
q.join()

collector = sell_threader.getCollector()
avgdropdict = defaultdict(list)
avgmodedict = defaultdict(list)
avgpricedict = defaultdict(list)

mode = "Change"
if zen.getSortedStocks.get == "price":
    for i,price in enumerate(pricelist):
        for droppage in ylist:
            color = getColors()[i]
            tupp = (droppage, mode, price)
            try:
                value = z.avg(collector[tupp])
            except:
                print("tupp : {}".format( tupp ))
                continue
        
            avgdropdict[droppage].append(value)
            avgmodedict[mode].append(value)
            avgpricedict[price].append(value)
        
            try:
                plt.scatter(droppage, value, color=color)
            except:
                pass
else:
    for droppage in ylist:
        for typed in ["low", "high", "both"]:
            zen.getSortedStocks.get = typed
            for mode in dask_help.getModes():
                modeidx = dask_help.getModes().index(mode)
                color = getColors()[modeidx]
                modestr = "{}/{}".format(mode, typed)
                tupp = (droppage, modestr, price)
                try:
                    value = z.avg(collector[tupp])
                except Exception as e:
                    print("1tupp : {}".format( tupp ))
                    z.trace(e)
                    raise SystemExit
                    continue
                avgdropdict[droppage].append(value)
                avgmodedict[modestr].append(value)
                avgpricedict[price].append(value)
        
                try:
                    plt.scatter(droppage, value, color=color)
                except:
                    pass
    
etfavg = list()
for akey,alist in avgmodedict.items():
    avg = z.avg(alist)
    etfavg.append(avg)

for akey,alist in avgdropdict.items():
    avg = z.avg(alist)
    etfavg.append(avg)

for akey,alist in avgpricedict.items():
    avg = z.avg(alist)
    etfavg.append(avg)

#print(zen.getSortedStocks.get)
avgetf = z.avg(etfavg)

print (z.getStocks.devoverride)
print("this etf avg: {}".format( avgetf))

etfcollector = sell_threader.getEtfCollector()
etfcollectort = sell_threader.getEtfCollectorT()
for akey,alist in avgmodedict.items():
    avg = z.avg(alist)
    etfvalue = etfcollector[akey]
    etft = etfcollectort[akey]
#    print("modes: {0:<12} {1:<8} {2:<7}".format( akey, avg, round(etfvalue/(numy*testpoints), 3)))
    print("modes: {0:<12} {1:<8} {2:<7}".format( akey, avg, round(etfvalue/etft,3) ))

for akey,alist in avgdropdict.items():
    avg = z.avg(alist)
    print("drop: {} {} ".format( akey, avg))

for akey,alist in avgpricedict.items():
    avg = z.avg(alist)
    print("price: {} {} ".format(akey, avg))


print("general etf winrate: {}".format(round(sell_threader.getEtfWins() / played,3)))
print (sell_threader.buySellSim.tracks)
print("years : {}".format( years ))
print("testpoints : {}".format( testpoints ))

#z.setp(avgdropdict, "{}avgdropdict".format(z.getStocks.devoverride))
#z.setp(avgmodedict, "{}avgmodedict".format(z.getStocks.devoverride))

path = z.getPath("plots/test_special.png")
plt.savefig(path)
plt.show()

#print("collector : {}".format( collector ))
