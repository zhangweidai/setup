#!/usr/bin/python3
import sys
import time
import os.path
cpath = os.path.splitext(sys.argv[1])[0]
from subprocess import Popen
from itertools import islice

cf_path = "{}.cf".format(cpath)
print("cf_path : {}".format( cf_path ))
cfdg_path = "{}.cfdg".format(cpath)
print("cfdg_path : {}".format( cfdg_path ))

name = os.path.splitext(cfdg_path)[0]
name = os.path.basename(name)
new_file = "/mnt/c/temp/{}.png".format(name)
cmd="cfdg {} --width=2560 --height=1440 --minimumsize=2 -o {}".format(cfdg_path, new_file)
os.system(cmd)

#print("new_file: {}".format( new_file))
#parent = os.path.dirname(new_file)
#cmd="cd {}; wslview {}.png".format(parent, name)
#os.system(cmd)
exit()

#print (sys.argv[1])
#destination = "/tmp/out.cfdg"
with open(cf_path, "r") as f:
    bar = f.readlines()
values = dict()
variables = list()
ranges = dict()
args = None
for aline in bar:

    if aline and aline[0] == "#":
        continue

    if not args:
        args = aline
        continue

    if ":" in aline:
        tokens = aline.split(":")
        val = tokens[1][:-1]
        key = tokens[0]
        if " " in val:
            ranges[key] = val.strip().split(" ")
        else:
            values[key] = val

needed = int(values['duration']) * int(values['fps'])
for key,var in ranges.items():
    start = float(var[1])
    stop  = float(var[0])
    iteration =  (stop-start)/needed
    ranges[key] = [start, iteration]

print("needed : {}".format( needed ))

cmd="rm /mnt/c/temp/bar* -rf"
os.system(cmd)

commands = list()
for i, it in enumerate(range(needed)):
    addline = []
    for key,var in ranges.items():
        value = round(((i + 1) * var[1]) + var[0],4)
        addline.append("-D{}={}".format(key, value))
    cmd="cfdg {} {} {} -o /mnt/c/temp/bar{}.png".format(cfdg_path, args[:-1], " ".join(addline), str(i).zfill(3))
    commands.append(cmd)
#    os.system(cmd)

max_workers = 10  # no more than 2 concurrent processes
processes = (Popen(cmd, shell=True) for cmd in commands)
running_processes = list(islice(processes, max_workers))  # start new processes
while running_processes:
    for i, process in enumerate(running_processes):
        if process.poll() is not None:  # the process has finished
            running_processes[i] = next(processes, None)  # start new process
            if running_processes[i] is None: # no new processes
                del running_processes[i]
                break

cmd="ffmpeg -i /mnt/c/temp/bar%3d.png -r {} /mnt/c/outputs/test_{}.avi".format(values['fps'], str(int(time.time())))
os.system(cmd)

#cmd="cfdg $1 --width=2560 --height=1440 --minimumsize=2 -DloopN=3 -o /mnt/c/temp/bar.jpg
#for need in range(needed):
#    print("need : {}".format( need ))
#
#for aline in bar:
#    print("aline : {}".format( aline ))
