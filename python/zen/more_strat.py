import threading
from queue import Queue
import z
import worst_duration
import random
import sell_threader
import zen
import threadprep
from collections import defaultdict
import matplotlib.pyplot as plt

threadprep.getModes.useRandom = True
sell_threader.setTranscript.enabled = False
sell_threader.buySellSim.tracks = 30

zen.loadSortedEtf("BUY2")
#z.getStocks.devoverride = "ITOT"
#zen.getSortedStocks.get = "low"

use_q = True
testpoints = 15
years = 2.5

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        sell_threader.buySellSim(q.get())
        q.task_done()

dates = z.getp("dates")
num_days = len(dates)

starti = dates.index("2013-04-12")

ayear = 252
duration = int (years * ayear)

endi = (num_days-duration)-1
startd = dates[starti]
print("startd : {}".format( startd ))
endd = dates[endi]
print("endd : {}".format( endd ))

q = Queue()
for x in range(7):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

print("num_days : {} - {} {}".format( endi- starti, startd, endd ))
played = 0

def getColors():
    return ["blue", "red", "green", "black", 'cyan', 'brown', 
            'orange', 'pink', 'magenta', 'olive', "indigo", "teal", "silver"]

types = ["low", "high", "both"]
ylist = [i/100 for i in range(55,90,5)]
numy = len(ylist)

#points = [ random.randrange(starti, endi) for tries in range(testpoints) ]
#print("points : {}".format( points ))
points = z.getp("{}points{}".format(years, testpoints))
if not points:
    points = [ random.randrange(starti, endi) for tries in range(testpoints) ]
    z.setp(points, "{}points{}".format(years, testpoints))

for droppage in ylist:
    for start in points:
        end = start + duration
        for typed in types:
            for mode in threadprep.getModes():
                played += 1
                if use_q:
                    q.put([droppage, start, end, mode, typed])
                else:
                    sell_threader.buySellSim([droppage, start, end, mode, typed])
q.join()
collector = sell_threader.getCollector()
avgdropdict = defaultdict(list)
avgmodedict = defaultdict(list)

for droppage in ylist:
    for typed in types:
        zen.getSortedStocks.get = typed
        for mode in threadprep.getModes():
            modeidx = threadprep.getModes().index(mode)
            color = getColors()[modeidx]
            modestr = "{}/{}".format(mode, typed)
            tupp = (droppage, modestr)
            try:
                value = z.avg(collector[tupp])
            except Exception as e:
                print("1tupp : {}".format( tupp ))
                z.trace(e)
                raise SystemExit
                continue
            avgdropdict[droppage].append(value)
            avgmodedict[modestr].append(value)
    
            try:
                plt.scatter(droppage, value, color=color)
            except:
                pass

etfavg = list()
for akey,alist in avgmodedict.items():
    avg = z.avg(alist)
    etfavg.append(avg)

for mode in threadprep.getModes():
    typed = "low"
    modestr = "{}/{}".format(mode, typed)
    avgl = z.avg(avgmodedict[modestr])

    typed = "high"
    modestr = "{}/{}".format(mode, typed)
    avgh = z.avg(avgmodedict[modestr])
    print("mode {}: {}".format(mode,  round(abs(avgl-avgh),3) ))

for akey,alist in avgdropdict.items():
    avg = z.avg(alist)
    etfavg.append(avg)

avgetf = z.avg(etfavg)

print (z.getStocks.devoverride)
print("testpoints : {}".format( testpoints ))
print("this etf avg: {}".format( avgetf))

etfcollector = sell_threader.getEtfCollector()
etfcollectort = sell_threader.getEtfCollectorT()
for akey,alist in avgmodedict.items():
    avg = z.avg(alist)
    etfvalue = etfcollector[akey]
    etft = etfcollectort[akey]
    print("modes: {0:<12} {1:<8} {2:<7}".format( akey, avg, round(etfvalue/etft,3) ))

for akey,alist in avgdropdict.items():
    avg = z.avg(alist)
    print("drop: {} {} ".format( akey, avg))

print("general etf winrate: {}".format(round(sell_threader.getEtfWins() / played,3)))
print (sell_threader.buySellSim.tracks)
print("years : {}".format( years ))
print("testpoints : {}".format( testpoints ))

#z.setp(avgdropdict, "{}avgdropdict".format(z.getStocks.devoverride))
#z.setp(avgmodedict, "{}avgmodedict".format(z.getStocks.devoverride))
try:
    transcript, transcript2 = sell_threader.getTranscript()
    path = z.getPath("transcript/{}high.txt".format(zen.loadSortedEtf.etf))
    print("path: {}".format( path))
    with open(path, "w") as f:
        f.write("\n".join(transcript))
    
    path = z.getPath("transcript/{}low.txt".format(zen.loadSortedEtf.etf))
    with open(path, "w") as f:
        f.write("\n".join(transcript2))
except:
    pass

import portfolio

bar = z.getp("highest")
print ("worthNow {}".format(portfolio.worthNow(bar)))

bar = z.getp("lowest")
print ("worthNow {}".format(portfolio.worthNow(bar)))

path = z.getPath("plots/test_special.png")
plt.savefig(path)
plt.show()

#print("collector : {}".format( collector ))
