# Import pandas
import pandas as pd
import buy
import os
import util
import z
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
import z
import csv
import zen
from collections import defaultdict

skips = ["FNSXX", "VTRLX", "BLNK", "BLCN"]
def fidelity(forselling=False, updating=False):
    global port
#    path = z.getPath("port/fidelity.csv")
    spentBasis = 0
    current_pv = 0
    need = False
    myportlist = list()
    ports = defaultdict(int)
    for row in csv.DictReader(open(getLatestFidelityCsv())):

        astock = row['Symbol'] 
        if "*" in astock:
            continue

        if len(astock) >= 1 and astock not in skips:

            myportlist.append(astock)

            try:
                c_value = float(row['Current Value'].strip("$"))
                ports[astock] = round(ports[astock] + c_value,2)
                cbprice = float(row['Cost Basis Per Share'].strip("$"))
                count = float(row['Quantity'])
                temp2 = float(row['Cost Basis Total'].strip("$"))
                spentBasis += temp2
                currentprice = zen.getPrice(astock)
                temp = round(count*currentprice,4)
#                print (z.percentage(temp/temp2))
                current_pv += temp
            except:
                print("problem astock: {}".format( astock))
                continue

            if forselling:
                try:
                    lastsaveprice = fidelity.lastSave[astock]
                except:
                    try:
                        fidelity.lastSave = z.getp("lastsaveprice")
                        if fidelity.lastSave is None:
                            fidelity.lastSave = dict()
                        lastsaveprice = fidelity.lastSave[astock]
                    except:
                        try:
                            print ("never saved before {}".format(astock))
                            lastsaveprice = max([currentprice, cbprice])
                            fidelity.lastSave[astock] = lastsaveprice
                            need = True
                        except:
                            print (zen.getPrice(astock))
                            print("astock: {}".format( astock))
                            print (cbprice)
                            print ("hsouldnt gher eher")
                            pass
                cbprice = lastsaveprice

            if updating:
                try:
                    lastsaveprice = fidelity.lastSave[astock]
                except:
                    print("no last save for astock: {}".format( astock))
                    return
                using = max([zen.getPrice(astock), lastsaveprice])
                fidelity.lastSave[astock] = using
                port[astock] = using
            else:
                port[astock] = cbprice

    if updating or need:
        z.setp(fidelity.lastSave, "lastsaveprice")

    z.setp(myportlist,"myportlist")
    z.setp(ports,"ports", printdata=True)

    return round(current_pv/spentBasis,4), spentBasis, current_pv

fidelity.allowSave = False
fidelity.lastSave = dict()


#def fidelitySellPrice():
#    global port
#    path = z.getPath("port/fidelity.csv")
#    dict
#    for row in csv.DictReader(open(path)):
##        print(row )
#        astock = row['Symbol'] 
#        if "*" in astock:
#            continue
#        if len(astock) >= 1 and astock not in skips:
#            port[astock] = 
#            bprice = float(row['Cost Basis Per Share'])
#            lprice = getPrice(astock)
#            if bprice


def getTrainingFidelity():
    global port
    path = "../zen_dump/port/DetailedHoldings.xls"
    xl = pd.ExcelFile(path)
    df = xl.parse(xl.sheet_names[0])
    vals = df.columns.values
    syms = df[vals[0]].tolist()[1:-1]
    count = df[vals[7]].tolist()[1:-1]

    for i, sym in enumerate(syms):
        port.setdefault(sym, 0)
        port[sym] += count[i]

def getBasis(astock):
    return float(port[astock])

def getPortfolio(aslist = False, stocksOnly = False):
    global port
#    getTrainingMotif()
#    getTrainingFidelity()
#    getRobin()
    fidelity()

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

def getRobin():
    global port
    path = util.getPath("port/robinhood.csv")
    df = pd.read_csv(path)
    syms = df['symbol'].tolist()
    count = df['quantity'].tolist()
    for i, sym in enumerate(syms):
        port.setdefault(sym, 0)
        port[sym] += count[i]

