import os
import pickle
import pandas

def getPath(path, allowmake = True):
    path = "{}/../zen_dump/{}".format(os.getcwd(), path)
    parent = os.path.dirname(path)
    if allowmake and not os.path.exists(parent):
        os.makedirs(parent)
    return path

def percentage(factor):
    return "{:.2%}".format(factor-1)

def getp(name):
    try:
        path = getPath("pkl/{}.pkl".format(name))
        return pickle.load(open(path, "rb"))
    except:
        return None

def setp(data, name):
    path = getPath("pkl/{}.pkl".format(name))
    pickle.dump(data, open(path, "wb"))

def getStocks(etf = None, dev=False, reset = False, simple = False, preload = True):
    if not reset:
        try: return getStocks.ret
        except: pass

    if dev:
        if preload:
            getCsv.savedReads = getp("devdf")
        return ["SPY", "BA", "BRO"]

    if not etf:
        getStocks.ret = getp("alls")
        return getStocks.ret

    if etf and getStocks.etfs:
        getStocks.ret = getStocks.etfs[etf]
        return getStocks.ret

    if etf:
        getStocks.etfs = getp("etfdict")
        getStocks.ret = getStocks.etfs[etf]
        return getStocks.ret
getStocks.etfs = None


util = None
def getCsv(astock, asPath=False, save=True):
    csvdir = "historical"

    if asPath:
        return getPath("{}/{}.csv".format(csvdir, astock))

    try:
        if save:
            return getCsv.savedReads[astock]
    except :
        pass

    df = None
    try:
        path = getPath("{}/{}.csv".format(csvdir, astock), allowmake = False)
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
        else:
            global util
            if not util:
                import util as util
            try:
                path = util.saveProcessedFromYahoo(astock)
                if path:
                    df = pandas.read_csv(path)
                    if df is None:
                        return None

            except Exception as e:
                print (str(e))
                print ("problem with {}".format(astock))
                return None
    if save:
        getCsv.savedReads[astock] = df
    return df
getCsv.savedReads = dict()
