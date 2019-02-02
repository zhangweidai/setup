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

dirs = list()
i = 0
for b in read:
    printme = os.path.dirname(b)
    if printme in dirs:
        continue

    if not os.path.exists(printme):
        continue

    i = i + 1

    if query == i:
        print printme
        exit()

    if printFiles:
        print "{} {}".format(i, printme)

    dirs.append(printme)
    if len(dirs) > 30:
        break;

