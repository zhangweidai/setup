import threading
from queue import Queue
import time
from filelock import FileLock
import worst_duration
import util

mydict = dict()
# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        astock = q.get()
        mydict[astock] = util.getCsv(astock, save = False)
        q.task_done()

# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(7):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

#util.getStocks.totalOverride = "IVV"
stocks = util.getStocks()
for astock in stocks:
    q.put(astock)
q.join()

print ("am i done")
what = mydict["BA"].at[3,'Date']
print("what : {}".format( what ))
