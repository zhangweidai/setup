#!/usr/bin/python3
import sys
import subprocess

try:
    script_name = sys.argv[1]

    cmd = "cp template.py {}.py".format(script_name)
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    
    cmd = "ln -s {}.py {}".format(script_name, script_name)
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    cmd = "git add {}.py".format(script_name)
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    cmd = "git add {}".format(script_name)
    cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
except Exception as e:
    print (e)
    print ("wrong usage")
    pass
