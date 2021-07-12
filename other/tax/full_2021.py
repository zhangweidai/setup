import csv
from termcolor import colored
from collections import defaultdict
import datetime

from taxutils import *

print (colored('Start', 'red'), colored('Here', 'green'))

#Date(UTC),          Pair,  Type, Order Price, Order Amount, AvgTrading Price,  Filled, Total,      status
#2021-03-06 06:04:11,ETCUSD,SELL, 11.0868,     26.10,        11.0868,           26.10,  289.3654,   Filled

path = "2021/pro.csv"
def getProduct(product):
    product = product.replace("-", "")
    product = product.replace("USDT", "USD")
    product = product.replace("USDC", "USD")
    product = product.replace("XETH", "ETH")
    product = product.replace("XXBT", "BTC")
    product = product.replace("ZUSD", "USD")
    return product

def binance(row):
    if row["status"] != "Filled":
        return

    try:
        operation = row["Type"]
        product = getProduct(row['Pair'])
        price = float(row['AvgTrading Price'])
        date = get_date(row['Date(UTC)'])
        size = float(row['Order Amount'])
        return operation, product, price, date, size 
    except:
        return None

#portfolio, trade id,   product,    side,   created at, 
#default,   697,        XRP-USD,    BUY,    2019-02-26T19:46:02.301Z,
#size,          size unit,      price,    fee,        total,              price/fee/total unit
#157.00000000,  XRP,            0.3167,   0.1491657,   -49.8710657,       USD

def get_date(date):
    dates = date.split(" ")[0].split("-")
    tran_date = int("{}{}{}".format(dates[0], dates[1], dates[2]))
    return tran_date

def get_date2(date):
    dates = date.split("T")[0].split("-")
    return int("{}{}{}".format(dates[0], dates[1], dates[2]))

def pro(row):
    operation = row["side"]
    product = getProduct(row['product']) 
    price = float(row['price'])
    date = get_date2(row['created at'])
    size = float(row['size'])
    return operation, product, price, date, size 
#def buy(            product,  price,    tran_date, size, fee = 0):
#    answer: ('BUY', 'XRPUSD', '0.3167', 20190226, '157.00000000')

#Date,Time (UTC),Type,Symbol,Specification,Liquidity Indicator,Trading Fee Rate (bps),USD Amount USD,Fee (USD) USD,USD Balance USD,BTC Amount BTC,Fee (BTC) BTC,BTC Balance BTC,BCH Amount BCH,Fee (BCH) BCH,BCH Balance BCH,LTC Amount LTC,Fee (LTC) LTC,LTC Balance LTC,Trade ID,Order ID,Order Date,Order Time,Client Order ID,API Session,Tx Hash,Deposit Destination,Deposit Tx Output,Withdrawal Destination,Withdrawal Tx Output
#2021-02-19,04:26:23.644,Buy,BTCUSD,Limit,Taker,35.00 ,($519.83),($1.82),"$4,478.35 ",0.0101601 BTC ,,0.0101601 BTC ,,,0.0 BCH ,,,0.0 LTC ,23461468313,23461468308,2021-02-19,04:26:23.643,,,,,,,
req = ["BUY", "SELL"]

def gemfix(strval):
    strval = strval.split(" ")[0]
    try:
        return float(strval)
    except:
        if "(" in strval:
            strval = strval[1:]
        if ")" in strval:
            strval = strval[:-1]
        if "$" in strval:
            strval = strval[1:]
        strval = strval.replace(",", "")
    return float(strval)

def gemini(row):
    operation = row["Type"].upper()
    if operation not in req:
        return

    date = get_date(row['Date'])
    product = getProduct(row['Symbol']) 
    prductless = product[0:-3]

    size = gemfix(row['{} Amount {}'.format(prductless, prductless)])
    usd_amount = gemfix(row['USD Amount USD'])
    price = (usd_amount / size)

    return operation, product, price, date, size 

#"txid","ordertxid","pair","time","type","ordertype","price","cost","fee","vol","margin","misc","ledgers"
#"TUYXVT-ERWMN-WLLARC","OK32XX-NNRGK-FT3MGP","XETHZUSD","2021-02-15 20:28:14.7123","sell","market",1834.98000,500.34400,1.30089,0.27267000,0.00000,"","LLV5QZ-3IOES-7VWYPL,LVEN5S-2HQTW-JL57Z7"

def kraken(row):
    operation = row["type"].upper()
    if operation not in req:
        return

    date = get_date(row['time'])
    product = getProduct(row['pair']) 
    price = float(row['price'])
    size = float(row['vol'])

    return operation, product, price, date, size 

#files = [("2021/kraken.csv", kraken)]

files = [("2021/binance.csv", binance) , ("2021/pro.csv", pro), 
      ("2021/gemini.csv", gemini),
      ("2021/kraken.csv", kraken)]
#files = [("2021/binance.csv", binance)]
sells = list()

for pair in files:
    csvpath = pair[0]
    method = pair[1]

    for row in csv.DictReader(open(csvpath)):
        try:
            answer = method(row)
            if not answer:
                continue

            if answer[2] == 0: 
                exit()

            if answer[0] == "BUY":
                buy(product = answer[1], 
                    price = answer[2], 
                    tran_date = answer[3], 
                    size = answer[4])
            else:
                sells.append(answer)
        except Exception as e:
            import traceback
            print (traceback.format_exc())
            print("e: {}".format( e))
            print("answer : {}".format( answer ))
            continue

    for asell in sells:
        sell(product = asell[1], 
             salesPrice = asell[2], 
             dateSold = asell[3], 
             size = asell[4])


    #status()
printfile()
exit()

