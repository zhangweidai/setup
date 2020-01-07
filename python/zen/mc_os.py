import z
import buy
stocks = z.getp("listofstocks")
from sortedcontainers import SortedSet

# shrinking outstanding shares and increasing marketcap with slight volume

sset = SortedSet()
for astock in stocks:
    try:
        if buy.getFrom("latestmc", astock, None) > 1500:
            continue

        yearagomc_size = buy.getFrom("yearagomc", astock)
        mc_size = buy.getFrom("latest_mc", astock)
        mcc = round(mc_size/yearagomc_size,4)
        dr, ebit, r_value, slope = buy.getFrom("wlp_lasts", astock)
        volr = buy.getFrom("voldic", astock)
        if slope < -0.7 and abs(r_value) > 0.8 and mcc > 1.1 and volr < 1700:
            buy.addSortedHigh("mc_os", mcc, astock, 30)
    except Exception as e:
        pass

bar = buy.getSorted("mc_os")
print("bar : {}".format( bar ))
buy.multiple(bar, runinit = True)

