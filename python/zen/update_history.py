import util
import update_csv

getStocks.totalOverride = True
stocks = util.getStocks()
for astock in stocks:
    try:
        update_csv.updateCsv(astock, yahoo_date)
    except:
        print ("problem with {}".format(astock))
        continue
    break


