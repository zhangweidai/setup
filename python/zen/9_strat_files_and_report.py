import gen_strat
import strategy
import util

util.saveProcessedFromYahoo.download = False
where = gen_strat.historical()
strategy.multi(where)
