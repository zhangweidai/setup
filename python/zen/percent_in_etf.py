# Import pandas
import os
#"Account Name/Number","Symbol","Description","Quantity","Last Price","Last Price Change","Current Value","Today's Gain/Loss Dollar","Today's Gain/Loss Percent","Total Gain/Loss Dollar","Total Gain/Loss Percent","Cost Basis Per Share","Cost Basis Total","Type"

import csv
     
import os
def getLatestFidelityCsv():
    import fnmatch
    parentdir = "/mnt/c/Users/Zoe/Downloads"
    if not os.path.exists(parentdir):
        parentdir = "/mnt/c/Users/pzhang/Downloads"

    listOfFiles = os.listdir(parentdir)
    newest = 0
    cfile = None
    for entry in listOfFiles:  
        if "Portfolio" not in entry:
            continue
        if ".csv" not in entry:
            continue
        fullpath = "{}/{}".format(parentdir, entry)
        tim = os.path.getmtime(fullpath)
        if tim > newest:
            newest = tim
            cfile = fullpath

    print("fidelity file: {}".format( cfile))
    os.system("chmod 777 {}".format(cfile) )
    return cfile

    
if __name__ == '__main__':
    currentValue = 0
    for row in csv.DictReader(open(getLatestFidelityCsv())):
        astock = row['Description'] 
        try:
            if " ETF" not in astock:
                continue
        except:
            continue
        astock = row['Symbol'] 
        value = float(row['Current Value'][1:-1])
        print("{} : {:>5}".format( astock, value ))
        currentValue += value
    print("currentValue : {}".format( currentValue ))

#    vals = fidelity(forselling)
#    print("vals : {}".format( vals ))
#    print("vals : {}".format( z.percentage(vals[0])))
#    print("port: {}".format(port))
#    
#    port = dict()
#    fidelity(forselling=True, updating=True)
#    print("port: {}".format(port))
#    
#    port = dict()
#    fidelity(forselling=True)
#    print("port: {}".format(port))
    
