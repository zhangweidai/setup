import z
import buy
import statistics
from scipy import stats
import args

# calculate vol percentile

def proc(istocks = None):

    mstocks = istocks if istocks else stocks
    try:
        days_ago = dates[-50]
    except:
        dates = z.getp("dates")
        days_ago = dates[-50]

    volcdict = dict()
    volp = dict()
    for idx, astock in enumerate(mstocks):
        if args.args.debug:
            print("astock : {}".format( astock ))
        try:
            avg = list()
            for i, row in enumerate(buy.getRows(astock, dates[-50])):
                if not i % 3:
                    continue
                try:
                    avg.append(int(row['Volume']))
                except Exception as e:
                    avg.append(int(float(row['Volume'])))

            volcdict[astock] = round(statistics.median(avg))
        except Exception as e:
            continue

    vols =  list(volcdict.values())[::2]
    for astock in mstocks:
        try:
            volp[astock] = round(stats.percentileofscore(vols, volcdict[astock]),2)
        except Exception as e:
            z.trace(e)
            pass
    if not args.args.debug:
        z.setp(volp, "volp")
    return volp

if __name__ == '__main__':
    proc()