def worthNow(port):
    value = 0
    for astock, vec in port.items():
        cprice = zen.getPrice(astock)
        tprice = cprice * vec[0]
        value += tprice
    return round(value,3)
            
import os
second = False
from sortedcontainers import SortedSet

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
#        print("vals : {}".format( vals[0] ))
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
#            try:
#                regen_stock.process(astock)
#            except:
#                print("astock: {}".format( astock))
#                continue

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

def getSellStats(updating=False):
    fidelity(forselling=True, updating=updating)
    return
    lastSave = z.getp("lastsaveprice")
    myportlist = list()
    for row in csv.DictReader(open(getLatestFidelityCsv())):
        astock = row['Symbol'] 
        if "*" in astock:
            continue
        myportlist.append(astock)

        if len(astock) >= 1 and astock not in skips:
            cprice = z.getPrice(astock)
            try:
                last = lastSave[astock]
            except:
                continue
            try:
                if cprice == last  or cprice > last:
                    continue
            except:
                continue

            change = round(cprice / lastSave[astock], 3)
            print("astock: {} {}".format( astock , z.percentage(change)))

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
        

def simple(path, dontknow, etfs, total):
    global ports, second, mine, tory, sset, cost_change

    print("path : {}".format( path ))
    for row in csv.DictReader(open(path)):
        isetf = False
        astock = row['Description'] 
        try:
            if " ETF" in astock:
                isetf = True
        except:
            pass

        astock = row['Symbol'] 
        if "*" in astock:
            continue

        if len(astock) >= 1 and astock not in skips:

            try:
                quant = float(row['Quantity'])
                c_value = float(row['Current Value'].strip("$").strip(" ").replace(',',''))
                c_gain = float(row['Total Gain/Loss Percent'].strip("%"))
                c_account = row['Account Name/Number']
                saveGain(c_account, astock, c_gain, quant)
            except Exception as e:
                z.trace(e)
                exit()
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
    return dontknow, etfs, total


ports = None
tory = None
mine = None
sset = None
def getPorts():
    paths = getFidelities()
    if len(paths) != 2:
        print ("not enough files")
        exit()

    global ports, second, ports, tory, mine, sset, saved_gain, cost_change
    ports = defaultdict(int)
    mine = list()
    tory = list()
    sset = defaultdict(int)

    total = 0
    dontknow = 0
    etfs = 0

    dontknow, etfs, total = simple(paths[0][1], dontknow, etfs, total)
    print("total : {}".format( total ))
    second = True
    total2 = 0

    dontknow, etfs, total2 = simple(paths[1][1], dontknow, etfs, total2)
    print("total2 : {}".format( total2 ))
    total += total2

    z.setp(cost_change, "cost_change", True)
    z.setp(saved_gain, "saved_gain", True)
    z.setp(down_gain, "down_gain", True)
    z.setp(downps, "downps", True)

    z.setp(ports,"ports")
    z.setp(mine, "mine")
    z.setp(tory, "tory")
    print("dontknow : {}".format( dontknow ))

    skeys = sorted(sset.keys())
    print("total: {}".format( total))
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

    z.setp(sset, "mcranges")



if __name__ == '__main__':

#    saved_gain = z.getp("saved_gain") or dict()
#    down_gain = z.getp("down_gain") or dict()
    downps = defaultdict(list)
    saved_gain = dict()
    down_gain = dict()
    cost_change = defaultdict(tuple)
    getPorts()
#    getFidDumps()
#    import sys
#    update = None
#    try:
#        if sys.argv[1][0] == "u":
#            update = True
#    except:
#        pass
#
#    getSellStats(updating=update)
#    vals = fidelity()
#    print("vals : {}".format( vals ))
#    print("vals : {}".format( z.percentage(vals[0])))
#    print("port: {}".format(port))
#    
#    port = dict()
#    fidelity(forselling=True, updating=True)
#    print("port: {}".format(port))
#    
#    port = dict()
#    fidelity(forselling=True)
#    print("port: {}".format(port))
    
