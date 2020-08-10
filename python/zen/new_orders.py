import os
import z
import buy
import csv

#Order Status
#08/08/2020 02:47:24 PM ET
#
#"Symbol","Status","Order Type","Trade Description","TIF","Account","Order Time","Cancel Date"
#"RH","OPEN","Limit at $269.00","Buy 2 Limit at $269.00  ","GTC","INDIVIDUAL - TOD (Z03895009)","01:00:52 PM
#08/04/2020","04:00:00 PM
#08/25/2020"
#"MTCH","OPEN","Limit at $95.00","Buy 4 Limit at $95.00  ","GTC","INDIVIDUAL - TOD (Z03895009)","10:53:07 PM
#08/01/2020","04:00:00 PM
#08/31/2020"
#"KNSL","OPEN","Limit at $190.00","Buy 3 Limit at $190.00  ","GTC","INDIVIDUAL - TOD (Z03895009)","06:23:00 PM
#08/01/2020","04:00:00 PM
#08/31/2020"

from datetime import date
from collections import defaultdict
gdates = z.getp("dates")
def process():
    parentdir = "/mnt/c/Users/Zoe/Documents"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"

    listOfFiles = os.listdir(parentdir)
    dic = dict()
    stocks = list()

    combined = dict()
    buy_value = defaultdict(int)
    col_valus = defaultdict(str)
    saveem3 = defaultdict(int)
    orders = set()
    for entry in listOfFiles:  
        if not entry.endswith("csv"):
            continue
        if "order" not in entry:
            continue

        col_val = "t" if "tory" in entry else "p"

        fullpath = os.path.join(parentdir, entry)
        print("fullpath : {}".format( fullpath ))

        with open(fullpath, "r", errors='replace') as f:
            reader = csv.reader(f)
#            bar = f.readlines()
            cstock = None
            next(reader)
            next(reader)
            next(reader)
            next(reader)
            for row in enumerate(reader):
                bar = row[1]
                astock = bar[0]
                value = bar[3].split(" ")
                if not value[0] == 'Buy':
                    continue

                buyprice = float(value[4][1:].replace(',',""))
                count = float(value[1])
                value = buyprice * count
                try:
                    cdate = bar[-1].split('\n')[1]
                    print("{} {} cdate : {}".format( astock, value, cdate ))
                    cdate = cdate.split("/")
                    f_date = date(int(cdate[2]), int(cdate[0]), int(cdate[1]))
                    delta = f_date - date.today()
                    delta = str(delta).split(" ")[0]

                    buy_value[astock] += value
                    col_valus[astock] += "{}{}".format(col_val,delta)
                    saveem3[col_val] = value

                    combined[astock] = buyprice
                    orders.add(astock)

                except Exception as e:
                    z.trace(e)
                    pass
                continue

    for astock, buyprice in combined.items():
        combined[astock] = (buyprice, buy_value[astock], col_valus[astock])

#    z.setp(buy_value, "order_vals", True)
#    z.setp(col_valus, "order_keys", True)
    z.setp(combined, "combined", True)
    z.setp(orders, "orders")
    print("saveem3: {}".format( saveem3))

if __name__ == '__main__':
    process()
#    cost_basis = z.getp("cost_basis")
#    cost_basis = process()
#    last_price = z.getp("last_price")
#    first_date = cost_basis.keys()[0]
#    print("first_date : {}".format( first_date ))
#
#    ivv_dates = dict()
#    for i, row in enumerate(buy.getRows("IVV", first_date)):
#        cdate = row["Date"]
#        ivv_dates[cdate] = row["Close"]
#    print("ivv_dates: {}".format( ivv_dates))
#
#    last_ivv = row["Close"]
#    print("last_ivv : {}".format( last_ivv ))
#        
#    under_performed = SortedSet()
#    for date, values in cost_basis.items():
#        for value in values:
#            astock = value[0]
#            basis = value[2]
#            c_close = last_price[astock]
#            ivv_change = round(last_ivv/ivv_dates[date],3)
#            stock_change = round(c_close/basis,3)
#            if ivv_change > stock_change:
#                print("date: {} {} {} {}".format( date, astock, stock_change, ivv_change))
#                under_performed.add((round(stock_change - ivv_change, 4), astock))
#
#    z.setp(under_performed, "under_performed")
#    print("under_performed: {}".format( under_performed))
##
##    fig, ax = plt.subplots()
##    ax.cla()
##    ax.scatter(x,y)
##    plt.grid(color='black', linestyle='-', linewidth=0.5)
#    plt.rcParams['toolbar'] = 'None'
#    plt.show(block=True)
#    print("saveem: {}".format( saveem))
#            z.breaker(10, printme=False)
            

