import z
import os
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
    for apath in getFiles(astock, date):

        started = False
        try:
            for row in csv.DictReader(open(apath)):
                if date_year not in apath:
                    yield row
                elif started:
                    yield row
                elif row['Date'] == date:
                    started = True
                    yield row
                else:
                    daysplits = date.split("-")
                    cdate = row['Date']
                    cdaysplits = cdate.split("-")

                    bar = int(daysplits[1])
                    cbar = int(cdaysplits[1])
                    if bar == cbar:
                        bar = int(daysplits[2])
                        cbar = int(cdaysplits[2])
                        if cbar >= bar:
                            started = True
                            yield row

        except Exception as e:
            pass

def getRowsRange(astock, count = 20000, date = "2000"):
    date_year = date.split("-")[0]
    total = 0
    for apath in getFiles(astock, date):

        started = False
        try:
            for row in csv.DictReader(open(apath)):
                ok = False
                if date_year not in apath:
                    ok = True
                elif started:
                    ok = True
                elif row['Date'] == date:
                    started = True
                    ok = True
                else:
                    daysplits = date.split("-")
                    cdate = row['Date']
                    cdaysplits = cdate.split("-")

                    bar = int(daysplits[1])
                    cbar = int(cdaysplits[1])
                    if bar == cbar:
                        bar = int(daysplits[2])
                        cbar = int(cdaysplits[2])
                        if cbar >= bar:
                            started = True
                            ok = True
                            yield row

                if ok:
                    total += 1
                    if total < count:
                        yield row


        except Exception as e:
            pass
