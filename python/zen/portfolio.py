# Import pandas

import pandas as pd
import buy
import os
import z
import csv
from collections import defaultdict
from sortedcontainers import SortedSet

#"Account Name/Number","Symbol","Description","Quantity","Last Price","Last Price Change","Current Value","Today's Gain/Loss Dollar","Today's Gain/Loss Percent","Total Gain/Loss Dollar","Total Gain/Loss Percent","Cost Basis Per Share","Cost Basis Total","Type"

port = dict()
def process(path):
    global port
    xl = pd.ExcelFile(path)
    df = xl.parse(xl.sheet_names[0])
    vals = df.columns.values
    syms = df[vals[1]].tolist()[1:]
    count = df[vals[4]].tolist()[1:]
    for i, sym in enumerate(syms):
        port.setdefault(sym, 0)
        port[sym] += count[i]


def getTrainingMotif():
    import fnmatch
    pattern = "*.xlsx"  
    holds = []
    listOfFiles = os.listdir('../zen_dump/port')  
    for path in listOfFiles:  
        if fnmatch.fnmatch(path, pattern):
            process("../zen_dump/port/" + path)

skips = ["FNSXX", "VTRLX", "BLNK", "BLCN"]

def getBasis(astock):
    return float(port[astock])

def getPortfolio(aslist = False, stocksOnly = False):
    global port

    if aslist:
        if not stocksOnly:
            return list(port.keys())
        ret = list(port.keys())
        etfs = z.getEtfList(forEtfs = True)
        retlist = []
        for astock in ret:
            if astock not in etfs:
                retlist.append(astock)
        return retlist
    return port

#account,average_price,cancel,created_at,cumulative_quantity,execution_state,extended_hours,fees,first_execution_at,id,instrument,last_transaction_at,num_of_executions,override_day_trade_checks,override_dtbp_checks,position,price,quantity,ref_id,reject_reason,response_category,settlement_date,side,state,stop_price,symbol,time_in_force,trigger,type,updated_at,url

second = False

def getFidDumps():
    import fnmatch
    parentdir = "/mnt/c/Users/Zoe/Downloads"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"

    listOfFiles = os.listdir(parentdir)
    bar = SortedSet()
    dic = dict()
    for entry in listOfFiles:  
        if "screener_resul" not in entry:
            continue
        fullpath = "{}/{}".format(parentdir, entry)
        print("fullpath : {}".format( fullpath ))
        xl = pd.ExcelFile(fullpath)
        df = xl.parse(xl.sheet_names[0])
        vals = df.columns.values
#        print("vals: {}".format( vals))
#        print (list(vals).index("Symbol"))
        cashidx =  list(vals).index("Free Cash Flow")
#        syms = df[vals[0]].tolist()[1:]
#        count = df[vals[4]].tolist()[1:]
        for i, row in enumerate(df.values):
            astock = row[0]
            if type(astock) is float:
                continue
            if " " in astock or "/" in astock:
                continue

            fl = float(row[cashidx])
            bar.add((fl, astock))
            dic[astock] = fl

    buy.sortedSetToRankDict("fcfdic", bar, reverse=True)
    z.setp(dic, "fcfdic2")
#
#getFidDumps()
#exit()
import regen_stock
def process_adr():
    import fnmatch
    parentdir = "/mnt/c/Users/Zoe/Downloads"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"

    listOfFiles = os.listdir(parentdir)
    bar = SortedSet()
    dic = dict()
    stocks = list()
    for entry in listOfFiles:  
        if "adr" not in entry:
            continue
        fullpath = "{}/{}".format(parentdir, entry)
        print("fullpath : {}".format( fullpath ))
        xl = pd.ExcelFile(fullpath)
        df = xl.parse(xl.sheet_names[0])
        vals = df.columns.values
        for i, row in enumerate(df.values):
            astock = row[0]
            if type(astock) is float:
                continue
            if " " in astock or "/" in astock:
                continue
            stocks.append(astock)
    print (" ".join(stocks))
    print("stocks: {}".format( stocks))
#process_adr()
#exit()

