import threading
from queue import Queue
import z
import worst_duration
import random
import sell_threader
import generate_list
import dask_help
from collections import defaultdict
import matplotlib.pyplot as plt

sell_threader.setTranscript.enabled = False
sell_threader.buySellSim.tracks = 8
dask_help.getModes.override = ["Volume"]

z.getStocks.devoverride = "IUSG"
generate_list.getSortedStocks.get = "low"

use_q = True
testpoints = 600
print("testpoints : {}".format( testpoints ))
years = 1.4

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        sell_threader.buySellSim(q.get())
        q.task_done()


dates = z.getp("dates")
num_days = len(dates)

ayear = 252
duration = int (years * ayear)

starti = num_days-(duration*2)
endi = num_days-duration
startd = dates[starti]
endd = dates[endi]

prices_only = False
if generate_list.getSortedStocks.get == "price":
    prices_only = True
generate_list.setSortedDict(prices_only = prices_only)

q = Queue()
for x in range(7):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

print("num_days : {} - {} {}".format( num_days, startd, endd ))
played = 0
def calcPortfolio(droppage, mode, price):
    global played
    for tries in range(testpoints):
        start = random.randrange(starti, endi)
        end = start + duration
        played += 1
        if use_q:
            q.put([droppage, start, end, mode, price])
        else:
            sell_threader.buySellSim([droppage, start, end, 
                    mode, price])

def getColors():
    return ["blue", "red", "green", "black", 'cyan', 'brown', 
            'orange', 'pink', 'magenta', 'olive']

ylist = [i/100 for i in range(76,96,2)]

price = -1
pricelist = [price]
if generate_list.getSortedStocks.get == "price":
    pricelist = [i for i in range(4)]

    for droppage in ylist:
        for price in pricelist:
            calcPortfolio(droppage, mode="Change", price=price)

else:
    for droppage in ylist:
        for mode in dask_help.getModes():
            calcPortfolio(droppage, mode=mode, price=price)
q.join()

collector = sell_threader.getCollector()
avgdropdict = defaultdict(list)
avgmodedict = defaultdict(list)
avgpricedict = defaultdict(list)

mode = "Change"
if generate_list.getSortedStocks.get == "price":
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
        for mode in dask_help.getModes():
    
            modeidx = dask_help.getModes().index(mode)
            color = getColors()[modeidx]
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

#print(generate_list.getSortedStocks.get)
avgetf = z.avg(etfavg)
print("this etf avg: {}".format( avgetf))

for akey,alist in avgmodedict.items():
    avg = z.avg(alist)
    if avg > avgetf:
        print("modes: {} {} ".format( akey, avg))

for akey,alist in avgdropdict.items():
    avg = z.avg(alist)
    if avg > avgetf:
        print("drop: {} {} ".format( akey, avg))

for akey,alist in avgpricedict.items():
    avg = z.avg(alist)
    print("price: {} {} ".format(akey, avg))


print("general etf winrate: {}".format(round(sell_threader.getEtfWins() / played,3)))
print (sell_threader.buySellSim.tracks)

#z.setp(avgdropdict, "{}avgdropdict".format(z.getStocks.devoverride))
#z.setp(avgmodedict, "{}avgmodedict".format(z.getStocks.devoverride))

path = z.getPath("plots/test_special.png")
plt.savefig(path)
plt.show()

#print("collector : {}".format( collector ))
