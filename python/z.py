dic = {}
segments = {}
original_money = 30000
money = original_money
n_accounts = 3
n_months = 12
n_years = 2
segnums = n_accounts * n_months * n_years
cost = 600

class product:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        pass

    def gname(self):
        return self.name

    def glength(self):
        return self.length

    def cap(self):
        return 1.12

    def calc(self, value, growth):

        if growth < 0:
            print "did not grow, losing money"
            return value - cost

        if growth > self.cap():
            return value * self.cap()

        return value * (growth + 1)

added = {}
def addSegment(year, month, product, index, segmoney = 0):
    global money
    global segnums
    global segments
    global added

    name = product.gname()

    temp = str(year) + str(month) + name
    if not added.get(temp) == None:
        return
    added[temp] = 1

    if (money <= 0 and segmoney == 0):
        return;

    allocated = (original_money/segnums)

    if allocated > money:
        allocated = money


    subtotal = allocated + segmoney
    print "pulling from bank ${} ".format(allocated)

    inner2 = {}
    inner2[name] = (index, subtotal)

    expire = year + product.glength()

    if segmoney > 0 and segments.get(year):
        if segments[year][month][name] != None:
#             print "deleting segment {}".format(segments[year][month][name])
            del segments[year][month][name]

    print "setting segment month:{} year:{} at ${} expire:{} product:{}".format(month, year, subtotal, expire, name)
    if len(segments) == 0 or segments.get(expire) == None:
        inner = {}
        inner[month] = inner2
        segments[expire] = inner
    elif segments[expire].get(month) == None:
        segments[expire][month] = inner2
    else:
        segments[expire][month][name] = (index, subtotal)

    money = money - allocated
    print "money is at {}\n".format(money)

def process(datestr, index, product):
    global dic
    global money
    inner = {}
    inner2 = {}
    date = datestr.split("/")

    year = int(date[0])
    month = date[1]
    day = date[2]

#     print "\ny:{} d:{} m:{} cIndex:{}".format(year, day, month, index)

    inner2[product.gname()] = index
    inner[month] = inner2
    dic[year] = inner

    prevYear = year - 1

    foundYear = segments.get(year)
    if foundYear != None:
        foundMonth = foundYear.get(month)
        if foundMonth != None and len(foundMonth) > 0:
            print "FOUND segment in {} we found {} for month {}".format(year, 
                    foundMonth, month)
            shoebox = foundMonth.get(product.gname())
            if shoebox == None:
                return
            growth = 1-(shoebox[0]/index)
            print "growth {} ".format(growth)
            segmoney = shoebox[1]

            newmoney = product.calc(segmoney, growth)
            interest =  newmoney - segmoney
            print "interest earned {} ".format(interest)
            addSegment(year, month, product, index, newmoney)
        else:
            addSegment(year, month, product, index)
    else:
        addSegment(year, month, product, index)


def printsegs(segments):
    sub = 0
    for b in segments:
        for c in segments[b]:
            for d in segments[b][c]:
                sub += segments[b][c][d][1]
    return sub


read = None
with open("databig.csv", "r") as f:
    read = f.readlines()

print "starting {}".format(money)

oneyear = product("oneyear", 1)
# oneyear_2 = product("oneyear2", 1)
# oneyear_3 = product("oneyear3", 1)
twoyear = product("twoyear", 2)
fiveyear = product("fiveyear", 5)

for line in read:
    tokens = line.split("\n")
    for token in tokens:
        if "#" in token:
            continue

        if token == "":
            continue

        second = line.split(",")

        if len(second) != 2:
            continue;

        process(second[0], float(second[2]), oneyear)
        process(second[0], float(second[2]), twoyear)
        process(second[0], float(second[2]), fiveyear)


print "\n"
print "total at end {}\nstarted out at {}\nmoney in bank {}".format(printsegs(segments) + money, original_money, money)


