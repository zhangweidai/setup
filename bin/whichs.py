#!/usr/bin/python3
import sys
import inspect
try:
    path = inspect.getsourcefile(eval(sys.argv[1]))
except:
    path = sys.argv[1]
    pass
import os
if not os.path.exists(path):
    cmd = "which {}".format(path)
    import subprocess
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    bar = str(cmd.stdout.read())
    path = os.path.expanduser(bar[2:-3])

if os.path.exists(path):
    os.system("echo {}".format(path))
