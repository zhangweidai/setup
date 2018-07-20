#!/usr/bin/python
import types
import fnmatch
import os

bar = {}
bar['a'] = True
try:
    foo = bar['a']
    print foo
    foo = bar['b']
    print foo
except:
    pass
exit()

def writeTclFile(newFile, w1, w2, options, ascii, log):
    fo = open("./template.tcl", "r")
    content = fo.readlines()
    fo.close()

    fo = open(newFile, "w")
    text = "".join(content)
    text.format(w1, w2,options,ascii, log)
    fo.write(text)
    fo.close()



def hasAdditionalFailures(manualOutputDir, aceOutputDir):
    matches = []
    for root, dirnames, filenames in os.walk(aceOutputDir):
        for filename in fnmatch.filter(filenames, '*.wave'):
            matches.append(os.path.join(root, filename))

    nominalWaveForm = "~/tests/regtest/gui/ace3/input/wave_meas/nominal_ref.wave"

    for i, wave in enumerate(matches):
        basen = os.path.basename(wave).split(".")[0]
        newFile = "{}/{}.tcl".format(manualOutputDir, basen)
        writeTclFile(newFile, nominalWaveForm, wave )


print hasAdditionalFailures(".", "./tst_specreport_spec_edit/del.ace/")
exit()

def getConsolidatedAEX(dir):
    matches = []
    for root, dirnames, filenames in os.walk(dir):
        for filename in fnmatch.filter(filenames, '*.aex'):
            matches.append(os.path.join(root, filename))

    if len(matches) == 1:
        return matches[0]

    retFile = "./combinedManualResults.aex"
    with open(retFile, 'w') as outfile:
        for fname in matches:
            with open(fname) as infile:
                outfile.write(infile.read())
    return retFile

print getConsolidatedAEX("/home/pzhang/tests/regtest/gui/ace3/python_tests/ace/eldo/comprehensive_test/state_afs.ace/Simulations/ACE_Sweep-afs0")
exit()

class TestWrapper():
    def __init__(self):
        self.cornerVec = []

    def addCorner(self, name, params, includes):
        self.cornerVec.append([name, params, includes])

    def getCornerData(self):
        value = []
        corners = []
        params = []
        for corner in self.cornerVec:
            corners.append(corner[0])
            for param in corner[1]:
                params.append(param[0])

        value.append(("setCorners",        [corners, list(set(params))]))

        for corner in corners:
            value.append(("setCornerDisabled", [corner, False]))

        for corner in self.cornerVec:
            for param in corner[1]:
                value.append(("setCornerValue",    [corner[0], param[0], param[1]]))
            value.append(("setModelDefs",    [corner[0], corner[2]]))
        return value

    def getCornerCmd(self):
        ret =  "\n.option no_nominal_alter \n"
        for corner in self.cornerVec:
            ret +=  ".alter {} \n".format(corner[0])
            for param in corner[1]:
                if param[0] == "temp":
                    ret += ".temp {} \n".format(param[1])
                else:
                    ret += ".param {} = {} \n".format(param[0], param[1])

            for includePath in corner[2]:
                ret += ".include {} \n".format(includePath)

        return ret

    def commitCorners(self, name):

        cornerData = self.getCornerData()
        #self.currentAOHandle = adb_ADB.createCorner(name)
        #self.createObjs(name, data)

        cornerCmd = self.getCornerCmd()
        #appendCommand(self.currentNetlist, cornerCmd)

def test():
    tester = TestWrapper()

    params = [ ("temp", "27"), ("tend", "60n") ]
    includes = ["./lib/hspiceInclude_2.spi"]
    tester.addCorner("C1", params, includes)

    includes = ["./lib/hspiceInclude.spi"]
    tester.addCorner("C2", [], includes)

    tester.commitCorners("Corner")

test()
exit()

class Person():
    _names_cache = {}
    def __init__(self,name):
        self.name = name
        Person.count = Person.count + 1
        self.mycount = Person.count
    def __new__(cls,name):
        return cls._names_cache.setdefault(name,object.__new__(cls,name))
    def dothis(self, arg):
        self.name = self.name + " did this: " + arg
        return self.name
    def dothis2(self, arg):
        self.name = self.name + " did this2: " + arg
        return self.name

    def setUseSeed(self, boolean, value = -2):
        print "Wow"
        print value
        if boolean:
            print "yes"
        else:
            print "no"


Person.count = 0

print "COUNTS hERE"
t = Person("Tory")
z = Person("Zoe")
what = [True, 1]
def delme(boolean, value):
   print value
   if boolean:
       print "yes"
   else:
       print "no"
delme(*what)
print type(["a"])
print type("a")

def proc(kwargs):
    p = Person("Peter")
    for func in kwargs:
        evalfunc = eval("p."+func)
        evalfunc(*kwargs[func])

