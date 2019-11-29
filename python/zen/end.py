import locale
locale.setlocale(locale.LC_ALL,'')
age = 35
end = 70
stockrate = 0.0389
month_drawal = 300+500+200+200+120
startwithdraw = 40

years = end - age
months = years * 12
stocks = (210 + 25 + 26 )*1000
nowith = stocks
monthrate = stockrate / 12
print("stocks : {}".format( stocks ))
laststock = None
lasts = list()
lastsno = list()
startwdmonth = (startwithdraw - age)*12
withdrew = 0
lasts.append(stocks)
lastsno.append(stocks)
for month in range(months):
    stocks = round((stocks * monthrate) + stocks,2)
    nowith = round((nowith * monthrate) + nowith,2)

    if month > startwdmonth:
        stocks = stocks - month_drawal
        withdrew += month_drawal

    if not month % 12 and month >= 12:
        print("year : {}".format( month/12 ))
        lasts.append(stocks)
        lastsno.append(nowith)
        if len(lasts) >= 2:
            print("annual : {}".format( lasts[-1]/lasts[-2] ))
            print("annual : {}".format( lastsno[-1]/lastsno[-2] ))
            print("stocks : {}".format( locale.currency(stocks, grouping = True )))
            print("nowith : {}".format( locale.currency(nowith, grouping = True )))
            print("difference : {} withdrew {}\n".format( nowith-stocks, withdrew ))
    
print("lasts : {}".format( lasts ))
print("years : {}".format( years ))
print("annual draw : {}".format( 12*month_drawal ))

