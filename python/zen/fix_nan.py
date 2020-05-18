import regen_stock
apath = "problem"
items = set()
with open(apath, "r") as f:
    bar = f.readlines()
    for line in bar:
        astock = line.split("_")
        items.add(astock[0])
print("items: {}".format( items))
for astock in items:
    regen_stock.process(astock)
