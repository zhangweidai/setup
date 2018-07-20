import sys
if len(sys.argv) == 3:
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    modx = x + 100
    mody = y - 50
    aFile = "C:\\Users\\Peter\\Documents\\GitHub\\setup\\blender\\ahk\\myscript.ahk"
    f = open(aFile, "r+")
    lines = f.read().split('\n')
    newwrite = list()
    skipNext = False
    for r,aline in enumerate(lines):
        if skipNext: 
            skipNext = False
            continue
        newwrite.append(aline)
        if "XXX2" in aline:
            newwrite.append("MouseMove, {}, {}".format(str(modx), str(mody)))
            skipNext = True
        elif "XXX" in aline:
            newwrite.append("MouseMove, {}, {}".format(str(x), str(y)))
            skipNext = True
    f.seek(0)
    f.write('\n'.join(newwrite))
    f.close()
