full = True
import args
import os
import regen_stock
year = "2020"
import z
import download_batch
if __name__ == '__main__':

    stocks = z.getp("listofstocks")

    for astock in stocks:
        apath = z.getPath("split/{}/{}_{}.csv".format(astock[0], astock, year))
        if not os.path.exists(apath):
            download_batch.process(astock)

#    stocks.remove("CELG")
#    z.setp(stocks, "listofstocks")
