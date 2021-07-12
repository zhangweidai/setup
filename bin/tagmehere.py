#!/usr/bin/python3
import sys
import subprocess
import os

try:
    name = os.path.basename(os.getcwd())
    dest = "/home/peter/gits/{}.tag".format(name)
    msg = "au WinEnter,BufRead,BufNewFile */gits/{}/*  set tags={}".format(name, dest)
# 
    cmd = "echo {} >> ~/.vimrc".format(msg)
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    cmd = "ctags -R --language-force=python -f {} `pwd`".format(dest)
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

except Exception as e:
    print (e)
    print ("wrong usage")
    pass

