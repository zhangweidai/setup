import os
import z
from shutil import copyfile, copytree

dest = "/mnt/c/Users/pzhang/Documents/dest/split"
#z.gsavedir = dest

z.getp("dates")
path = z.getPath("split")
try:
    copytree(path, dest)
except:
    pass

dest = "/mnt/c/Users/pzhang/Documents/dest"
getpd = z.getp("getpd")
for name in getpd:
    path = z.getPath("{}/{}.pkl".format("pkl", name))
    newpath = "{}/{}.pkl".format(dest, name)
    print("newpath : {}".format( newpath ))
    copyfile(path, newpath)
