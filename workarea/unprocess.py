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

newfile = "finished_" + filename
with open(newfile, "w") as f:
    for line in read:
        skipping = False

        for value in sub.itervalues():
            key = sub.keys()[sub.values().index(value)]
            line = line.replace(value, key)

        f.write(line)
