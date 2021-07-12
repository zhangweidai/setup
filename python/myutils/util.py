import pickle
path = "/tmp/picks/{}.pkl"
def savep(name, data):
    pickle.dump(data, open(path.format(name), "wb"))

def loadp(name):
    return pickle.load(open(path.format(name), "rb"))
