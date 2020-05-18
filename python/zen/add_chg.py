import z
import os
import datetime
import csv

def getYears(date):
    away_year = int(date.split("-")[0])
    while int(away_year) != z.YEAR:
        yield away_year
        away_year += 1
    yield away_year

def getFiles(astock, date = "2000"):
    for year in getYears(date):
        yield z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))

def getRows(astock, date = "2000"):
    date_year = date.split("-")[0]
    prev_c = None
    for apath in getFiles(astock, date):

        try:
            t = os.path.getmtime(apath)
        except:
            continue

        csvdate = datetime.datetime.fromtimestamp(t)
        csvday = csvdate.day
        csvmonth = csvdate.month
        ttoday = datetime.date.today().day
        tmonth = datetime.date.today().month

        if csvday >= ttoday and tmonth == csvmonth:
            missed = 0
            continue

        try:
            with open(apath, "r") as f:
                lines = f.readlines()
        except:
            continue
        with open(apath, "w") as f:
            for i,aline in enumerate(lines):
                if i == 0:
                    f.write("{},{}\n".format(aline.rstrip(), "Chg"))
                else:
                    tokens = aline.split(",")
                    cclose = float(tokens[5])
                    try:
                        chg = round(prev_c / cclose, 3)
                    except Exception as e:
                        chg = 1
                    f.write("{},{}\n".format(aline.rstrip(), chg))
                    prev_c = cclose

stocks = z.getp("listofstocks")
for idx, astock in enumerate(stocks):
    if not idx % 100:
        print("idx: {}".format( idx))
    getRows(astock)

