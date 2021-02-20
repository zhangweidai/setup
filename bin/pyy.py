#!/usr/bin/python3

import os
import sys
printFiles = False
query = -1
if len(sys.argv) == 1:
    printFiles = True
else:
    query = int(sys.argv[1])

mru_path = os.path.expanduser("~/.vim_mru_files")
if not os.path.exists(mru_path):
    mru_path = "/mnt/c/Users/Peter/.vim_mru_files"

with open(mru_path) as f:
    read = f.readlines()
    lastfile = read[1].split(".")[-1]
    print("lastfile : {}".format( lastfile ))
    if "py" in lastfile:
        print ("read[1]")
        os.system("python3 {}".format(os.path.expanduser(read[1])))
    else:
        print ("read[]")
        print (read[1])

