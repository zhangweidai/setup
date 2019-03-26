import urllib.request
import util
import os
import fnmatch

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

def getCode():
    addy = 'https://www.ishares.com/us/products/239724/ishares-core-sp-total-us-stock-market-etf'
    with urllib.request.urlopen(addy) as url:
        lines = url.read().decode('utf-8').split(" ")
    for aline in lines:
        if "csv" in aline:
            return (getSymbol(aline))

etfs = ["IVV", "IWB", "IUSG", "USMV", "ITOT"]

def doit():
    code = getCode()
    for etf in etfs:
        addy = 'https://www.ishares.com/us/products/239724/ishares-core'\
               '-sp-total-us-stock-market-etf/{}.ajax?fileType=csv&fileName'\
               '={}_holdings&dataType=fund'.format(code, etf)
    
        with urllib.request.urlopen(addy) as url:
            lines = url.read().decode('utf-8')
    
        path = util.getPath("temp/{}".format(etf))
        with open(path,"w") as f:
            f.writelines(lines)

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

alls = set()
from collections import defaultdict
etfdict = defaultdict(set)
company = dict()

def cleanFiles():
    for afile in getCsvsFiles():
        etf = os.path.basename(afile)
        with open(afile, "r") as f:
            lines = f.readlines()
        lines[:] = [x for x in lines if determine(x)]
        for aline in lines:
            aline = aline.replace('"', "")
            tokens = aline.split(",")

            etfdict[etf].add(tokens[0])
            alls.add(tokens[0])
            company[tokens[0]] = tokens[1]
#cleanFiles()
#util.setp(alls, "alletfs")
#util.setp(company, "company")
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
