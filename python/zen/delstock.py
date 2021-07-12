full = True
import math
import z
from sortedcontainers import SortedSet
import os
import rows
import buy
import statistics

def delstock(astock, update = False):

    if update:
        try:
            data = z.getp("div_mc_dict")
            del(data[astock])
            z.setp(data, "div_mc_dict")
        except:
            pass

    afile = z.getPath("historical/{}.csv".format(astock))
    if os.path.exists(afile):
        os.remove(afile)
    try:
        for afile in rows.getFiles(astock):
            if os.path.exists(afile):
                os.remove(afile)
                print("removed  : {}".format( afile ))
    except Exception as e:
        z.trace(e)
        print("1problem  : {}".format( afile ))
        pass

#    if update:
#        data = z.getp("listofstocks", real=True)
#        data.remove(astock)
#        z.setp(data, "listofstocks")

def cleanup(astock, date):
    tokens = date.split("-")
    year = tokens[0]
    try:
        cyear = False
        for afile in rows.getFiles(astock):
            if not os.path.exists(afile):
                continue

            if year in afile:
                cyear = True
                with open(afile, "r") as f:
                    lines = f.readlines()

                with open(afile, "w") as f:
                    started = False
                    for i,line in enumerate(lines):
                        if date in line:
                            started = True
                        if i == 0 or started:
                            f.write(line)

            if not cyear:
                os.remove(afile)
                print("deleted afile: {}".format( afile))

    except Exception as e:
        z.trace(e)
        print("1problem  : {}".format( afile ))
        pass

def batchdelete(stocks):
    data = z.getp("div_mc_dict")
    top95 = z.getp("top95")
    listof = z.getp("listofstocks", real=True)
    quick = z.getp("quick", real=True)

    for astock in stocks:
        try:
            del(data[astock])
        except:
            print("dell stock problem astock : {}".format( astock ))
            pass

        try:
            if astock in listof:
                print("removed from listofstocks : {}".format( astock ))
                listof.remove(astock)

            if astock in quick:
                print("removed from quick : {}".format( astock ))
                quick.remove(astock)

            if astock in top95:
                print("removed from top95 : {}".format( astock ))
                top95.remove(astock)
        except:
            print("del problem astock : {}".format( astock ))
            pass

        delstock(astock, update=False)

    z.setp(data, "div_mc_dict")
    z.setp(listof, "listofstocks")
    z.setp(quick, "quick")
    z.setp(top95, "top95")

if __name__ == '__main__':
    import args
#    import argparse
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--delete')
#    parser.add_argument('--updatestocks', default=False)
#    args = parser.parse_args()

    z.getp.cache_clear()
    top95 = z.getp("top95")
    data = z.getp("listofstocks", real=True)
    quick = z.getp("quick", real=True)

    for astock in stocks:
        delstock(astock, True)
        if astock in data:
            print("removed from listofstocks : {}".format( astock ))
            data.remove(astock)

        if astock in quick:
            print("removed from quick : {}".format( astock ))
            quick.remove(astock)

        if astock in top95:
            print("removed from top95 : {}".format( astock ))
            top95.remove(astock)

    z.setp(data, "listofstocks")
    z.setp(quick, "quick")
    z.setp(top95, "top95")
