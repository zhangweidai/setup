import wget
import z
import zen
import os
import portfolio

def metrics(astock):
    path = z.getPath("metrics/{}.xlsx".format(astock))
    if os.path.exists(path):
        return path
    print ("trying to get {}\n".format(astock))
    url = 'https://stockrow.com/api/companies/{}/financials.xlsx?dimension=MRQ&section=Metrics&sort=desc'.format(astock)
    wget.download(url, path)


if __name__ == '__main__':
    stocks = z.getp("etfdict")['IVV']
#    stocks = portfolio.getPortfolio(aslist=True, stocksOnly = True)
    for astock in stocks:
        try:
            metrics(astock)
        except:
            print("astock: {}".format( astock))
