#!/usr/bin/python3
import sys
import subprocess

try:
    cmd = "/home/peter/gits/wsl-open/wsl-open.sh "
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

except Exception as e:
    print (e)
    print ("wrong usage")
    pass

