import urllib.request
import util
import os
import fnmatch
import z

def savefile():
    addy = 'https://www.ishares.com/us/products/239724/ishares-core-sp-total-us-stock-market-etf'
    with urllib.request.urlopen(addy) as url:
        lines = url.read().decode('utf-8').split(" ")
        with open("mytest","w") as f:
            f.writelines(lines)

def getSymbol(text):
    import re
    m = re.search(r"\/(.*?)\.ajax", text)
    if m:
        return m.group(1).split("/")[-1]
    return None

def getCode(i, etf):
    addy = 'https://www.ishares.com/us/products/{}'.format(codes[i])
    with urllib.request.urlopen(addy) as url:
        lines = url.read().decode('utf-8').split(" ")
    for aline in lines:
        if "csv" in aline:
            try:
                return (getSymbol(aline))
            except Exception as e:
                print ("download")
                print (str(e))
                with open(etf,"w") as f:
                    f.writelines(lines)

alls = set()
from collections import defaultdict
etfdict = defaultdict(set)
company = dict()
codes = [
    "239724/ishares-core-sp-total-us-stock-market-etf",
    "239763/ishares-core-sp-midcap-etf",
    "239774/ishares-core-sp-smallcap-etf",
    "239726/ishares-core-sp-500-etf", 
    "239707/ishares-russell-1000-etf",
    "239713/ishares-core-sp-us-growth-etf",
    "239695/ishares-msci-usa-minimum-volatility-etf"
]

import time
def doit():
    global alls, company, etfdict

    alls = util.getp("alletfs")
    company = util.getp("company")
    etfdict = util.getp("etfdict")
#
    dels = util.getp("deletes")
    for i,etf in enumerate(z.getEtfList()):
        print("i: {}".format( i))
        try:
            code = getCode(i, etf)
        except Exception as e:
            print ("download")
            print (str(e))
            continue

        print("code : {}".format( code ))
        addy = 'https://www.ishares.com/us/products/{}'\
               '/{}.ajax?fileType=csv&fileName'\
               '={}_holdings&dataType=fund'.format(codes[i], code, etf)
    
        print(addy)
        with urllib.request.urlopen(addy) as url:
            lines = url.read().decode('utf-8').split("\n")
#        print(lines)
    
#        path = util.getPath("temp/{}".format(etf))
#        with open(path,"w") as f:
#            f.writelines(lines)
        cleanLines(lines, etf, dels)
        time.sleep(3)

    util.setp(alls, "alls")
    util.setp(company, "company")
    util.setp(etfdict, "etfdict")

def getCsvsFiles():
    holds = []
    path = util.getPath('temp')
    listOfFiles = os.listdir(path)
    for entry in listOfFiles:  
        holds.append("{}/{}".format(path,entry))
    return holds

def determine(aline):
    if "NASDAQ" in aline or "New York Stock Exchange" in aline:
        return True
    return False


def cleanLines(lines, etf, cleans):
    global etfdict, alls, company
    lines[:] = [x for x in lines if determine(x)]
    for aline in lines:
        aline = aline.replace('"', "")
        tokens = aline.split(",")

        astock = tokens[0]
        if astock in cleans:
            print("skipping astock : {}".format( astock))
            continue

        etfdict[etf].add(astock)
        alls.add(astock)
        company[astock] = [tokens[1], tokens[3]]

def cleanFiles():
    for afile in getCsvsFiles():
        etf = os.path.basename(afile)
        with open(afile, "r") as f:
            lines = f.readlines()
        cleanLines(lines)
doit()
#cleanFiles()
#huh = util.getp("alletfs")

#with open("mytest","w") as f:
#    f.writelines(getweb())
#lines = []
#with open("mytest","r") as f:
#    lines = f.readlines()
#for aline in lines:
#    if "ITOT" in aline:
#        print("aline : {}".format( aline ))

#print(len(html))
