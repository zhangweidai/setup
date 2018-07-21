import sys
import tkinter as tk  
from tkinter import *

import random
import opened
import os

from TkinterDnD2 import *

def endapp():
    root.withdraw() # if you want to bring it back
    root.quit()
    os.system("taskkill /f /fi \"Windowtitle eq C:\WINDOWS\system32\cmd.exe\"")
    os.system("taskkill /f /fi \"Windowtitle eq C:\WINDOWS\system32\cmd.exe\"")

root = TkinterDnD.Tk()

# width x height + x_offset + y_offset:
root.geometry("880x450+300+300") 
     
def getContents(ftype):
    aFile = "E:\\recent\\{}.txt".format(ftype)
    f = open(aFile, "r")
    return f.read().split('\n')

# from colorama import Fore, Back, Style
# from colorama import init
# init()

# cache = dict()
mode = None
def process(ftype):
    global lb, mode
    mode = ftype
    lb.delete(0, END)
    files = reversed(getContents(ftype))

    for f in files:
        if f:
            lb.insert(END, f)

    cs = lb.curselection()
    if not cs:
        lb.select_set(0)


l = StringVar()
def keyPressInput(event):
    global e, l, lb

    if event.keysym in ('Enter', 'Return'):
        value = str((lb.get(ACTIVE)))
        opened.openForMe(value)
        endapp()

    text = e.get()
    if text == 'p' or text == "pd" or text == "pdf":
        process("pdf")
        if text == "pdf":
            lb.focus_set()
    elif not text:
        lb.delete(0, END)

def appendRecent(ftype, fpath):
    aFile = "E:\\recent\\{}.txt".format(ftype)
    f = open(aFile, "r+")
    lines = f.read().split('\n')
    if fpath in lines:
        lines.remove(fpath)
    lines.append(fpath)

    if "" in lines:
        lines.remove("")

    f.seek(0)
    f.write("{}".format("\n".join(lines)))
    f.truncate()
    f.close()


def keyPressList(event):
    global lb
    cs = lb.curselection()
    index = cs[0]
#     print("index")
#     print(index)
    if event.keysym in ('j') and index + 1 < lb.size():
        index = index + 1
    elif event.keysym in ('k') and index >= 1:
        index = index - 1
    elif event.keysym in ('Enter', 'Return'):
        value = str((lb.get(ACTIVE)))
        opened.openForMe(value)
        endapp()
#        appendRecent(mode, value)

    lb.select_clear(0, END)
    lb.select_set(index)
    lb.activate(index)
#         lb.insert(END, "so far so godo {}".format(str(
#                         )))


# search
Label(root, textvariable=l, font="Courier 20").grid(row=1, column=0)
l.set("Open:")

v = StringVar()
e = Entry(root, textvariable=v, font = "Courier 14",justify="center",width=70)
e.grid(row=1, column=1)
e.focus_set()
e.bind('<KeyRelease>', keyPressInput)
lb = Listbox(root,width=80, height=50, font="Courier 14")
lb.bind('<KeyRelease>', keyPressList)
lb.grid(row=2, column=0, columnspan=3)

def onClose(event):
    endapp()

root.bind('<Escape>', onClose)

root.mainloop()
