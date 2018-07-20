import sys
import os
import subprocess
import opened

def appendRecent(ftype, fpath):
    aFile = "E:\\recent\\{}.txt".format(ftype)
    f = open(aFile, "r+")
    lines = f.read().split('\n')
    if fpath in lines:
        lines.remove(fpath)
    lines.append(fpath)
    print (lines)
    f.seek(0)
    f.write("{}".format("\n".join(lines)))
    f.truncate()
    f.close()

def openForMe(fileArg):
    cmd = ""
    if ".pdf" in fileArg:
        appendRecent("pdf", fileArg)
        cmd = 'C:\\Program Files (x86)\\FOXIT SOFTWARE\\FOXIT READER\\Foxit Reader.exe {}'.format(fileArg)
    elif ".blend" in fileArg:
        cmd = "E:\\Program Files\\Blender Foundation\\Blender\\blender.exe {}".format(fileArg)
    
    if cmd:
        subprocess.Popen(cmd)

if __name__ == "__main__":
    openForMe(sys.argv[1])

