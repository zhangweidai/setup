import os
import z
import fnmatch
import csv
from collections import defaultdict
from sortedcontainers import SortedSet
import buy
import os
from scipy import stats
import numpy as np
#
#x = np.random.random(10)
#y = np.random.random(10)
#slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
#print("r_value: {}".format( r_value))
#print("slope: {}".format( slope))
#
#x = [60 - i for i in range(30)]
#y = [i for i in range(30)]
#slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
#print("r_value: {}".format( r_value))
#print("slope: {}".format( slope))
#
#exit()

# take wlp dumps and capture historical fundamentals

def doit(allowed = []):
    print("allowed : {}".format( allowed ))
    dates = z.getp("dates")
    yearago = dates[-252]
    parentdir = "/mnt/c/Users/Zoe/Documents/wlp_dump2"
    pattern = "*.txt"  
    listOfFiles = os.listdir(parentdir)
    wlp_dict = defaultdict(dict)
    wlp_sorted_mc = defaultdict(SortedSet)
    sorted_mc = SortedSet()
    newlist = list()
    wlp_dict = defaultdict(dict)
    wlp_list = defaultdict(dict)
    os_change = dict()
    wlp_lasts = dict()
    latest_mc = dict()
    yearagomc = dict()
    single = bool(allowed)
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            path = parentdir + "/" + entry
            astock = os.path.basename(os.path.splitext(entry)[0])
            if allowed and astock not in allowed:
                continue

            lastdr = None
            lastos = None
            lastebit = None
            l1 = list()
            l2 = list()
            l3 = list()
#            if astock != "PSA":
#                continue
            for row in csv.DictReader(open(path)):
                mc = float(row['MC'])
                dr = float(row['DebtRatio'])
                date = row['Date']
                out = float(row['out'])
                ebit = float(row['ebit'])

                if date == yearago:
                    yearagomc[astock] = mc
#                if lastdr != dr:
#                    lastdr = dr
#                    l1.append(dr)

                if lastos != out:
                    lastos = out
                    l2.append(out)

#                if lastebit != ebit:
#                    lastebit = ebit
#                    l3.append(ebit)

#                wlp_dict[astock][date] = mc, dr, out, ebit
#                wlp_sorted_mc[date].add((mc, astock))

#            wlp_list[astock]['DebtRatio'] = l1
#            wlp_list[astock]['OS'] = l2

            if single:
                print("l2: {}".format( l2))

            r_value = "NA"
            slope = "NA"
            latest_mc[astock] = mc
            sorted_mc.add((mc, astock))
#            print("l2: {}".format( len(l2)))
#            print("ebit: {}".format( ebit))
#            print("dr: {}".format( dr))
            if len(l2) > 8:
                l2 = l2[-8:]
                y = [ i for i in range(len(l2)) ]
                try:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(l2, y)
                except:
                    pass
                r_value = round(r_value * r_value,2)
                slope = round(slope,2)
                if single:
                    print("r_value : {}".format( r_value ))
                    print("slope : {}".format( slope ))
            wlp_lasts[astock] = dr, ebit, r_value, slope

#                print("r_value: {}".format( r_value))
#                print("slope: {}".format( slope))

    z.setp(latest_mc, "latest_mc", True)
    if not allowed:
        z.setp(yearagomc, "yearagomc", True)
        z.setp(wlp_lasts, "wlp_lasts", True)
#    z.setp(wlp_list, "wlp_list")
#    z.setp(os_change, "os_change")
#    z.setp(buy.getSorted("os_sorted"), "os_sorted", True)

#    z.setp(wlp_sorted_mc, "wlp_sorted_mc")
#    dates = z.getp("dates")
    buy.sortedSetToRankDict("latestmc", sorted_mc, reverse=True)
    bar  = z.getp("latestmc")
    print("bar  : {}".format( bar  ))
#    buy.sortedSetToRankDict("1ymc", wlp_sorted_mc[dates[-252]], reverse=True)
#    buy.sortedSetToRankDict("2ymc", wlp_sorted_mc[dates[-252*2]], reverse=True)
#    buy.sortedSetToRankDict("3ymc", wlp_sorted_mc[dates[-252*3]], reverse=True)

if __name__ == '__main__':
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('helpers', type=str, nargs='?', default = [])
    args = parser.parse_args()
    stocks = []
    if args.helpers:
        stocks = [args.helpers.upper()]

    start_time = time.time()
    doit(stocks)
    elapsed_time = time.time() - start_time
    print("elapsed_time : {}".format( elapsed_time ))
#    wlp_sorted_mc = z.getp("wlp_sorted_mc")
#    def sortedSetToRankDict(saveas, sset, reverse=False, printdata = False):

