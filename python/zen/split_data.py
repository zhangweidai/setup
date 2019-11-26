import csv
import os
import z

def split():
    path = z.getPath("historical")
    listOfFiles = os.listdir(path)
    stocks = list()
    for entry in listOfFiles:  
#        cpath = "{}/{}".format(path, entry)
        astock = os.path.splitext(entry)[0]
        stocks.append(astock)
    z.setp(stocks, "listofstocks")
#        process(astock, cpath)
#        for row in csv.DictReader(open(cpath)):
#            pass
#        getPrice.latest[astock] = ( float(row['Open']), float(row[closekey]) )

def process(astock, path):
    print("astock : {}".format( astock ))
    reader = csv.DictReader(open(path))
    cyear = None
            
    for row in reader:
        date = row['Date']
        year = date.split("-")[0]
        if cyear != year:
            tpath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
            writer = csv.DictWriter(open(tpath, "w"), fieldnames=reader.fieldnames)
            writer.writeheader()
            cyear = year
        writer.writerow(row)

def num_of_days_checks():
    stocks = z.getp("listofstocks")
    for astock in stocks:
        path = z.getCsvPath(astock)
        i = 0
        for row in csv.DictReader(open(path)):
            i += 1
        if i < 218:
            print("astock: {} {} ".format( astock, i))
if __name__ == '__main__':
#    split()
    num_of_days_checks()
#    path = z.getPath("historical/KO.csv")
#    process("KO", path)
