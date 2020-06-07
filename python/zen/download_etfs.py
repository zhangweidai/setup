from collections import defaultdict
from shutil import copyfile
import os
import time
import urllib.request
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
                z.trace(e)
                with open(etf,"w") as f:
                    f.writelines(lines)

alls = set()
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

def doit():
    global alls, company, etfdict

    etfpath = z.getPath("pkl/etfdict.pkl")
    try:
        copyfile(etfpath, z.getPath("pkl/etfdict_back.pkl"))
    except:
        pass

    dels = z.getp("deletes")
    for i,etf in enumerate(z.getEtfList(forEtfs=True)):
        print("i: {}".format( i))
        try:
            code = getCode(i, etf)
        except Exception as e:
            print ("problem with download")
            z.trace(e)
            continue

        print("code : {}".format( code ))
        addy = 'https://www.ishares.com/us/products/{}'\
               '/{}.ajax?fileType=csv&fileName'\
               '={}_holdings&dataType=fund'.format(codes[i], code, etf)
    
        print(addy)
        with urllib.request.urlopen(addy) as url:
            lines = url.read().decode('utf-8').split("\n")
        cleanLines(lines, etf, dels)
        time.sleep(3)

    z.setp(alls, "alls")
    z.setp(company, "company")
    z.setp(etfdict, "etfdict")

def getCsvsFiles():
    holds = []
    path = z.getPath('holdings/{}.csv'.format())
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

def diffISharesEtfs():
    latest = z.getp("etfdict")
    previous = z.getp("etfdict_back")
    dels = z.getp("deletes")
    if not latest or not previous:
        print ("missing data")
        return
    allthesame = True
    changes = dict()
    for key,list1 in latest.items():
        list2 = previous[key]
        print("\nkey: {}".format( key))
        s1 = set(list1).difference(list2)
        s2 = set(list2).difference(list1)

#        print("Added:", (set(list1).difference(list2)))
#        print("Removed:", (set(list2).difference(list1)))
        changes["{}_added".format(key)] = s1
        changes["{}_removed".format(key)] = s2
    print("changes: {}".format( changes))
    z.setp(changes, "etfchanges")

if __name__ == '__main__':
#    doit()
    diffISharesEtfs()
