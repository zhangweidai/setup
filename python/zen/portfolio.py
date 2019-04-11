# Import pandas
import pandas as pd
import os
import util

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

skips = ["FNSXX", "VTRLX", "BLNK"]
def fidelity(forselling=False, updating=False):
    global port
    path = z.getPath("port/fidelity.csv")
    for row in csv.DictReader(open(path)):
#        print(row )
        astock = row['Symbol'] 
        if "*" in astock:
            continue
        if len(astock) >= 1 and astock not in skips:
            price = float(row['Cost Basis Per Share'].strip("$"))
#            print("cost basis price : {}".format( price ))
            if forselling:
                try:
                    lastsaveprice = fidelity.lastSave[astock]
                except:
                    try:
                        fidelity.lastSave = z.getp("lastsaveprice")
                        lastsaveprice = fidelity.lastSave[astock]
                    except:
                        fidelity.lastSave = dict()
                        try:
                            lastsaveprice = max([zen.getPrice(astock), price])
                            fidelity.lastSave[astock] = lastsaveprice
                        except:
                            print (zen.getPrice(astock))
                            print("astock: {}".format( astock))
                            print (price)
                            print ("hsouldnt gher eher")
                            pass
                price = lastsaveprice

            if updating:
                using = max([zen.getPrice(astock), lastsaveprice])
                fidelity.lastSave[astock] = using
                port[astock] = using
            else:
                port[astock] = price

    if updating:
        z.setp(fidelity.lastSave, "lastsaveprice")

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


if __name__ == '__main__':
    fidelity()
    print("port: {}".format(port))
    
    port = dict()
    fidelity(forselling=True, updating=True)
    print("port: {}".format(port))
    
    port = dict()
    fidelity(forselling=True)
    print("port: {}".format(port))
    
