import z
import zen
import buy
from collections import defaultdict
from sortedcontainers import SortedSet

# largest change by mc years ago as a last year predicter

wlp_dict = z.getp("wlp_dict")

dates = z.getp("dates")
rsi_indicator_dic = dict()
changers = SortedSet()
yearsago = -1*252*2
keeping = 60
discardlocation = int(keeping/2)
for j, astock in enumerate(wlp_dict.keys()):
    seen = list()
    rsid = dict()
    rseen = list()
    try:
        bar = wlp_dict[astock]
        if astock == "BA":
            print("bar : {}".format( bar.keys() ))
        data1 = bar[dates[-252]][0]
        data2 = bar[dates[yearsago]][0]
        change = round(data1/data2,3)
        changers.add((change, astock))
        if len(changers) > keeping:
            changers.discard(changers[discardlocation])
#        change2 = data2/data3
#        change2 = data2/data3
    except:
        pass

#print("changers: {}".format( changers))
z.setp(changers[:discardlocation], "mc1", True)
z.setp(changers[-1*discardlocation:], "mc2", True)
exit()

#    if not j % 100:
#        print("count: {}".format( j))
#
#    try:
#        prev = None
#        for i, row in enumerate(buy.getRows(astock, dates[0])):
#            c_close = round(float(row[z.closekey]),2)
#            try:
#                change = round(c_close/prev,4)
#            except:
#                prev = c_close
#                continue
#            seen.append(change)
#            if len(seen) > count:
#                seen.pop(0)
#                try:
#                    rsi = getRsi(seen)
#                except:
#                    print("{} problems: {}".format(astock, seen))
#                    continue
#                rseen.append((rsi, c_close))
##                rsid[row['Date']] = round(rsi,1)
#            prev = c_close
#    except Exception as e:
#        z.trace(e) 
#        pass
#
#    tally = list()
#
#    for i, pair in enumerate(rseen):
#        rsi = pair[0]
#        try:
#            if rsi <= 20:
#                if pair[1] < rseen[i+preday][1]:
#                    tally.append(1)
#                else:
#                    tally.append(-1)
#            elif rsi >= 80:
#                if pair[1] > rseen[i+preday][1]:
#                    tally.append(1)
#                else:
#                    tally.append(-1)
#        except:
#            pass
#    try:
#        lental = len(tally)
#        if lental < 50:
#            continue
#        valid = abs(round(sum(tally)/lental,3))
#    except:
#        continue
#    rsi_indicator_dic[astock] = valid
#    rsi_high.add((valid, astock))
#    if len(rsi_high) > 30:
#        rsi_high.remove(rsi_high[0])
#z.setp(rsi_indicator_dic, "rsi_indicator_dic")
#z.setp(rsi_high, "rsi_high", True)
#
