import os
import z

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
gdates = z.getp("dates")
def process():
    parentdir = "/mnt/c/Users/Zoe/Documents"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"

    listOfFiles = os.listdir(parentdir)
#    bar = SortedSet()
    dic = dict()
    stocks = list()

    saveem = defaultdict(list)
    for entry in listOfFiles:  
        if not entry.endswith("csv"):
            continue
        if "ports" not in entry:
            continue
#        if "adr" not in entry:
#            continue
        fullpath = os.path.join(parentdir, entry)
        print("fullpath : {}".format( fullpath ))

        with open(fullpath, "r", errors='replace') as f:
            bar = f.readlines()

        cstock = None
        for idx, aline in enumerate(bar):
            if idx <= 3:
                continue
            aline = aline.split('","')
            first_arg = aline[0].replace('"', '')
            try:
                is_int = float(first_arg)
                cost_basis = float(aline[1].replace('"', '').replace(',',''))
                if cost_basis <= 0:
                    continue
                date = aline[4].replace('"', '').split("/")
                date = "{}-{}-{}".format(date[2],date[0],date[1])
                value = round(is_int * cost_basis,1)
                values = (cstock, value)
                saveem[date].append(values)

            except Exception as e:
#                if cstock == "AMZN":
#                    print (z.trace(e))
#                    print("aline: {}".format( aline))
                if not first_arg == "Quantity" and not first_arg == "ASSOCIATED LOTS":
                    cstock = first_arg
    z.setp(saveem, "cost_basis", True)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    cost_basis = z.getp("cost_basis")
#    y = [3, 3]
#    x = [
#        "03-04-1993", 
#        "03-03-1993", 
#    ]

    first_date = cost_basis.keys()[0]

    ivv_dates = dict()
    for i, row in enumerate(buy.getRows("IVV", first_date)):
        cdate = row["Date"]
        ivv_dates[cdate] = row["Close"]
    print("ivv_dates: {}".format( ivv_dates))
        
    for date, values in cost_basis.items():

#
#    fig, ax = plt.subplots()
#    ax.cla()
#    ax.scatter(x,y)
#    plt.grid(color='black', linestyle='-', linewidth=0.5)
#    plt.rcParams['toolbar'] = 'None'
#    plt.show(block=True)
#    print("saveem: {}".format( saveem))
#            z.breaker(10, printme=False)
            

