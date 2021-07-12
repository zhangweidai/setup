import csv
from termcolor import colored
from collections import defaultdict
import datetime
from taxutils import *

basis_prices = defaultdict(list)
basis_dates = defaultdict(list)
basis_sizes = defaultdict(list)
basis_fees = defaultdict(list)

def buy(product, price, tran_date, size, fee = 0):
#    print("BUY {} tran_date : {} size {} price {}".format( product, tran_date, size, price ))

    if not tran_date in basis_dates[product]:
        # first encounter date 
        basis_dates[product].append(tran_date)
        basis_prices[product].append(price)
        basis_sizes[product].append(size)
        basis_fees[product].append(fee)
    else:
        # second encounter date merge
        indx = basis_dates[product].index(tran_date)
        basis_sizes[product][indx] = basis_sizes[product][indx] + size
        basis_prices[product][indx] = max((basis_prices[product][indx], price))

helps = list()
maxes = list()
def sellHelper(salesPrice, saleAmount, i):
    helps.append((salesPrice, saleAmount, i))
    maxes.append(salesPrice)

alldics = list()

def record(dateAcquired, dateSold, salesPrice, costBasis, amount):
    global alldics
    description = "{}_{}_c{}_os{}".format(round(amount,4), original_product, round(costBasis,3), round(original_sell_size,3))
    print ("SELLING", " ".join([description, str(dateAcquired), str(dateSold), str(salesPrice), str(costBasis)]))
#short,3,5_ETCUSD_c10_5,20210306,20210306,100,100
    ret = dict()
    ret['holdingType'] = "short"
    ret['reportingCategory'] = "3"
    ret['description'] = description
    ret['dateAcquired'] = dateAcquired
    ret['dateSold'] = dateSold
    ret['salesPrice'] = round(salesPrice * amount,2)
    ret['costBasis'] = round(costBasis * amount,2)
    alldics.append(ret)

removes = list()
def getSell(product, remaining, dateSold, salesPrice):
    global helps, removes
    maxvalue = max(maxes)
    idx = maxes.index(maxvalue)
    costBasis, saleAmount, i = helps[idx]

    need_to_remove = False

    try:
        last_date = basis_dates[product][i]
        last_price = basis_prices[product][i]
    except Exception as e:
        print("e: {}".format( e))
        print("helps: {}".format( helps))
        print("maxes: {}".format( maxes))
        exit()

    if saleAmount < remaining:
        # sold all
        need_to_remove = True
        record(last_date, dateSold, salesPrice, costBasis, saleAmount)
    else:
        new_size = saleAmount - remaining
        if new_size <= 0:
            need_to_remove = True
        else:
            helps[idx] = (salesPrice, new_size, i)
            basis_sizes[product][i] = new_size
        record(last_date, dateSold, salesPrice, costBasis, remaining)
        saleAmount = remaining

    if need_to_remove:
        maxes.pop(idx)
        helps.pop(idx)
        removes.append(i)

    remaining = remaining - saleAmount
    if not maxes and remaining:
        record(last_date, dateSold, salesPrice, costBasis, remaining)
    return remaining

original_sell_size = None
original_product = None
def sell(product, salesPrice, dateSold, size, fee = 0):
    global helps, original_sell_size, original_product
    global maxes, removes
    original_sell_size = size
    original_product = product

    if salesPrice == 0:
        print("SELL tran_date : {} size : {} salesPrice : {}".format( dateSold, size, salesPrice))
        exit()

    removes = list()
    helps = list()
    maxes = list()

    for i, date in enumerate(basis_dates[product]):
        if dateSold < date:
            continue

        sellHelper( basis_prices[product][i], basis_sizes[product][i], i)

    remaining = size
    while helps and remaining > 0:
        remaining = getSell(product, remaining, dateSold, salesPrice)

    removes = sorted(removes, reverse=True)
    for i in removes:
        basis_prices[product].pop(i)
        basis_sizes[product].pop(i)
        basis_dates[product].pop(i)

    if not helps and remaining:
        print("TROUBLE {} {} dateSold : {} size : {} salesPrice : {}".format( colored("SELL", "red"), product,
                    dateSold, size , salesPrice))
        return

def status():
    print("basis_sizes : {}".format( basis_sizes ))
    print("basis_dates : {}".format( basis_dates ))
    print("basis_prices: {}".format( basis_prices))
    print("basis_prices: {}".format( len(basis_prices)))

def test_collecting():
    product = "ETCUSD"
    size = 10
    price = 10
    total = 289.3654
    date = 20210306

    buy(product, price, date, size)

    size = 15
    sell(product, price, date, size)
    status()
    printfile()
    exit()

    price = 20
    size = 5
    date = 20210307
    buy(product, price, date, size)

    size = 16
    price = 15
    date = 20210308
    sell(product, price, date, size)

def printfile():
    print("alldics: {}".format( len(alldics)))
    keys = ["holdingType","reportingCategory","description","dateAcquired","dateSold","salesPrice","costBasis"]
    #long,1,Some Stock,12/02/2007,03/04/2017,1234.50,325.55
    outputfile = "outputnew.csv"
    with open(outputfile, 'wt') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, lineterminator='\n')
        dict_writer.writeheader()
        dict_writer.writerows(alldics)
#    print("total : {}".format( round(total,2) ))
if __name__ == '__main__':
    test_collecting()
    printfile()
