import threading
from queue import Queue
import z
import worst_duration
import random
import sell_threader
import generate_list
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

def calcPortfolio(droppage, mode):
    print("mode: {}".format(mode))
    for tries in range(23):
        print("tries : {}".format( tries ))
        start = random.randrange(num_days-duration)
        end = start + duration
        q.put([droppage, start, end, mode])
        break

etfsource = "IUSG"
print ("csvs")
generate_list.getBuyStocks.stocks = z.getStocks(etfsource, preload=True)
calcPortfolio(0.5, mode="special2")
#    vari = np.var(changes)
#    average = round(sum(changes)/len(changes),3)
#    alist.append(average)
q.join()

collector = sell_threader.getCollector()
print("collector : {}".format( collector ))
