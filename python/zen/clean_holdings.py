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

print(getCsvsFiles())
