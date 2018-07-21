class Share:
    def __init__(self, name):
        pass

    def get_historical(self, start, end):
        vec =  {'Volume': '27145700', 'Symbol': 'intc', 'Adj_Close': '22.15698', 'High': '24.959999', 'Low': '24.629999', 'Date': '2014-01-29', 'Close': '24.68', 'Open': '24.75'}
        ret = []
        for a in range(0,14):
            ret.append(vec)
        return ret