def getFidelities():
    import fnmatch
    parentdir = "/mnt/c/Users/Zoe/Downloads"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"

    listOfFiles = os.listdir(parentdir)
    bar = SortedSet()
    for entry in listOfFiles:  
        if "Portfolio" not in entry:
            continue
        if ".csv" not in entry:
            continue
        fullpath = "{}/{}".format(parentdir, entry)
        print("fullpath : {}".format( fullpath ))
        tim = os.path.getmtime(fullpath)
        bar.add((tim, fullpath))
        os.system("chmod 777 {}".format(fullpath) )
    return bar


def getLatestFidelityCsv():
    global second
    import fnmatch
    parentdir = "/mnt/c/Users/Zoe/Downloads"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"

    listOfFiles = os.listdir(parentdir)
    newest = 0
    cfile = None
    for entry in listOfFiles:  
#        if second and "_2" not in entry:
#            continue
#        elif "_1" not in entry:
#            continue

        if "Portfolio" not in entry:
            continue
        if ".csv" not in entry:
            continue
        fullpath = "{}/{}".format(parentdir, entry)
        tim = os.path.getmtime(fullpath)
        if tim > newest:
            newest = tim
            cfile = fullpath

    print("fidelity file: {}".format( cfile))
    os.system("chmod 777 {}".format(cfile) )
    yield cfile

saved_gain = None    
down_gain = None
downps = None
cost_change = None

def saveGain(account, astock, c_gain, quant):
    global saved_gain, down_gain, downps, cost_change

    key = "{}_{}".format(account, astock)
    done = False
    try:
        prev_gain, prev_quant = saved_gain[key]
    except:
        done = True
        saved_gain[key] = c_gain, quant
        if c_gain < 0:
            down_gain[key] = abs(c_gain)

    if not done:
        if prev_gain < c_gain:
            saved_gain[key] = c_gain, quant
            down_gain[key] = None
        elif quant > (prev_quant * 1.15) or quant < prev_quant:
            saved_gain[key] = c_gain, quant
            if c_gain > 0:
                down_gain[key] = None
            else:
                down_gain[key] = abs(c_gain)
        elif c_gain < 0:
            if prev_gain > 0:
                down_gain[key] = c_gain - prev_gain
            else:
                down_gain[key] = abs(c_gain)
        elif prev_gain > c_gain:
            answer = round(prev_gain-c_gain,2)
            down_gain[key] = answer
        else:
            down_gain[key] = None

    try:
        if down_gain[key] > 0:
            downps[astock].append(down_gain[key])
    except Exception as e:
        pass

cash = 0
cashlist = list()
def simple(path, dontknow, etfs, total):
    global ports, second, mine, tory, sset, cost_change, cash, cashlist
    ccash = 0

    for row in csv.DictReader(open(path)):
        isetf = False
        astock = row['Description'] 
        try:
            if " ETF" in astock:
                isetf = True
        except:
            pass

        astock = row['Symbol'] 
        if "**" in astock or astock == "FNSXX":
            c_value = float(row['Current Value'].strip("$").strip(" ").replace(',',''))
            cash += c_value
            ccash += c_value
            cashlist.append(c_value)
            continue

        if len(astock) >= 1 and astock not in skips:

            try:
                quant = float(row['Quantity'])
                c_value = float(row['Current Value'].strip("$").strip(" ").replace(',',''))
                c_gain = float(row['Total Gain/Loss Percent'].strip("%"))
                c_account = row['Account Name/Number']
                saveGain(c_account, astock, c_gain, quant)
            except Exception as e:
                print("astock: {}".format( astock))
                print("row: {}".format( row))
                z.trace(e)
