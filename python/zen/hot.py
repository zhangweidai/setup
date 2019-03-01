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

ranked = rankList(stocks)

encoder = None
def encodeRanked(ranking):
    global encoder
    encoder = OneHotEncoder(handle_unknown='ignore')
    encoder.fit(ranking)
    return encoder.transform(ranking).toarray()

print (encodeRanked(ranked))

#print (encoder.categories_)
#print (encoder.transform(ranking).toarray())

