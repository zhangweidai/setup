import z
def setStockDays():
    df = z.getCsv("SPY")
    dates = df["Date"].tolist()
    z.setp(dates,"dates")
#setStockDays()
