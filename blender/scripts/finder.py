import sys
import tkinter as tk  
from tkinter import *
import random
import os

mode = "py"

from TkinterDnD2 import *

root = TkinterDnD.Tk()

droppedVar = StringVar()
droppedVar.set("Drop Here")

def onDrop(event):
    droppedVar.set(event.data)
# width x height + x_offset + y_offset:
root.geometry("470x270+1300+300") 
     
# languages = ['Python','Perl','C++','Java','Tcl/Tk']
# labels = range(5)
# for i in range(5):
#    ct = [random.randrange(256) for x in range(3)]
#    brightness = int(round(0.299*ct[0] + 0.587*ct[1] + 0.114*ct[2]))
#    ct_hex = "%02x%02x%02x" % tuple(ct)
#    bg_colour = '#' + "".join(ct_hex)
#    l = tk.Label(root, 
#                 text=languages[i], 
#                 fg='White' if brightness < 120 else 'Black', 
#                 bg=bg_colour)
#    l.place(x = 20, y = 30 + i*30, width=120, height=25)
def getContents(aFile):
     f = open(str(aFile), "r")
     return f.read().split('\n')

from colorama import Fore, Back, Style
from colorama import init
init()

cache = dict()
def process(word):
    global cache, mode
    from pathlib import Path
    scripts = ""
    print (mode)
    if mode == "py":
        scripts = "/scripts/"
    folder = 'C:/Users/Peter/Documents{}'.format(scripts)
    print (folder)
    files = [f for f in Path(folder).glob("*.{}".format(mode)) if f.is_file()]
    counter = 1
    for aFile in files:
        contents = cache.setdefault(aFile), getContents(aFile)
        for r,aline in enumerate(contents):
            if aline == None:
                continue
            for x, whatline in enumerate(aline):
                if not whatline:
                    continue
                if word in whatline:
                    msg = "{:^4} {:50} :{:^3} {} {}".format(str(counter), str(aFile).ljust(40), str(x), Fore.GREEN+whatline, Style.RESET_ALL)
                    print (msg)
                    counter = counter + 1
    print ("\n")
             

l = StringVar()
def keyPress(event):
    global e, mode, l
    if event.keysym == 'Tab':
        if mode == "py":
            mode = "ahk"
        elif mode == "ahk":
            mode = "py"
    l.set("Search {}:".format(mode))

    if event.keysym in ('Enter', 'Return'):
        text = e.get()
#        print (int(text))
        process(e.get())
        v.set("")

def backupAction():
    from shutil import copytree, ignore_patterns, rmtree
    source = "C:/Users/Peter/Documents/scripts"
    dest = "C:/Users/Peter/Documents/GitHub/setup/blender/scripts"
    rmtree(dest, ignore_errors=True)
    copytree(source, dest, ignore=ignore_patterns('*.pyc', 'tmp*', "*.swp"))
    print ("clicked")

def restoreAction():
    print ("clicked")

# drop label
Label(root, textvariable=droppedVar, font="Helvetica 20").grid(row=0)

# search
Label(root, textvariable=l, font="Helvetica 20").grid(row=1, column=0)
l.set("Search {}:".format(mode))

v = StringVar()
e = Entry(root, textvariable=v, font = "Helvetica 20",justify="center",width=16)
e.drop_target_register(DND_FILES)
e.dnd_bind('<<Drop>>', onDrop)
e.grid(row=1, column=1)
e.focus_set()
e.bind('<KeyRelease>', keyPress)

separator = Frame(height=1, bd=4, padx=10, pady=10)
separator.grid(row=3)

backupButton = Button(separator, text="BackUp", command=backupAction, font="Helvetica 18", width=10)
restoreButton = Button(separator, text="Restore", command=restoreAction, font="Helvetica 18", width=10)
backupButton.pack()
LabelFrame(separator, height=20).pack()
restoreButton.pack()


# def callback():
#     print (e.get())
# 
# text = e.get()
# 
# def makeentry(parent, caption, width=None, **options):
#     Label(parent, text=caption).pack(side=LEFT)
#     entry = Entry(parent, **options)
#     if width:
#         entry.config(width=width)
#     entry.pack(side=LEFT)
#     return entry
# 
# user = makeentry(root, "User name:", 10)
# password = makeentry(root, "Password:", 10, show="*")
# caption = "asdfaDSF"
# content = StringVar()
# entry = Entry(root, text=caption, textvariable=content)
# 
# text = content.get()
# content.set(text)

def onClose(event):
    root.withdraw() # if you want to bring it back
    root.quit()
    os.system("taskkill /f /fi \"Windowtitle eq C:\WINDOWS\system32\cmd.exe\"")
    os.system("taskkill /f /fi \"Windowtitle eq C:\WINDOWS\system32\cmd.exe\"")
#     sys.exit() # if you want to exit the entire thing
#    exit()


root.bind('<Escape>', onClose)

root.mainloop()
