import util
etfs = util.getFromHoldings()
ivv = set(util.getStocks("IVV"))
common = set()
test = set()
path = "etf_report"
with open(path, "w") as f:
    for etf in etfs:
        if etf == "IVV" or etf == "USRT" or etf == "VLUE":
            continue
        other = set(util.getStocks(etf))
        f.write ("ivv - {}\n".format(etf))
        f.write (", ".join(ivv - other))
        f.write ("\n")
    
        f.write ("{} - ivv\n".format(etf))
        f.write (", ".join(other-ivv))
        f.write ("\n")
    
        f.write ("common {}\n".format(etf))
        temp = (other&ivv)
        if not common:
            common = temp
            test = temp
        else:
            test = (common & temp)
            if test:
                common = test
        f.write (", ".join(temp))
        f.write ("\n")
    
    f.write ("COMMON\n")
    f.write (", ".join(common))
