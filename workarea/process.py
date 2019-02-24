import os
import sys
print sys.version_info

skipped = ["Meta Event", "Text type", "Time signature", "Key "]
sub = {
        "Channel volume":"l", 
        "Instrument":"!", 
        "Tempo":")", 
        "End of track":"(", 
        "format":"Z", 
        "tracks":"|", 
        "division":"_", 
        "BA":"z", 
        "CR": "q", 
        "TR": "w", 
        "NT": "y", 
        "CH": "?",
        "ST": "x",
        "von=": "@"}

if len(sys.argv) == 1:
    print "need a file"
    raise SystemExit

filename = sys.argv[1]
if not os.path.exists(filename):
    print "need a file"
    raise SystemExit

with open(filename, "r") as f:
    read = f.readlines()

newfile = filename + ".doesthiswor"
with open(newfile, "w") as f:
    for line in read:
        skipping = False
        if len(line) == 1:
            continue

        if line[0] =="#":
            continue

        for skip in skipped:
            if skip in line:
                skipping = True
                break

        if skipping:
            continue

        line = ' '.join(line.split())
        f.write(line + "\n")


newfile = filename + ".filt"
with open(newfile, "w") as f:
    for line in read:
        skipping = False
        if len(line) == 1:
            continue

        if line[0] =="#":
            continue

        for skip in skipped:
            if skip in line:
                skipping = True
                break

        if skipping:
            continue

        updatedline = ' '.join(line.split())

        for key in sub.iterkeys():
            updatedline = updatedline.replace(key, sub[key])

        f.write(updatedline + "\n")