#                exit()
                continue

            try:
                c_basis = float(row['Cost Basis Per Share'].strip("$").strip(" ").replace(',',''))
                if astock not in cost_change:
                    cost_change[astock] = (quant, c_basis)
                else:
                    prev_quant, prev_basis = cost_change[astock]
                    new_quant = prev_quant + quant
                    new_total = round(((prev_basis * prev_quant) + (quant * c_basis))/new_quant,2)
                    cost_change[astock] = (new_quant, new_total)
            except Exception as e:
                continue
            
            if second:
                tory.append(astock)
            else:
                mine.append(astock)

            total += c_value

            if not isetf:
                try:
                    mc = buy.getMCRank(astock)
                    binid = mc // 50
                    sset[binid] += c_value
                except Exception as e:
                    print("prob 2 astock: {} {}".format( astock, c_value))
                    dontknow += c_value
                    pass
            else:
                etfs += c_value

            ports[astock] = round(ports[astock] + c_value,2)
    return dontknow, etfs, total, ccash

ports = None
tory = None
mine = None
sset = None
def getPorts():
    import locale
    locale.setlocale( locale.LC_ALL, '' )

    paths = getFidelities()
    if len(paths) != 2:
        print ("Unexpected number of files")
        exit()

    global ports, second, ports, tory, mine, sset, saved_gain, cost_change
    ports = defaultdict(int)
    mine = list()
    tory = list()
    sset = defaultdict(int)

    total = 2838
    ccash = 0
    dontknow = 0
    etfs = 0

    dontknow, etfs, total, ccash = simple(paths[0][1], dontknow, etfs, total)
    print("P total : {}".format(locale.currency( total+ccash , grouping=True )))
    print("P cash  : {}".format(locale.currency( ccash , grouping=True )))
    print("        : {}".format(round(ccash/(total+ccash),2)))

    second = True
    total2 = 0

    dontknow, etfs, total2, ccash = simple(paths[1][1], dontknow, etfs, total2)
    print("T total : {}".format(locale.currency( total2+ccash , grouping=True )))
    print("T cash  : {}".format(locale.currency( ccash , grouping=True )))
    print("        : {}".format(round(ccash/(total2+ccash),2)))
    total += total2

    vg = round(vanguard())
    print("Vanguard: {}".format(locale.currency( vg , grouping=True )))
    total += vg
    etfs += vg
    total += cash
    total = round(total)
    print("Total  : {}".format(locale.currency( total , grouping=True )))

    z.setp(cost_change, "cost_change")
    z.setp(saved_gain, "saved_gain")
    z.setp(down_gain, "down_gain")
    z.setp(downps, "downps")

    z.setp(ports,"ports")
    z.setp(mine, "mine")
    z.setp(tory, "tory")
    if dontknow:
        print("dontknow : {}".format( dontknow ))

    skeys = sorted(sset.keys())
    for akey in skeys:
        res = round(round(sset[akey] / total,3) * 100,2)
        dkey = "{}-{}".format(akey*50, (akey+1)*50)
        print(" {:>10} {:>6}% {:>6}".format( dkey, res, round(sset[akey]) ))

    try:
        res = round(dontknow / total,3) * 100
        print(" {:>10} {:>6}% {:>6}".format( "dontknow", res, round(dontknow) ))
    except:
        pass

    try:
        res = round(round(etfs / total,3) * 100,2)
        print(" {:>10} {:>6}% {:>6}".format( "etfs", res, round(etfs)))
    except:
        pass
    print("Cash  : {}".format(locale.currency( cash , grouping=True )))
    print("cashlist: {}".format( cashlist))

    z.setp(sset, "mcranges")

def vanguard():
    global ports, cash, cashlist
    parentdir = "/mnt/c/Users/Zoe/Downloads"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"
    csvfile = "ofxdownload.csv"
    path = "{}/{}".format(parentdir, csvfile)
    ret = 0
    for row in csv.DictReader(open(path)):
        try:
            val = float(row["Total Value"])
            astock = row["Symbol"]
            if astock == "VMFXX":
                cash += val
                cashlist.append(c_value)
                continue
        except:
            val = 0
            pass

        if val:
            ports[astock] = round(ports[astock] + val, 2)
            ret += val
    return ret

if __name__ == '__main__':

#    saved_gain = z.getp("saved_gain") or dict()
#    down_gain = z.getp("down_gain") or dict()
    downps = defaultdict(list)
    saved_gain = dict()
    down_gain = dict()
    cost_change = defaultdict(tuple)
    getPorts()

