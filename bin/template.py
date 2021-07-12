#!/usr/bin/python3
import sys
import subprocess

try:
    cmd = "ctags -R --language-force=python -f ../tagme.tag `pwd`"
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

except Exception as e:
    print (e)
    print ("wrong usage")
    pass

