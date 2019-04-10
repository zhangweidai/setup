import os
import pickle
import pandas
from functools import lru_cache

def getPath(path, allowmake = True):
    path = "{}/../zen_dump/{}".format(os.getcwd(), path)
    parent = os.path.dirname(path)
    if allowmake and not os.path.exists(parent):
        os.makedirs(parent)
    return path

def getAdded():
    ret = set()
    ret.add("SPY")
    return ret


def online():
    return online.online
online.online = False

def percentage(factor):
    if type(factor) is str:
        return factor
    return "{:.2%}".format(factor-1)

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

@lru_cache(maxsize=8)
def getp(name, override="pkl"):
    try:
        path = getPath("{}/{}.pkl".format(override, name))
        return pickle.load(open(path, "rb"))
    except:
        return None

def setp(data, name, override="pkl"):
    path = getPath("{}/{}.pkl".format(override, name))
    if os.path.exists(path):
        os.remove(path)
    pickle.dump(data, open(path, "wb"))

def getCorruptStocks():
    problems = []
    stocks = getStocks()
    print(len(stocks))
    for astock in stocks:
        df = getCsv(astock)
        if df is None:
            problems.append(astock)
            continue
        vals = []
        for idx in range(len(df)-1):
            start = df.at[idx,"Close"]
            end = df.at[idx+1,"Close"]
            change = start/end
            if change > 4 or change < 0.15:
                problems.append(astock)
                break

    print("problems: {}".format( problems))
    return problems
    
def saveCsvCache( csv_pkl_name, etf = None ):
    print ("need to update cache")
    global util
    if not util:
        import util as util
    util.saveProcessedFromYahoo.download = False
    stocks = getStocks(etf)
    for astock in stocks:
        getCsv.savedReads[astock] = getCsv(astock, save=False)
    getCsv.savedReads["SPY"] = getCsv("SPY", save=False)
    setp(getCsv.savedReads, csv_pkl_name)

def getStocks(etf = None, dev=False, reset = False, 
        simple = False, preload = False):

    if dev or getStocks.devoverride == True:
        if preload:
            getCsv.savedReads = getp("devdf")
#        return ["OLLI", "UA"]
        return ["SPY", "BA", "C", "KO", "AMD"]

    if not reset:
        try: return getStocks.ret
        except: pass

    if getStocks.devoverride:
        etf = getStocks.devoverride

    if preload:
        df = getCsv("SPY")
        csv_pkl_name = "{}csvs".format(etf or "all")

        print("csv_pkl_name : {}".format( csv_pkl_name ))
        try:
            getCsv.savedReads = getp(csv_pkl_name)
            df2 = getCsv.savedReads["SPY"]
            if len(df2) != len(df):
                saveCsvCache(csv_pkl_name, etf)
        except:
            getCsv.savedReads = dict()
            saveCsvCache(csv_pkl_name, etf)

    if not etf:
        getStocks.ret = (getp("alls") | set(getEtfList()) | getAdded())
        return getStocks.ret 

    if not getStocks.etfs:
        getStocks.etfs = getp("etfdict")

    if etf:
        if "/" in etf:
            tokens = etf.split("/")
            getStocks.ret = getStocks.etfs[tokens[0]].intersection(\
                    getStocks.etfs[tokens[1]])
        elif "-" in etf:
            tokens = etf.split("-")
            getStocks.ret = getStocks.etfs[tokens[0]] - \
                    getStocks.etfs[tokens[1]]
        elif "|" in etf:
            tokens = etf.split("|")
            getStocks.ret = getStocks.etfs[tokens[0]] | \
                    getStocks.etfs[tokens[1]]
        else:
            getStocks.ret = getStocks.etfs[etf]

        if getStocks.extras:
            getStocks.ret |= set(getConsider())
            if getStocks.sells:
                import portfolio
                bar = portfolio.getPortfolio(aslist=True)
                getStocks.ret |= set(bar)

        return getStocks.ret

getStocks.etfs = None
getStocks.devoverride = False
getStocks.extras = False
getStocks.sells = False

#print (getStocks("IUSG") - getStocks("ITOT"))
#print (len(getStocks("IUSG|IVV")))
#raise SystemExit

