import datetime
import random

starting = 90000
miles = 0
total = 8000

dest = []
dest.append(0)
dest.append(0)
dest.append(0)
dest.append(1)
dest.append(2)
dest.append(3)
dest.append(4)
dest.append(5)
dest.append(6)


appoints = []
appoints.append(0)
appoints.append(0)
appoints.append(0)
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
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(3)
appoints.append(4)
appoints.append(5)
appoints.append(5)
appoints.append(6)

possiblemiles = []
possiblemiles.append(3)
possiblemiles.append(3)
possiblemiles.append(3)
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
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(10)
possiblemiles.append(40)
possiblemiles.append(60)

dates = []
date_1 = datetime.datetime.strptime("01/01/16", "%m/%d/%y")
endofdate = datetime.datetime.strptime("01/01/17", "%m/%d/%y")
log = dict()

daydidntwork = 0
def subtract():
    global daydidntwork
    global miles
    global dates
    global dest
    global date_1
    global starting
    global log

    date_1 = date_1 + datetime.timedelta(days=1)
    if date_1.isoweekday() > 5:
        return

    pointstoday = random.choice(appoints)
    if pointstoday == 0:
        daydidntwork += 1
        return

    print "\ndate is {}\n{} appointments".format(str(date_1), pointstoday)
    places = []
    dmiles = []
    places.append(0)
    prev = 0
    for x in range (0, pointstoday):
        bar2 = random.choice(dest)
        while bar2 == prev:
            bar2 = random.choice(dest)

        if x == pointstoday-1 and bar2 == 0:
            while bar2 == 0 or bar2 == prev:
                bar2 = random.choice(dest)
        
        prev = bar2
        places.append(bar2)
        dmiles.append(dest[bar2])

    places.append(0)
    submiles = 0
    for x in range (0, len(places)-1):
        a = places[x]
        b = places[x+1]
        c = "{}{}".format(a,b)
        c2 = "{}{}".format(b,a)

        if None == log.get(c2) and None == log.get(c):
            single =  random.choice(possiblemiles)
            log[c] = single
            log[c2] = single
        value = log[c]
        submiles += value
        print "going from {} to {} and it took {} miles".format(a,b, value)
        print "start mileage {} and end mileage {}".format(starting, starting + value)
        starting += value

        personal = random.randint(0,100)
        if personal > 60:
            gosomewhererandom = random.randint(1, 10)
#             print "personal mileage {}".format(gosomewhererandom)
            starting += gosomewhererandom
        miles += value

    print places
    print "work miles so far {}".format(miles)

while (miles < total and date_1 < endofdate):
    subtract()

print "days didnt work {}".format(daydidntwork)