b = {}
b["dothis"] = ["values"]
b["dothis2"] = ["bvalues"]
b["setUseSeed"] = [False, 2]
proc(b)

exit()

ifile = "./th.is/ismy.file"
basen = os.path.basename(ifile).split(".")
newfile = os.path.dirname(ifile)+ "/"+basen[0]+"2."+basen[1]
print newfile


def someFunction(a = 2,b = 0):
   print (a-b)
   return ["done"]

something = someFunction(b=12)
something = someFunction(a=12)
print (something[0])

mystring = "asdfa"
print (type(mystring))
mystring = 2
print (type(mystring))
if type(mystring) == types.IntType:
   print ("Im INT")
else:
   print ("Im NOT INT")

mystring = None

if type(mystring) == types.NoneType:
   print ("Im None")

# Function definition is here
def printinfo( arg1, *vartuple ):
   "This prints a variable passed arguments"
   print "Output is: "
   print arg1
   for var in vartuple:
      print var
   return
printinfo( 70, 60, 50 );

sum = lambda arg1, arg2 : arg1 + arg2;
print "Value of total : ", sum( 10, 20 )

lis = []
lis.insert(0,1)
lis.insert(0,2)

print "\033[92mlist is\033[0m:",lis

# map; table, dic
tel = {'jack': 4098, 'sape': 4139, 'zoe' : "ok"}
print tel['sape']
print tel.get('saped')
print tel.keys()
print "\033[92mMap is\033[0m:",tel

print ' 1  2   3  '.split()

from collections import namedtuple
Point = namedtuple('Point', 'x y')
pt1 = Point(1.0, 2.0)
print (pt1.x, pt1)

def iequal(a, b):
   try:
      return a.upper() == b.upper()
   except AttributeError:
      return a == b


peter = 'Zhang'
if iequal(peter, 'zhang'):
   print 'good'
else:
   print 'bad'


def fooFunc(netlist):
    print "hello"
    print netlist
    return netlist.split("a")
b = eval("fooFunc")
w = b("what")
print w


class Person():
    _names_cache = {}
    def __init__(self,name):
        self.name = name
        Person.count = Person.count + 1
        self.mycount = Person.count
    def __new__(cls,name):
        return cls._names_cache.setdefault(name,object.__new__(cls,name))
    def dothis(self):
        self.name = self.name + " did this" 

Person.count = 0

print "COUNTS hERE"        
peter = Person("Peter")
tory = Person("Tory")
zoe = Person("Zoe")
print zoe.mycount
print tory.mycount
print peter.mycount
print peter.name
peter.dothis()
print peter.name

try:
   import cPickle as pickle
except:
   import pickle



class Team(object):
    def __init__(self, name=None, logo=None, members=0):
        self.name = name
        self.logo = logo
        self.members = members

team = Team("Oscar", "http://...", 10)

team2 = Team()
team2.name = "Fred"
team3 = Team(name="Joe", members=10)
print team

def doit():
    import math,time
    a=0
    while a < math.pi:
        print " "*int(4+20*math.sin(a))+str(a);
        time.sleep(0.01)
        a+=.24

#doit()

import subprocess
import time
ts = time.time()
lineStr = ""
#lineStr = subprocess.Popen(['cat', "/net/skyline/scratch1/aref/peval.para_rc"], stdout=subprocess.PIPE).communicate()[0]
te = time.time()
elapsed_time = te - ts
print "Elapsed Time:" , elapsed_time
lineVec = lineStr.split('\n');
lvsIgnore = False
propEval = False
brokenRefs = False
for aline in lineVec:
    if aline.find("Removing Inst") > 0:
        lvsIgnore = True
    elif aline.find("Saving oaProp") > 0:
        propEval = True
    elif aline.find("Broken Reference") > 0:
        brokenRefs = True

if lvsIgnore: 
    print "ignoring"
if propEval: 
    print "evaluating"
if brokenRefs: 
    print "brokenRefs"

exit()

import os
print os.path.basename("/var/tmp")

print "start"

def process(contents):
    for var in contents:
        print var

#file
dumpFile = open("/net/skyline/scratch1/regen/test", 'r+')
lineVec = dumpFile.read()
lineVec = lineVec.split('\n')
prepath = "/wv/icqa/work_areas/top_xregr/icqa"

for var in lineVec:
    if var.find("ic.xregr") == 0:
        tempLine = var.split(" ")
        path = prepath +"/"+tempLine[0]
        print path
        contents = os.listdir(path)
        process(contents)
dumpFile.close()
print "end"

def set_transform(x):
    y = "this is so coo" + x
    print "what " + x
    return y

# print abcdefg in reverse
print "abcdefg"[::-1]

retva = set_transform("l HELLOworld")
print retva
