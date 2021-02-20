#!/usr/bin/python3
import os
import subprocess
from subprocess import Popen
cmd = "echo `xclip -o`"
cmd = Popen(cmd, shell=True, stdout=subprocess.PIPE)
#cmd_out = str(cmd.stdout.read())
bar = str(cmd.stdout.read())
bar = os.path.expanduser(bar[2:-3])
if os.path.isfile(bar):
    print(os.path.dirname(bar))
else:
    if os.path.exists(bar):
        print (bar)
    else:
        bar = os.path.dirname(bar)
        print (bar)
