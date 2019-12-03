import csv
import os
import z
import update_history

def setlistofstocks():
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

#    problems = z.getp("problems")
    problems = []
    for astock in problems:
        if astock == "BRKB":
            continue
        df = update_history.getDataFromYahoo(astock, "2013-01-02")
        if df is None:
            print("astock : {}".format( astock ))
            continue

        path = z.getPath("historical/{}.csv".format(astock))
        with open(path, "a") as f:
            for i,idx in enumerate(df.index):
                if i == 0:
                    f.write("Date,Open,High,Low,Close,Adj Close,Volume\n")
                cdate = str(idx.to_pydatetime()).split(" ")[0]
                opend = df.at[idx, "Open"]
                high = df.at[idx, "High"]
                low = df.at[idx, "Low"]
                closed = df.at[idx, "Close"]
                adj = df.at[idx, "Adj Close"]
                vol = df.at[idx, "Volume"]
                added = True
                f.write("{},{},{},{},{},{},{}\n".format(cdate, opend, high, low, closed, adj, vol))
        print("path : {}".format( path ))
        process(astock, path)

    setlistofstocks()
    import prob_down_5_years
    prob_down_5_years.prob()

    import gained_discount
    gained_discount.dosomething()
    gained_discount.genUlt()


#    num_of_days_checks()
#    path = z.getPath("historical/KO.csv")
#    process("KO", path)
