import subprocess
import re

def buy(what):
    print what


st = ""
import readchar
key = ''
while key != 'q':
    # prevents lots of python error output
    try:
        key = readchar.readkey()
        print key
    except:
        break

    # check if you should exit
#     lower = s.strip().lower() 
#     if lower == 'exit' or lower == 'e':
#         break

    if key == 'b':
        buy = True
    else:
        st = st + key


    # try to run command
#     try:
#         cmd = subprocess.Popen(re.split(r'\s+', s), stdout=subprocess.PIPE)
#         cmd_out = cmd.stdout.read()
# 
#         # Process output
#         print cmd_out
# 
#     except OSError:
#         print 'Invalid command'
