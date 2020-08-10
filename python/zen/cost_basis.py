import os
import z
import buy

#"Symbol","Last","Chg","% Chg","Quantity","Purchase Price","Value","G/L","% G/L","Account","Earnings Date"
#"ABT","101.23","0","0.00","1","79.73","101.23","21.50","26.97","INDIVIDUAL - TOD (Z03895009)","10/14/2020"
#"ASSOCIATED LOTS","","","","",""
#"Quantity","Cost Basis/Share","Unrealized G/L","Unrealized % G/L","Date Acquired","Holding Period"
#"1","79.73","21.50","26.97","04/03/2019","Long"
#"ALLY","21.47","0","0.00","20","24.734","429.4","-65.28","-13.20","INDIVIDUAL - TOD (Z03895009)","10/14/2020"
#"ASSOCIATED LOTS","","","","",""
#"Quantity","Cost Basis/Share","Unrealized G/L","Unrealized % G/L","Date Acquired","Holding Period"
#"5","14.04","37.17","52.96","03/24/2020","Short"
#"15","28.30","-102.45","-24.13","02/19/2020","Short"
#"AMD","84.85","0","0.00","25","41.455","2121.25","1,084.87","104.68","INDIVIDUAL - TOD (Z03895009)","10/27/2020"
#"ASSOCIATED LOTS","","","","",""
#"Quantity","Cost Basis/Share","Unrealized G/L","Unrealized % G/L","Date Acquired","Holding Period"
#"25","41.46","1,084.87","104.68","11/19/2019","Short"

from collections import defaultdict
from sortedcontainers import SortedSet
gdates = z.getp("dates")
ports = defaultdict(int)
owned = defaultdict(str)

parentdir = "/mnt/c/Users/Zoe/Documents"
if not os.path.exists(parentdir):
    parentdir = "/mnt/c/Users/pzhang/Downloads"

def process():

    listOfFiles = os.listdir(parentdir)
    dic = dict()
    stocks = list()

    cost_dict = defaultdict(list)
    for entry in listOfFiles:  
        if not entry.endswith("csv"):
            continue
        if "port" not in entry:
            continue
#        if "adr" not in entry:
#            continue

        col_val = "T" if "tory" in entry else "P"
        fullpath = os.path.join(parentdir, entry)
        print("fullpath : {}".format( fullpath ))

        with open(fullpath, "r", errors='replace') as f:
            bar = f.readlines()

        cstock = None
        valueidx = 0
        for idx, aline in enumerate(bar):
            if idx <= 3:
                aline = aline.split('","')
                try:
                    valueidx = aline.index('Value')
                except:
                    pass
                continue
            aline = aline.split('","')
            first_arg = aline[0].replace('"', '')
            try:
                is_int = float(first_arg)
                cost_basis = float(aline[1].replace('"', '').replace(',',''))
                if cost_basis <= 0 or is_int < 1.0:
                    continue

                longp = "Long" in aline[-1]
                date = aline[4].replace('"', '').split("/")

                date = "{}-{}-{}".format(date[2],date[0],date[1])
                value = round(is_int * cost_basis,1)
                values = (cstock, value, cost_basis, longp, col_val, date)
                cost_dict[date].append(values)

            except Exception as e:
#                if cstock == "AMZN":
#                    print (z.trace(e))
#                    print("aline: {}".format( aline))
                if not first_arg == "Quantity" and not first_arg == "ASSOCIATED LOTS":
                    cstock = first_arg
                    try:
                        ports[cstock] += float(aline[valueidx])
                        owned[cstock] += col_val
                    except:
                        pass

    return cost_dict

import csv
van = defaultdict(float)
def processVan():
    parentdir = "/mnt/c/Users/Zoe/Downloads"
    fullpath = os.path.join(parentdir, "van.csv")
    with open(fullpath, "r", errors='replace') as f:
        reader = csv.DictReader(f)
        for row in enumerate(reader):
            row = row[1]
            astock = row["Symbol"]
            shares = row["Shares"]
            try:
                if " " in astock:
                    break
                val = float(shares)
                if val and "XX" not in astock:
                    van[astock] += val
            except:
                pass
    print("van: {}".format( van))

if __name__ == '__main__':
    ivv_better_value = 0
    based_on = 0
    processVan()
    last_price = z.getp("last_price")

    cost_dict = process()

    ivv_dates = dict()
    for i, row in enumerate(buy.getRows("IVV", gdates[-700])):
        cdate = row["Date"]
        ivv_dates[cdate] = float(row["Close"])

    last_ivv = float(row["Close"])
        
    under_performed = SortedSet()
    under_performed2 = SortedSet()
    for date, values in cost_dict.items():
        for value in values:
            astock = value[0]
            basis = value[2]
            try:
                c_close = last_price[astock]
                ivv_change = round(last_ivv / ivv_dates[date],3)
                stock_change = round(c_close/basis,3)
                if ivv_change > stock_change:
#                    print("date: {} {} {} {}".format( date, astock, stock_change, ivv_change))
                    change = round(stock_change - ivv_change, 4)
                    amount = round(change*value[1])
                    ivv_better_value += amount
                    based_on += value[1]
                    if amount <= -10:
                        under_performed.add((change , astock, amount, ivv_change, stock_change, value[1], value[4], value[5]))
                    if amount <= -50 and value[3]:
                        under_performed2.add((amount, (astock, value[4])))
            except:
                pass

    z.setp(under_performed, "under_performed")
    print("under_performed: {}".format( under_performed))
    z.setp(under_performed2, "under_performed2")
    print("\n\nunder_performed2: {}".format( under_performed2))

    for astock, owned_str in owned.items():
        owned[astock] = (owned_str, round(ports[astock]))

    for astock, number in van.items():
        
        val = round(last_price[astock] * number)
        owned_str, cvalue = owned.get(astock, ("", 0))
        owned_str += "V"
        owned[astock] = (owned_str, round(cvalue + val))

    z.setp(owned, "owned")

    for be in under_performed:
        print("be : {}".format( be ))
    print("ivv_better_value : {}".format( ivv_better_value ))
    print("based_on : {}".format( based_on ))
#    under_performed.add((change , astock, amount, ivv_change, stock_change, value[1]))
#
#    fig, ax = plt.subplots()
#    ax.cla()
#    ax.scatter(x,y)
#    plt.grid(color='black', linestyle='-', linewidth=0.5)
#    plt.rcParams['toolbar'] = 'None'
#    plt.show(block=True)
#    print("saveem: {}".format( saveem))
#            z.breaker(10, printme=False)
            

