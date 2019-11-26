import csv
import os
import z

def split():
    path = z.getPath("historical")
    listOfFiles = os.listdir(path)
    for entry in listOfFiles:  
        cpath = "{}/{}".format(path, entry)
        for row in csv.DictReader(open(cpath)):
            pass
        astock = os.path.splitext(entry)[0]
        getPrice.latest[astock] = ( float(row['Open']), float(row[closekey]) )

def process(path):
    astock = os.path.splitext(path)[0]
    print("astock : {}".format( astock ))
    tpath = z.getPath("split/{}.csv".format(astock))
    reader = csv.DictReader(open(path))
    bar = csv.DictWriter(open(tpath, "w"), fieldnames=reader.fieldnames)
            
    for row in reader:
        bar.writerow(row)
        date = row['Date']
        print("date : {}".format( date ))
        print("row : {}".format( row ))
        year = date.split("-")[0]
        z.breaker(4)
        pass

if __name__ == '__main__':
#    split()
    path = z.getPath("historical/KO.csv")
    process(path)
