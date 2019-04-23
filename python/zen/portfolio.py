# Import pandas
import pandas as pd
import os
import util
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

skips = ["FNSXX", "VTRLX", "BLNK", "BLCN"]
def fidelity(forselling=False, updating=False):
    global port
#    path = z.getPath("port/fidelity.csv")
    spentBasis = 0
    current_pv = 0
    need = False
    myportlist = list()
    for row in csv.DictReader(open(getLatestFidelityCsv())):
        astock = row['Symbol'] 
        if "*" in astock:
            continue

        if len(astock) >= 1 and astock not in skips:

            myportlist.append(astock)
            cbprice = float(row['Cost Basis Per Share'].strip("$"))

            try:
                count = float(row['Quantity'])
                temp2 = float(row['Cost Basis Total'].strip("$"))
                spentBasis += temp2
                currentprice = zen.getPrice(astock)
                temp = round(count*currentprice,4)
#                print (z.percentage(temp/temp2))
                current_pv += temp
            except:
                print("astock: {}".format( astock))
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

def getPortfolio(aslist = False):
    global port
#    getTrainingMotif()
#    getTrainingFidelity()
#    getRobin()
    fidelity()

    if aslist:
        return list(port.keys())
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
def getLatestFidelityCsv():
    import fnmatch
    parentdir = "/mnt/c/Users/Zoe/Downloads"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"

    listOfFiles = os.listdir(parentdir)
    newest = 0
    cfile = None
    for entry in listOfFiles:  
        if "Portfolio" not in entry:
            continue
        if ".csv" not in entry:
            continue
        fullpath = "{}/{}".format(parentdir, entry)
        tim = os.path.getmtime(fullpath)
        if tim > newest:
            cfile = fullpath

    print("fidelity file: {}".format( cfile))
    os.system("chmod 777 {}".format(cfile) )
    return cfile

def getSellStats(updating=False):
    fidelity(forselling=True, updating=updating)
    lastSave = z.getp("lastsaveprice")
    myportlist = list()
    for row in csv.DictReader(open(getLatestFidelityCsv())):
        astock = row['Symbol'] 
        if "*" in astock:
            continue
        myportlist.append(astock)

        if len(astock) >= 1 and astock not in skips:
            cprice = z.getPrice(astock)
            last = lastSave[astock]
            if cprice == last  or cprice > last:
                continue
            change = round(cprice / lastSave[astock], 3)
            print("astock: {} {}".format( astock , z.percentage(change)))
    
if __name__ == '__main__':
    import sys
    update = None
    try:
        if sys.argv[1][0] == "u":
            update = True
    except:
        pass

    getSellStats(updating=update)
#    vals = fidelity(forselling)
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
    
