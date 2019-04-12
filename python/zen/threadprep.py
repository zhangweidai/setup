import z
from collections import defaultdict, deque
from threading import Lock
from sortedcontainers import SortedSet
import csv

modes = [ 'Volume', 'Price', "C5", "C12", "C24", "C50"]
keeping = 40
discardlocation = int(keeping/2)

mutex = Lock()
sdict = defaultdict(dict)
interval=5
def doone(astock):
    path = z.getPath("historical/{}.csv".format(astock))
    currentStack = deque([])
    prevPrices = deque([])
    for row in csv.DictReader(open(path)):
        date = row['Date']
        tokens = date.split("-")
        year = int(tokens[0])
        prev5 = 0
        if year >= 2012 and int(tokens[1]) > 8:
            currentStack.append(int(row['Volume']))
            value = float(row['Close'])
            prevPrices.append(value)
            if len(currentStack) > interval:
                currentStack.popleft()
            if len(prevPrices) > 51:
                prevPrices.popleft()

        if year < 2013:
            continue

        close = float(row['Close'])
        for mode in modes:
            if mode == "C5":
                value = round(close/prevPrices[5],3)

            elif mode == "C12":
                value = round(close/prevPrices[12],3)

            elif mode == "C24":
                value = round(close/prevPrices[24],3)

            elif mode == "C50":
                value = round(close/prevPrices[50],3)

            elif mode == "Volume":
                try:
                    value = z.avg(currentStack)
                except:
                    value = int(row['Volume'])
            else:
                value = close
            try:
                sdict[mode][date].add((value, astock))
            except Exception as e:
                try:
                    sdict[mode][date] = SortedSet([(value, astock)])
                except Exception as e:
                    z.trace(e)
                    raise SystemExit                    

#            mutex.acquire()
#            try:
            if len(sdict[mode][date]) > keeping:
                sdict[mode][date].discard(sdict[mode][date][discardlocation])
#            finally:
#                mutex.release()


def threader():
    global q
    while True:
        doone(q.get())
        q.task_done()

q = None
def doit():
    global q
    import threading
    from queue import Queue
    q = Queue()
    for x in range(2):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    stocks = z.getStocks(dev=True)
    for astock in stocks:
        doone(astock)
#        break
#        q.put(astock)

    q.join()
#    print("sdict: {}".format( sdict['Price']['2013-03-13']))
#    print ("asdfasdfasdf")
    print("sdict: {}".format( sdict['C5']['2013-03-13']))
#    bar = z.getp("save")
#    if bar == sdict:
#       print ("ok") 
#    else:
#       print ("notok") 
#    z.setp(sdict, "save")
#    print("sdict: {}".format( sdict['2003-06-30']))

doit()
