import util
import pandas
#key: ScoreA 41421.0 0.381
#key: Score 36637.0 0.376
#key: DiscountA 48862.0 0.365
#key: Discount 46259.0 0.392
#key: DipA 23102.0 0.284
#key: Dip 73186.0 0.33
#key: VarianceA 64922.0 0.224
#key: Variance 22395.0 0.39
#key: PointsAboveA 30709.0 0.358
#key: PointsAbove 49136.0 0.423
#key: WCA 63460.0 0.327
#key: WC 36524.0 0.414

stocks = util.getStocks()

def negs(x):
    return x < 1

dic = dict()
for i in range(1, 10):
    path = util.getPath("final/selection_standard_{}.csv".format(i))
    df = pandas.read_csv(path)
#    print("dic : {}".format( dic.columns ))
    for idx in df.index:
        mode =  df.at[idx, "Unnamed: 0"]
        dollar =  df.at[idx, "Cost"]
        tokens = mode.split("/")
        ascending = "A" if tokens[1] == "True" else ""
        mode = "{}{}".format(tokens[0], ascending)
        dic.setdefault(mode, list())
        dic[mode].append(dollar)

for key in dic:
    vals =  dic[key]
    total = len(vals)
    neg = sum(map(negs, vals))
    added = sum(vals)
    percn = round(neg/total,3)
    print("key: {} {} {}".format( key, added, percn))

#    raise SystemExit
#    highs = df["High"].tolist()
#    lows = df["Low"].tolist()
#    for value in values:
#        print("value : {}".format( value ))
#        raise SystemExit

