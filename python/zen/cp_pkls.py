import os
import z
from shutil import copyfile, copytree

dest = "/mnt/c/Users/Zoe/Documents/dest/split"
#z.gsavedir = dest

z.getp("dates")
path = z.getPath("split")
try:
    copytree(path, dest)
except:
    pass
print ("finished split")

dest = "/mnt/c/Users/Zoe/Documents/dest"
getpd = z.getp("getpd")
for name in getpd:
    path = z.getPath("{}/{}.pkl".format("pkl", name))
    newpath = "{}/{}.pkl".format(dest, name)

    if not os.path.exists(newpath):
        print("newpath : {}".format( newpath ))
        copyfile(path, newpath)
