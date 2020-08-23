import z
import math
import csv
from collections import defaultdict
import table_print
import statistics
import os
from sortedcontainers import SortedSet
from rows import *
from scipy import stats
import args
import buy

#table_print.accurate = 2

# mc 30.00B to 1.54T
# mc 7.5B to 30.00B 
# mc 2.7B to 7.5B
# mc 0 to 2.7B 

cols = ["last",
        "target",
        ("md", "%"),
        ("md1", "%"),
        ("md2", "%"),
        ("mg", "%"),
        "gddif",
        ("dl", "%"),
        "mcp",
        ("chg1", "%"),
        "chg1p",
        ("chg5", "%"),
        ("chg30", "%"),
        "chg30p",
        ("y1u"),
        ("ivvb"),
        ("ly", "%"),
        ("l2y", "%"),
        ("wc", "%"),
        ("bc", "%"),
        ("avg", "%"),
        ("avg8", "%"),
        ("dfh1y", "%"),
        ("gfl1y", "%"),
        "volp",
        ("m30c", "%"),
        ("w30", "%"),
        "revmcp",
        "div",
        "bta" ]

tory = z.getp("tory")
mine = z.getp("mine")

def single(astock):

    mydic = z.getpp(astock)
    values = [("name", astock)]

    for col in cols:
        if type(col) is tuple:
            colname = col[0]
            values.append((colname, mydic[colname], col[1]))
        else:
            values.append((col, mydic[col]))

    if args.args.live:
        try:
            live_price = z.getLiveData(astock, key = "price")
            liveChange = live_price / mydic["last"]
            values.append(("live", liveChange, "%"))
        except:
            pass

    try:
        loc, portvalue = buy.getFrom("owned", astock)
    except:
        where = ""
        portvalue = ""
        loc = ""
    values.append(("owned", portvalue))

#    owned = buy.portFolioValue(astock)
#    values.append(("owned", owned))

#    if owned:
#        loc += "P" if astock in mine else ""
#        loc += "T" if astock in tory else ""

    try:
#        combined[astock] = (buyprice, buy_value[astock], col_valus[astock])
        buyprice, buy_value, loct = buy.getFrom("combined", astock)
        loc = "{}{}".format(loc,loct)
#        order = buy.getFrom("orders", astock)[0]
#        order,value = order[1], round(order[0])
        ochg = buyprice/mydic["last"]
        values.insert(3, ("ochg", ochg, "%"))
        values.insert(4, ("value", buy_value))

    except Exception as e:
        ochg = ""
        value = "NA"
        values.insert(3, ("ochg", ochg, "%"))
        values.insert(4, ("value", value))

#    loc = ""
#    if ochg:
#        try:
#            loc = "t" if astock in z.getp("torys") else "p"
##        except:
#            pass
#
#
    values.append(("location", loc))

    table_print.store(values)

if __name__ == '__main__':

    print("stocks: {}".format( stocks))
    if not args.args.mode:
        for astock in stocks:
            try:
                single(astock)
            except Exception as e:
                z.trace(e)
    else:
        mcdic = z.getp("latestmc")
        mcs = list(mcdic.keys())
        idx = 0
        end = idx + 50
        for astock in mcs[idx:end]:
            single(astock)


    table_print.initiate()
