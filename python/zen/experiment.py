d={'a':2, 'b':13}
def normalizeDict(dic):
    factor=1.0/sum(dic.values())
    for k in dic:
        dic[k] = dic[k]*factor
print (d)
print (normalizeDict(d))
print (d)

