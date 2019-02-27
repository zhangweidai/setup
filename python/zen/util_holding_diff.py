import stock_analyze
one = stock_analyze.getStocks("IVV")
two = stock_analyze.getStocks("USMV")
print (set(two) - set(one))