import dask.dataframe as dd
util = None
def getCsv(astock, asPath=False, save=True):

    if asPath:
        return getPath("{}/{}.csv".format(getCsv.csvdir, astock))

    try:
        if save:
            return getCsv.savedReads[astock]
    except :
        pass

    df = None
    try:
        path = getPath("{}/{}.csv".format(getCsv.csvdir, astock), allowmake = False)
        df = pandas.read_csv(path)
        if df is None:
            return None
    except:
        # allow getCsv to return from specified csv files
        path = getPath(astock, allowmake = False)
        if os.path.exists(path):
            df = pandas.read_csv(path)
            if df is None:
                return None
        elif getCsv.download:
            global util
            if not util:
                import util as util
            try:
                path = util.saveProcessedFromYahoo(astock)
                if path:
                    print("downloading astock: {}".format( astock))
                    df = pandas.read_csv(path)
                    if df is None:
                        print("did not save astock: {}".format( astock))
                        raise SystemExit
                        return None

            except Exception as e:
                trace(e)
                print ("problem with {}".format(astock))
                return None
    if save:
        getCsv.savedReads[astock] = df
    return df
getCsv.csvdir = "historical"
getCsv.savedReads = dict()
getCsv.download = True
def getLatestDate(etf="IUSG", final=""):
    import datetime
    path = getPath("pkl/{}prices{}.pkl".format(etf, final))
    t = os.path.getmtime(path)
    pdate = str(datetime.datetime.fromtimestamp(t)).split(" ")[0]
    return pdate

import zen
def getPrice(*kwargs, **kwarg2s):
    return zen.getPrice(*kwargs, **kwarg2s)
#    df = getCsv(astock)
#    if type(idx) == int:
#        return round(df.at[idx,"Close"],3)
#    try:
#        idx = list(df["Date"]).index(idx)
#    except Exception as e:
#        getPrice.noprice.append(astock)
#        return None
#    return round(df.at[idx,"Close"],3)
#getPrice.noprice = list()

#    items = [ "ROKA", "CRDB", "LGFB", "CBSA", "MPO", "LGFA", "CRDA", 
def removeFromStocks(itemd):
    if not itemd:
        return
    stocks = getp("alls")
    dels = getp("deletes")
    for item in itemd:
        try:
            stocks.remove(item)
            path = getPath("historical/{}.csv".format(item))
            os.remove(path)
        except:
            pass
        dels.add(item)
    setp(stocks, "alls")
    setp(dels, "deletes")

def clearFromEtfDics(items = None):
    dels = items if items else getp("deletes")
    etfs = getp("etfdict")
    stocks = getp("alls")
    for key in etfs:
        for astock in dels:
            try:
                etfs[key].remove(astock)
            except:
                pass
            try:
                stocks.remove(astock)
            except:
                pass
    setp(stocks, "alls")
    setp(etfs, "etfdict")

def delStock(astock, save=False):
    if type(astock) is set:
        delStock.items = delStock.items + list(astock)
    elif type(astock) is list:
        delStock.items = delStock.items + astock
    else:
        delStock.items.append(astock)
        path = getPath("historical/{}.csv".format(astock))
        try:
            os.remove(path)
        except:
            pass
    if save:
        removeFromStocks(delStock.items)
        clearFromEtfDics(delStock.items)
delStock.items = []

#delStock(getp("deletes"), save=True)
#raise SystemExit
#delStock("JWA", save=True)

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

def getEtfList(forEtfs = False):
    if forEtfs:
        return [ "IJH" ]
#        return [ "ITOT" , "IJH", "IJR", "IVV", "IWB", "IUSG", "USMV"]
    return [ "IUSG", "IJH", "IJR", "IVV", "ITOT" ]
#    , "USMV"
#    ]
#    "IWB", 

def avg(lists):
    return round(sum(lists)/len(lists),3)

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

def getConsider():
    return ["FF", "ACB", "BABA", "CRM", "ABT", "GM", "YUM", "ZEN", "BNS", "WPG", \
        "PAGS", "ZTS", "CSGP", "CGNX", "EW", "VMC", "ASML", "AGN", "HRS"]

def getConsider2():
    return {"Janus": ["PAGS","ZTS", "CSGP"]}

#removeFromStocks(getCorruptStocks())
if __name__ == '__main__':
    import sys
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "delete":
                astock = sys.argv[2]
                print("astock : {}".format( astock ))
                delStock(astock, True)
    except Exception as e:
        trace(e)
        pass

