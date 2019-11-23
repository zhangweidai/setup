import util
import os
import csv
import z
import statistics

def getAverageReturn(values, year_length = 12, consideration_length = 1):
    count = len(values)
    size = consideration_length * year_length 
    end = size * -1
    consideration = values[:end]
    country_vals = list()
    for i, value in enumerate(consideration):
        consideration2 = values[i:i+size]

        duration_vals = list()
        endvalue = consideration2[-1]
        running = 0
        vals = list()

        for x, value in enumerate(consideration2[:-1]):
            useme = value[1]
            duration_vals.append(round(endvalue[1]/useme,3))
            vals.append(useme)

        country_vals.append(round(statistics.mean(duration_vals),3))
    return country_vals

def process(path):
    values = []
    print("path: {}".format( path))
    for row in csv.DictReader(open(path)):
        lis = list(row.values())
        values.append((lis[0],round(float(lis[1]),3)))

    for years in range(1,11):
        try:
            vals = getAverageReturn(values, consideration_length = years)
            mean = round(statistics.mean(vals),3)
            median = round(statistics.median(vals),3)
            low = min(vals)
            high = max(vals)
            print("years:{} mean:{} median: {} low:{} high:{}".format( years, mean, median, low, high))
        except:
            continue

def getFiles(where, his_idx = None):
    import fnmatch
    holds = []
    parentdir = util.getPath(where)
    listOfFiles = os.listdir(parentdir)
    for entry in listOfFiles:  
        path = os.path.join(parentdir, entry)
        process(path)

getFiles("countries")
#(process("/home/zoe/setup/python/zen/../zen_dump/countries/usa.csv"))
