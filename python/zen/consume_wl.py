import os
import z
import fnmatch
import csv
from collections import defaultdict
from sortedcontainers import SortedSet
import buy

# take wlp dumps and capture historical fundamentals

def doit():
    parentdir = "/mnt/c/Users/Zoe/Documents/wlp_dump2"
    pattern = "*.txt"  
    listOfFiles = os.listdir(parentdir)
    wlp_dict = defaultdict(dict)
    wlp_sorted_mc = defaultdict(SortedSet)
    newlist = list()
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            path = parentdir + "/" + entry
            astock = os.path.basename(os.path.splitext(entry)[0])
            for row in csv.DictReader(open(path)):
                mc = float(row['MC'])
                dr = float(row['DebtRatio'])
                out = float(row['out'])
                ebit = float(row['ebit'])
                wlp_dict[astock][row['Date']] = mc, dr, out, ebit
                wlp_sorted_mc[row['Date']].add((mc, astock))
                #print("row : {}".format( row ))
                #z.breaker(10)
    #    for row in csv.DictReader(open(path)):
    #print("newlist: \n{}".format( " ".join(newlist)))
    
    z.setp(wlp_dict, "wlp_dict")
    z.setp(wlp_sorted_mc, "wlp_sorted_mc")
    dates = z.getp("dates")
    buy.sortedSetToRankDict("latestmc", wlp_sorted_mc[dates[-1]], reverse=True)
    buy.sortedSetToRankDict("1ymc", wlp_sorted_mc[dates[-252]], reverse=True)
    buy.sortedSetToRankDict("2ymc", wlp_sorted_mc[dates[-252*2]], reverse=True)
    buy.sortedSetToRankDict("3ymc", wlp_sorted_mc[dates[-252*3]], reverse=True)

if __name__ == '__main__':
    doit()
#    wlp_sorted_mc = z.getp("wlp_sorted_mc")
#    def sortedSetToRankDict(saveas, sset, reverse=False, printdata = False):

