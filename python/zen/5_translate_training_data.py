import json_util
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
    save = False
    if encoder is None:
        encoder = OneHotEncoder(handle_unknown='ignore')
        save = True
    encoder.fit(ranking)

    if save:
        with open("encoder.pkl", "w") as f:
            import pickle
            pickle.dump(encoder, f)
    return encoder.transform(ranking).toarray().tolist()

def first(elem):
    return elem[1]

def second(elem):
    return elem[2]

# True is Descending
def rankEm(stocks, method = (True, False)):
    stocks.sort(key=first, reverse=method[0])
    for i, astock in enumerate(stocks):
        stocks[i][1] = i

    if not method[1] == None:
        stocks.sort(key=second, reverse=method[1])
        for i, astock in enumerate(stocks):
            stocks[i][2] = i
    return stocks

#stocks = [["goog",321, 1], ["spy",100,132], ["voo",30,3], ["ivv",1,0.2]]
#ranked = rankEm(stocks, method = (True, False))
#print (encodeRanked(ranked))
import util
import os

def translateTraining():
    files = util.getTrainingTemps()
    for afile in files:
        path = util.getPath("training_data/{}".format(afile)
        print (path)
        trend_dict = json_util.getData(path, asList = True)
        ranked = rankEm(trend_dict, method = (True, False))
        encoded = encodeRanked(ranked)
        path = util.getPath("encoded/prep_{}.py".format(afile.split(".")[0]))
        with open(path, 'w') as f:
            f.write('score = %s' % encoded)

translateTraining()

#from prepared import score as my_list
#print (my_list)

#training_data_encoded
#with open(path, "w") as f:
#    f.write(str(saveList))

#generateTrainingData(util.getStocks("IVV", andEtfs = True, dev=True))
