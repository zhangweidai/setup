import z
import buy
from sortedcontainers import SortedSet

def generateWorst30():
    dates = z.getp("dates")
    stocks = z.getp("listofstocks")
    yearlydic = z.getp("latestAnnual")
    answer = SortedSet()
    for idx,astock in enumerate(stocks):
        mcrank = buy.getMCRank(astock)
        try:
            if int(mcrank) > 320:
                continue

            price = buy.getPrice(astock, dates[-252])
            if price < 5:
                continue
        except Exception as e:
            continue


        try:
            annual = yearlydic[astock]
        except:
            print("missing annual for : {}".format( astock))
            continue

        answer.add((annual, astock))
        if len(answer) > 30:
            answer.remove(answer[-1])

    print("answer: {}".format( answer))
    z.setp(answer, "worst30")


generateWorst30()
exit()

if __name__ == '__main__':
    import update_history
    try:
        latestprices = dict()
        problems = [] 
        skips = list()
#        if args.skips:
#            skips = z.getp("problems")

        if update_history.update(prices = latestprices, problems=problems, skips=skips):
            if problems:
                print("problems: {}".format( problems))
                key = readchar.readkey()
                if key == "d":
                    for pstock in problems:
                        z.delStock(pstock)
                    exit()

            print ("finished update history 1")
            update_history.update(where= "ETF", prices=latestprices)
            print ("finished update history 2")
            z.setp(latestprices, "latestprices")

#            if "2" in args.main:
#                import json_util
#                json_util.saveOutstanding(update=True)
#                diffOuts()

#            reloaddic()
#            import startover_rank
#            startover_rank.saveData()

            import ranketf2
            ranketf2.regen()

            import prob_down_5_years
            prob_down_5_years.prob()

            import gained_discount
            gained_discount.dosomething()

            generateWorst30()
            import buyat
            buyat.runmain()

            exit()

    except Exception as e:
        print ("problem with gbuy")
        z.trace(e)
        exit()


