import urllib.request, json 
def saveJson(astock):
    with urllib.request.urlopen("https://financialmodelingprep.com/api/company/profile/{}".format(astock)) as url:
        decoded = url.read().decode()
        data = json.loads(decoded.replace("<pre>",""))
        with open('./json/{}.json'.format(astock), 'w') as outfile:
            json.dump(data, outfile)
