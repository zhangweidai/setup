from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder(handle_unknown='ignore')
#X = [['Male', 1], ['Female', 3], ['Female', 2]]
#print ("enc.fit(X)")
#print (enc.fit(X))
#print (enc.transform([['Female', 1], ['Male', 1]]).toarray())
#print (enc.inverse_transform([[1, 0, 1, 0, 0], [0, 1, 1, 0, 0]]))
#print ("enc.categories_")
#print (enc.categories_)
#print ("enc.transform([['Female', 1], ['Male', 4]]).toarray()")
#print (enc.transform([['Female', 1], ['Male', 4]]).toarray())
#print ("enc.inverse_transform([[0, 1, 1, 0, 0], [0, 0, 0, 1, 0]])")
#print (enc.inverse_transform([[0, 1, 1, 0, 0], [0, 0, 0, 1, 0]]))
#print ("enc.get_feature_names()")
#print (enc.get_feature_names())

stocks = ["goog", "spy", "voo", "ivv"]
def rankList(stocks):
    for i,b in enumerate(stocks):
        stocks[i] = [stocks[i], i]
    return stocks

#ranked = rankList(stocks)

encoder = None
def encodeRanked(ranking):
    global encoder
    encoder = OneHotEncoder(handle_unknown='ignore')
    encoder.fit(ranking)
    return encoder.transform(ranking).toarray()

def first(elem):
    return elem[1]

def second(elem):
    return elem[2]

#stocks = [["goog",321, 1], ["spy",100,132], ["voo",30,3], ["ivv",1,0.2]]
# True is Descending
def rankEm(stocks, method = (True, False)):
    stocks.sort(key=first, reverse=method[0])
    for i, astock in enumerate(stocks):
        stocks[i][1] = i

    if not method[1] == None:
        stocks.sort(key=second, reverse=method[1])
        for i, astock in enumerate(stocks):
            stocks[i][2] = i
    print (stocks)

import util
trend_dict = util.getData("Final_all", asList = True)
#mylist = []
#for key, value in trend_dict.iteritems():
#    temp = [key,value[1]]
#    mylist.append(temp)
rankEm(trend_dict, method = (True, None))
#    if not method[0]:
#        stocks.sort(key=second, reverse = True)
#    if not method[0]:
#        stocks.sort(key=max1)

#print (encodeRanked(ranked))

#print (encoder.categories_)
#print (encoder.transform(ranking).toarray())

