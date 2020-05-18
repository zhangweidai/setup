import z
import os
import csv
from collections import defaultdict

def getFiles():
    import fnmatch
    parentdir = "/mnt/c/Users/Zoe/Downloads/csvs"
    listOfFiles = os.listdir(parentdir)
    files = []
    for entry in listOfFiles:  
        if ".csv" not in entry:
            continue
        fullpath = "{}/{}".format(parentdir, entry)
        files.append(fullpath)
    return files

files = getFiles()
#files = ["/mnt/c/Users/Zoe/Downloads/csvs/12_19_tory.csv"]
import rows
dic = dict()
vooclist = list()
avgvoo = None
def getvoochanges():
    global dic, vooclist
    cdate = None
    cmonth = None
    beginPrice = None
    beginDate = None
    last = None
    for row in rows.getRows("VOO", date = "2018"):
        cdate = row['Date']
        parts = cdate.split("-")
        cc = float(row['Close'])

        if not cmonth == parts[1]:
            if beginPrice:
                change = round(last[0]/ beginPrice,3)
                vooclist.append(change)
                tokens = last[1].split("-")
                key = "{}{}".format(int(tokens[0])-2000, int(tokens[1]))
                dic[key] = change
            cmonth = parts[1]
            beginPrice = float(row["Open"])
            beginDate = cdate
        last = cc, cdate


getvoochanges()
begins = defaultdict(int)
changes = defaultdict(int)
for afile in files:
    mapping = None

    tokens = os.path.splitext(os.path.basename(afile))[0].split("_")
    key = "{}{}".format(tokens[1], tokens[0])

    for row in csv.DictReader(open(afile)):
        acc = row['']
        if not acc:
            break
        values = row[None]
        try:
            begin = float(values[0])
            changeV = float(values[1])
        except:
            continue

        begins[key] += begin
        changes[key] += changeV

print("begins: {}".format( begins))
avglist = list()
voowins = list()
for key in begins.keys():
    begin = begins[key]
    changeV = changes[key]
    change = round((begin + changeV)/begin,3)
    voo = dic[key]
    voowins.append(1 if dic[key] > change else 0)
    avglist.append(change)
    print("\nkey : {} \nvoo {} change {} begin {}\n".format( key, voo, change, begin ))


voowins2 = round(sum(voowins)/len(voowins),3)
print("voowins2 : {}".format( voowins2 ))
myavg = round(sum(avglist)/len(avglist),3)
print("myavg : {}".format( myavg ))

avgvoo = round(sum(vooclist)/len(vooclist),3)
print("avgvoo : {}".format( avgvoo ))
