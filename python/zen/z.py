import os
import pickle
import pandas

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
    
def saveCsvCache():
    print ("need to update cache")
    global util
    if not util:
        import util as util
    util.saveProcessedFromYahoo.download = False
    stocks = getStocks()
    for astock in stocks:
        getCsv.savedReads[astock] = getCsv(astock)
    setp(getCsv.savedReads, "allcsvs")

def getStocks(etf = None, dev=False, reset = False, simple = False, preload = False):
    if not reset:
        try: return getStocks.ret
        except: pass

    if dev:
        if preload:
            getCsv.savedReads = getp("devdf")
        return ["SPY", "BA", "BRO"]

    if preload:
        df = getCsv("SPY")

        try:
            getCsv.savedReads = getp("allcsvs")
            df2 = getCsv.savedReads["SPY"]
            if len(df2) != len(df):
                saveCsvCache()
        except:
            getCsv.savedReads = dict()
            saveCsvCache()

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
        return getStocks.ret
getStocks.etfs = None
#print (getStocks("IUSG") - getStocks("ITOT"))
#print (len(getStocks("IUSG|IVV")))


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
        elif getCsv.download:
            global util
            if not util:
                import util as util
            try:
                print("downloading astock: {}".format( astock))
                path = util.saveProcessedFromYahoo(astock)
                if path:
                    df = pandas.read_csv(path)
                    if df is None:
                        print("did not save astock: {}".format( astock))
                        raise SystemExit
                        return None

            except Exception as e:
                print (str(e))
                print ("problem with {}".format(astock))
                return None
    if save:
        getCsv.savedReads[astock] = df
    return df
getCsv.savedReads = dict()
getCsv.download = True

def getPrice(astock, idx=-1):
    df = getCsv(astock)
    if type(idx) == int:
        return round(df.at[idx,"Close"],3)
    try:
        idx = list(df["Date"]).index(idx)
    except Exception as e:
        getPrice.noprice.append(astock)
        return None
    return round(df.at[idx,"Close"],3)
getPrice.noprice = list()

#    items = [ "ROKA", "CRDB", "LGFB", "CBSA", "MPO", "LGFA", "CRDA", 
def removeFromStocks(itemd):
    if not itemd:
        return
    stocks = getp("alls")
    dels = getp("deletes")
    for item in itemd:
        try:
            stocks.remove(item)
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
    delStock.items.append(astock)
    if save:
        removeFromStocks(delStock.items)
        clearFromEtfDics(delStock.items)

delStock.items = []
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

def getEtfList():
    return ["ITOT", "IJH", "IJR", "IVV", "IWB", "IUSG", "USMV"]

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
        print (str(e))
        pass
