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
z.getStocks.devoverride = True
generate_list.setSortedDict()

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        sell_threader.buySellSim(q.get())
        q.task_done()

# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(7):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

dates = z.getp("dates")
num_days = len(dates)
years = 3
ayear = 252
duration = int (years * ayear)
print("num_days : {}".format( num_days ))
use_q = True
def calcPortfolio(droppage, mode):
    for tries in range(10):
        start = random.randrange(num_days-duration)
        end = start + duration
        if use_q:
            q.put([droppage, start, end, mode])
        else:
            sell_threader.buySellSim([droppage, start, end, mode])

def getColors():
    return ["blue", "red", "green", "black", 'cyan', 'brown', 
            'orange', 'pink']

ylist = [i/100 for i in range(76,92,4)]
for droppage in ylist:
    for mode in dask_help.getModes():
        calcPortfolio(droppage, mode=mode)
q.join()

collector = sell_threader.getCollector()
avgdropdict = defaultdict(list)
avgmodedict = defaultdict(list)
for droppage in ylist:
    for mode in dask_help.getModes():
        modeidx = dask_help.getModes().index(mode)
        color = getColors()[modeidx]
        tupp = (droppage, mode)
        value = collector[tupp]

        avgdropdict[droppage].append(value)
        avgmodedict[mode].append(value)

#        plt.scatter(droppage, collector[tupp], color=color)

for akey,alist in avgmodedict.items():
    print("modes: {} {} ".format( akey, z.avg(alist)))
for akey,alist in avgdropdict.items():
    print("drops: {} {} ".format( akey, z.avg(alist)))

path = z.getPath("plots/test_special.png")
plt.savefig(path)
plt.show()

#print("collector : {}".format( collector ))
