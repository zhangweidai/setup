import z
d1 = z.getp("prob_down")
d2 = z.getp("prob_down_5_10")
from sortedcontainers import SortedSet

scores = SortedSet()
def doem():
    saveem = dict()
    stocks = z.getp("listofstocks")
    for idx, astock in enumerate(stocks):
        if not idx % 100:
            print("idx: {}".format( idx))
        try:
            score = d1[astock] + (1-d2[astock])
        except:
            continue
        scores.add((score, astock))
    z.setp(scores[-30:], "probs_added_up")

if __name__ == '__main__':
    doem()
