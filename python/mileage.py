import datetime
import random

caroneProb = 80
gohomeProbability = 44
personalTravelProbability = 60
endofdate = datetime.datetime.strptime("01/01/17", "%m/%d/%y")
car = dict()
miles = 0
dates = []
date_1 = datetime.datetime.strptime("01/01/16", "%m/%d/%y")
log = dict()
dalog = []
daydidntwork = 0
persmile = 0

def startOver():
    global car, miles, dalog, log, dates, date_1, daydidntwork, appointtotal, persmile
    persmile = 0
    daydidntwork = 0
    dalog = []
    car[0] = 95027
    car[1] = 102011
    miles = 0
    appointtotal = 0
    dates = []
    date_1 = datetime.datetime.strptime("01/01/16", "%m/%d/%y")
    log = dict()

appoints = []
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(0)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(1)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(2)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(4)
appoints.append(4)
appoints.append(4)
appoints.append(4)
appoints.append(5)

possiblemiles = []
possiblemiles.append(3)
possiblemiles.append(3)
possiblemiles.append(3)
possiblemiles.append(3)
possiblemiles.append(3)
possiblemiles.append(3)
possiblemiles.append(4)
possiblemiles.append(4)
possiblemiles.append(4)
possiblemiles.append(4)
possiblemiles.append(4)
possiblemiles.append(4)
possiblemiles.append(4)
possiblemiles.append(4)
possiblemiles.append(4)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(6)
possiblemiles.append(6)
possiblemiles.append(6)
possiblemiles.append(6)
possiblemiles.append(6)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(5)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(7)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(9)
possiblemiles.append(9)
possiblemiles.append(9)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(8)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(12)
possiblemiles.append(14)
possiblemiles.append(14)
possiblemiles.append(14)
possiblemiles.append(14)
possiblemiles.append(14)
possiblemiles.append(14)

locationtranslate = []
locationtranslate.append(("Keizer Permanante", 8))
locationtranslate.append(("Skyline", 4))
locationtranslate.append(("Salem Hospital",3))
locationtranslate.append(("Salem Clinic",4))
locationtranslate.append(("Arrow Dental",7))
locationtranslate.append(("Smile Keeper 408", 5))
locationtranslate.append(("Smile Keep 1800",7 ))
locationtranslate.append(("Eye Care Physician", 3))
locationtranslate.append(("Beverly", 7 ))
locationtranslate.append(("Lancaster Family",3))
locationtranslate.append(("South Salem Clinic", 2))
locationtranslate.append(("Keizer Station", 11))
locationtranslate.append(("West Salem Clinic",5))
locationtranslate.append(("River Road Salem Clinic",12))
locationtranslate.append(("River Road ENT",4))
maxplaces = len(locationtranslate)

longdistance = []
longdistance.append(("Samaritan Hospital", 39))
longdistance.append(("Beaverton KP", 50))
longdistance.append(("Sunnyside Medical Center", 60))


def distance(a, b):
    global log
    loc = -1 
    loca = None
    locb = None
    note = ""
    if a==0:
        note = ""
        loc = b
    elif b == 0:
        note = "Returning from "
        loc = a

    # going to or from home
    if loc > 0:
        loc -= 1
        secondplace = locationtranslate[loc][0]

        note =  "{}{}".format(note, secondplace)
        return [locationtranslate[loc][1], note]

    loca = locationtranslate[a-1][0]
    locb = locationtranslate[b-1][0]

    c = "{}_{}".format(a,b)
    c2 = "{}_{}".format(b,a)

    if None == log.get(c2) and None == log.get(c):
        single =  random.choice(possiblemiles)
        log[c] = single
        log[c2] = single

    note =  "{} to {}".format(loca, locb)
    return [int(log[c]), note]

def chooseCar():
    return 0

longdistancedays = []
longdistancedays.append(random.randint(1, 250))
longdistancedays.append(random.randint(1, 250))
longdistancedays.append(random.randint(1, 250))
longdistancedays.append(random.randint(1, 250))
longdistancedays.append(random.randint(1, 250))
longdistancedays.append(random.randint(1, 250))
day = 0

def updateappoints():
    global appoints
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)
    appoints.remove(0)

def subtract():
    global persmile
    global appointtotal
    global daydidntwork
    global miles
    global dates
    global dest
    global date_1
    global car
    global dalog
    global day

    date_1 = date_1 + datetime.timedelta(days=1)
    if date_1.isoweekday() > 5:
        return
    day += 1

    if day == 150:
        updateappoints()

    date = str(date_1.strftime("%m/%d/%y"))
    todaycar = chooseCar()
    starting = car[todaycar]

    if day in longdistancedays:
        ld = random.choice(longdistance)
        d = ld[1]

        note = "Going to {}".format(ld[0])
        ending = starting + d
        dalog.append(",".join([date, str(starting), str(ending), str(d), note]))
        starting += d

        note = "Returning from {}".format(ld[0])
        ending = ending + d
        dalog.append(",".join([date, str(starting), str(ending), str(d), note]))
        starting += d
        miles = miles + 2 * d

        car[todaycar] = starting
        return


    pointstoday = random.choice(appoints)
    if pointstoday == 0:
        daydidntwork += 1
        return
    appointtotal += pointstoday

#     print "\nDate is {}\n{} appointments using car {}".format( date, pointstoday, todaycar)

    places = []
    dmiles = []
    places.append(0)
    prevIndex = 0
    for x in range (0, pointstoday):
        destIndex = random.randint(0, maxplaces) 
        while destIndex == prevIndex:
            destIndex = random.randint(0, maxplaces) 

        prevIndex = destIndex
        places.append(destIndex)
        dmiles.append(locationtranslate[destIndex-1][1])

        if x < pointstoday -1 and random.randint(0,100) < gohomeProbability:
            places.append(0)

    places.append(0)

    submiles = 0
    for x in range (0, len(places)-1):

        a = places[x]
        b = places[x+1]

        retD = distance(a,b)

        d = retD[0]
        note =  retD[1]

#         print "distance to go from {} to {} is {}".format(a,b,d)
#         print "start mileage {} and end mileage {}".format(starting, starting + d)

        submiles += d
        miles += d

        dalog.append(",".join([date, str(starting), str(starting + d), str(d), note]))
        starting += d

    personal = random.randint(0,100)
    if personal < personalTravelProbability:
        gosomewhererandom = random.randint(5, 32)
        persmile += gosomewhererandom
        starting += gosomewhererandom

    car[todaycar] = starting

ava = 0
avb = 0
avc = 0
lowest = 10000
lowestlog = None
last = 0
cd = 0
while last != 316:
    cd += 1
    startOver();
    while (date_1 < endofdate):
        subtract()

    last = appointtotal
    print "{} and {}".format(last, daydidntwork)
    ava += daydidntwork
    avb += miles
    avc += appointtotal

f = open('file', 'w')
for entry in dalog:
    f.write("{}\n".format(entry))

print "days didnt work {}".format(daydidntwork)
print "percent didnt work {}".format(daydidntwork/250.00)
print "work miles so far {}".format(miles)
print "number of appointments {}".format(last)
print "personal miles {}".format(persmile)


print "avg days didnt work {}".format(ava/cd)
print "avg work miles so far {}".format(avb/cd)
print "avg number of appointments {}".format(avc/cd)
print "avg number of appointments per week {}".format((avc/cd)/52)
print "miles savings {}".format((avb/cd) * 0.54)
print "income {}".format((avc/cd) * 34)
print "income {}".format(((avc/cd) * 34)/24)
print "lowest appointment {}".format(lowest)

print "average {}".format(sum(possiblemiles)/len(possiblemiles))
