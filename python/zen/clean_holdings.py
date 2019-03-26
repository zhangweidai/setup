import util
import os
import fnmatch
def getCsvsFiles():
    pattern = "*.csv"  
    holds = []
    path = util.getPath('toscrub')  
    listOfFiles = os.listdir(path)
    for entry in listOfFiles:  
        if fnmatch.fnmatch(entry, pattern):
            holds.append("{}/{}".format(path,entry))
    return holds

def cleanFiles():
    for afile in getCsvsFiles():
        with open(afile, "r") as f:
            lines = f.readlines()
            found = 0
            for i,aline in enumerate(lines):
                if "Ticker" in aline:
                    found = i
                    break
        if found != 0:
            with open(afile, "w") as f:
                f.writelines(lines[found:])
    
os.system("./scrub.sh Derivatives")
dels = util.getp("deletes")
for astock in dels:
    os.system("./scrub.sh {}".format(astock))
