import z
import buy
import statistics
from scipy import stats

# calculate vol percentile

def proc():
    check = ["BA", "IVV", "AMD"]
    volcdict = dict()
    volp = dict()
    for idx, astock in enumerate(stocks):
        if debug:
            print("astock : {}".format( astock ))
        try:
            avg = list()
            for i, row in enumerate(buy.getRows(astock, dates[-107])):
                if not i % 3:
                    continue
                try:
                    avg.append(int(row['Volume']))
                except:
                    break
            volcdict[astock] = round(statistics.median(avg))
        except Exception as e:
            continue

    vols =  list(volcdict.values())[::2]
    for astock in stocks:
        try:
            volp[astock] = round(stats.percentileofscore(vols, volcdict[astock]),2)
        except:
            pass
    if not debug:
        z.setp(volp, "volp", True)

if __name__ == '__main__':
    import args
    proc()

