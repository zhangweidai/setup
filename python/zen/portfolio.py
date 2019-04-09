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
def fidelity():
    global port
    skips = ["FNSXX", "VTRLX", "BLNK"]
    path = z.getPath("port/fidelity.csv")
    for row in csv.DictReader(open(path)):
#        print(row )
        astock = row['Symbol'] 
        if "*" in astock:
            continue
        if len(astock) >= 1 and astock not in skips:
            port[astock] = row['Cost Basis Per Share'] 

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
    return float(port[astock].strip("$"))

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

