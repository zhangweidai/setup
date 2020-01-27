from functools import lru_cache
import os
#import pandas
import pickle
import time

closekey = "Adj Close"
YEAR = 2020

def getPath(path, allowmake = True):
    path = "{}/../zen_dump/{}".format(os.getcwd(), path)
    parent = os.path.dirname(path)
    if allowmake and not os.path.exists(parent):
        os.makedirs(parent)
    return path


def percentage(factor, accurate=False):
    if type(factor) is str:
        return factor

    if accurate == 1:
        return "{:.1%}".format(factor-1)
    if accurate == 2:
        return "{:.2%}".format(factor-1)

    if not accurate:
        return "{:.1%}".format(factor-1)

    return "{:.3%}".format(factor-1)

def gyp(name):
    try:
        path = getPath("yahoo/{}.pkl".format(name))
        return pickle.load(open(path, "rb"))
    except:
        return None

def syp(data, name):
    path = getPath("yahoo/{}.pkl".format(name))
    if os.path.exists(path):
        os.remove(path)
    pickle.dump(data, open(path, "wb"))

getpd = set()
@lru_cache(maxsize=40)
def getp(name, override="pkl"):
    getpd.add(name)
    try:
        path = getPath("{}/{}.pkl".format(override, name))
        if not os.path.exists(path):
            return None
        return pickle.load(open(path, "rb"))
    except:
        try:
            return pickle.load(open(name, "rb"))
        except:
            pass
    return None

import atexit
gsave = False
gsavedir = None

@atexit.register
def goodbye():
    if getpd:
        print("\n---pickle report---")

    from sortedcontainers import SortedSet
    savedSort = SortedSet()
    for name in getpd:
        path = getPath("{}/{}.pkl".format("pkl", name))
        try:
            savedSort.add((os.stat(path).st_mtime, name))
        except:
            pass

    for dat, name in savedSort:
        modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dat))
        print("Modification time {} : {}".format(name, modificationTime))


    print ("\nSaved : ")
    for name in savedd:
        print(name)

    setp(getpd, "getpd")

    if not gsave or gsavedir:
        return

    from shutil import copyfile
    for save in getpd:
        path = getPath("pkl/{}.pkl".format(save))
        newpath = getPath("pkl2/{}.pkl".format(save))
        if gsavedir:
            newpath = "{}/{}.pkl".format(gsavedir, save)
        copyfile(path, newpath)

savedd = set()
def setp(data, name, printdata = False, override="pkl"):
    savedd.add(name)
    path = getPath("{}/{}.pkl".format(override, name))
    if os.path.exists(path):
        os.remove(path)
    if printdata:
        print (" {} : {} \n".format(name, data))
    pickle.dump(data, open(path, "wb"))

def online():
    return online.online
online.online = False

def avgp(lists, p=4):
    return percentage(sum(lists)/len(lists))

def avg(lists, p=4):
    return round(sum(lists)/len(lists),p)


import code, traceback, signal
def debug(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message  = "Signal received : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)

def listen():
    signal.signal(signal.SIGUSR1, debug)  # Register handler

def getEtfList(forEtfs = False, buys=False):
    if buys:
        return [ "ITOT" , "IJH", "IJR", "IVV", "IWB", "IUSG", "USMV", "BNDX", "VEA", "VIG", "VNQ", "VOO", "VTI", "VTV", "VUG", "VIG"]
    if forEtfs:
        return [ "ITOT" , "IJH", "IJR", "IVV", "IWB", "IUSG", "USMV", "VOO", "VUG"]
    return [ "IUSG", "IJH", "IJR", "IVV", "ITOT" ]

def getCsvPath(astock, year = YEAR):
    path = getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
    return path

def getPriceFromCsv(astock, year = YEAR, date = None, return_row=False):
    path = getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
    if not date:
        for row in csv.DictReader(open(path)):
            pass
        if return_row:
            return row
        return row[closekey]

    for row in csv.DictReader(open(path)):
        if row['Date'] == date:
            return row[closekey]

def avgp(lists, p=4):
    return percentage(sum(lists)/len(lists))

def avg(lists, p=4):
    return round(sum(lists)/len(lists),p)

#print(avg([2.313, 2.232, 2.358, 2.468, 2.727, 2.965, 3.262, 3.07]))
#print(avg([1.924, 1.944, 1.986, 2.123, 2.057, 2.405, 2.807, 2.822]))
#print(avg([2.359, 2.651, 2.148, 3.105, 3.109, 2.695, 3.25, 2.791]))
#print(avg([2.131, 2.417, 2.238, 2.618, 2.782, 2.829, 3.116, 3.141]))
#
#raise SystemExit

def breaker(count):
    if breaker.count == 0:
        exit()
    if not breaker.count:
        breaker.count = count
    else:
        breaker.count -= 1
        print("breaker: {}".format(breaker.count))
breaker.count = None

def trace(e):
    import traceback
    print (traceback.format_exc())
    print (str(e))

