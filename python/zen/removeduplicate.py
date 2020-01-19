import z

stocks = z.getp("listofstocks")
start = False
allowed = ["A", "B", "C"]
for astock in stocks:
    if astock[0] not in allowed:
        continue
#    if astock == "BRKB":
#        start = True

#    if not start:
#        continue

    try:
        path = z.getPath("split/{}/{}_2019.csv".format(astock[0], astock))
        with open(path, "r") as f:
            lines = f.readlines()
        
        with open(path, "w") as f:
            prevline = None
            for aline in lines:
                date = aline.split(',')[0]
                if date != prevline:
                    f.write(aline)
                prevline = date

    except:
        print("path : {}".format( path ))
        pass
