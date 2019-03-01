import util
one = util.getStocks("IVV")
two = util.getStocks("USMV")
print (set(two) - set(one))

