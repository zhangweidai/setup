import threading
from queue import Queue
import time
from filelock import FileLock
import worst_duration
import util

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        astock = q.get()
        worst_duration.getScoreLocked(astock)
        q.task_done()

# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(6):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

stocks = util.getStocks()
for i,astock in enumerate(stocks):
    if i < 82 or i > 200: 
        continue
    print ("sent "+astock)
    q.put(astock)
q.join()
