"""
Show how to connect to keypress events
"""

import sys
import matplotlib
#import numpy as np
import matplotlib.pyplot as plt
import z
from matplotlib.pyplot import figure
from tkinter import simpledialog
import os
from rows import *

increment = 10
default = 107 
start = default 
dates = z.getp("dates")
end = start
ax = None
ax2 = None
fig = None
astock = None
lastworking = None
ref_astock = "USMV"

import math

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def rebuild():
    global ax, fig, astock, start, lastworking, ax2

    values = list()
    istart = start * -1
    startdate = dates[istart]
    for i, row in enumerate(getRowsRange(astock, count=end, date=startdate)):
        c_close = float(row[z.closekey])
        values.append(c_close)

    fv = values[0]
    v1 = [ round((i/fv)-1,3) for i in values ]

    refvalues = list()
    for i, row in enumerate(getRowsRange(ref_astock, count=end, date=startdate)):
        c_close = float(row[z.closekey])
        refvalues.append(c_close)

    fv = refvalues[0]
    v2 = [ round((i/fv)-1,3) for i in refvalues ]

    minv = min(v1)
    maxv = max(v1)

    minvr = min(v2)
    maxvr = max(v2)

    maxv = maxv if maxv > maxvr else maxvr
    minv = minv if minv < minvr else minvr

    minv = minv if minv < -.2 else -.2
    maxv = maxv if maxv > .2 else .2

#    print("maxv {}    minv {}".format( maxv, minv ))

    iend = istart + end
    if iend == 0:
        iend = None

    try:
        date_range = dates[istart:iend]
        xranges = [i for i in range(0, end, round(end/9))]
        xlabels = ["{}\n({})".format(i, date_range[i]) for i in xranges]
    except:
        start = lastworking
        rebuild()
        return

    lastworking = start

    ax.cla()
    ax.set_title("{} {}".format(astock, startdate))
    color = 'tab:green'
    ax.set_ylabel(astock, color=color)  # we already handled the x-label with ax1
    ax.set_ylim([minv,maxv])

    ax.plot(v1, color=color)

    if ax2 is None:
        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.cla()
    color = 'tab:blue'
    ax2.set_ylabel(ref_astock, color=color)  # we already handled the x-label with ax1
    ax2.plot(v2, color=color)
    ax2.set_ylim([minv,maxv])

    ax.set_xticklabels(xlabels)
    ax.set_xticks(xranges)

    fig.tight_layout()
    fig.canvas.draw()
    fig.canvas.get_tk_widget().focus_set()

def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except:
        pass
#        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)

def updateTitle(force_ax = None, force_idx = None):
    global ax
    local_ax = force_ax if force_ax is not None else ax

    addl = ""
    local_ax.set_title("{}{}".format(getCurrentStock(force_idx), addl))
    fig.canvas.draw()


def nexti():
    global start
    start += increment
    rebuild()

def previ():
    global start
    start -= increment
    if start < default:
        start = default
    rebuild()

marked = []
def interpret(answer):
    global idx, stocks, previdx, stock_count, setstart_date, loadFrom
    print("answer: {}".format( answer))
    if not answer:
        return

    if "regen" in answer:
        import regen_stock
        regen_stock.process(astock)
        rebuild()

    elif "reset" in answer:
        stock = getCurrentStock()


    elif "newscore" in answer:
        resetStocks()

    elif "sets" in answer:
        setstart_date = df.at[0,"Date"]

    elif "load" in answer:
        pckl = answer.split(" ")[1]
        loadFrom = pckl
        resetStocks()

    else:
        previdx = idx
        answer = answer.upper()

def setCurrentMode(mode, build = True):
    if mode not in currentMode:
        toggleCurrentMode(mode, build)

def toggleCurrentMode(mode, build = True):
    global currentMode, ivvonly
    currentMode ^= mode

def handleModifier(key):
    print("key: {}".format( key))

def handleSelectionMode(increment = 1):
    pass

def press(event):
    if event.key and len(event.key) == 1:
        try: press.last += event.key
        except: press.last = event.key
    else : 
        handleModifier(event.key)
        return
    try: 
        if len(press.last) > 3 and len(event.key) == 1: 
            press.last = press.last[1:]
    except : pass

    print("last press :{}".format(press.last))

    global idx, fig, currentMode, stocks, ivvonly, start, end, increment

    sys.stdout.flush()

    print(event.key)

    if event.key == 'q':
        exit()
        return

    elif event.key == '=':
        start += 20
        end += 20
        increment += 5
        rebuild()

    elif event.key == '-':
        start -= 20
        end -= 20
        increment -= 5
        rebuild()


    elif event.key == '`':
        handleSort()

    # zz
    elif event.key == 'z':
        return

    elif event.key == 'x':
        restart_program()

    elif event.key == '9':
        start = 600
        end = 600
        increment = 50
        rebuild()

    elif event.key == '0':
        start = default
        end = default
        increment = 10
        rebuild()

    elif event.key == 'k':
        previ()
    elif event.key == ' ':
        answer = simpledialog.askstring("Advanced", "cmd:", parent = None, initialvalue=None)
        try:
            interpret(answer)
            press.prevanswer = answer
        except Exception as e:
            import traceback
            print (traceback.format_exc())
            print ('Failed2: '+ str(e))
            pass
        fig.canvas.get_tk_widget().focus_set()

    handleIncrease(event.key)

press.last = ""

def handle_close(evt):
    print ("Closing")
#    saveSettings()

def handleIncrease(key):
    print("key: {}".format( key))

def handle_scroll(evt):
    if evt.button == "up":
        nexti()
    else:
        previ()

def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK. You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)

def onrelease(event):
    return

def sonrelease(event):
    x1 = int(event.xdata) 
#    print("x1 : {}".format( x1 ))
    x2 = int(savedxdata) 
#    print("x2 : {}".format( x2 ))
    endx = len(values)
#    print("leng : {}".format( endx ))
    answer = values[x1] / values[x2]
    date1 = dates[x2]
    date2 = dates[x1]
#    date1 = df["Date"][x2]
#    date2 = df["Date"][x1]
    value1 = values[x2]
    value2 = values[x1]
#    value1 = df["Close"][x2]
#    value2 = df["Close"][x1]
    print ("Start : {}({})".format( date1, value1 ))
    print ("End   : {}({})".format( date2, value2 ))
    print ("Days  : {}".format( x1-x2 ))

def onclick(event):
    return

def configurePlots(fig):
#    adjust = 0.25
#
#    fig.subplots_adjust(left=adjust, bottom=adjust, 
#                        right=1-adjust, top=1-adjust)

#    move_figure(fig, 1920, 0)
#    move_figure(fig, 0, 0)
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('scroll_event', handle_scroll)
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('button_release_event', onrelease)
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.mpl_connect('mouse_move_event', handle_close)

multiax = None
def updateMultiPlot(titlesOnly = False):
    next_idx = idx
    for ax1 in multiax:
        for next_ax in ax1:
            if titlesOnly:
                updateTitle(force_ax = next_ax, force_idx = next_idx)
            next_idx += 1

def multiPlot():
    global fig, multiax, xcount, idx
    xcount = 3
    plt.close(fig)
    fig, multiax = plt.subplots(nrows=3, ncols=3)
    configurePlots(fig)
    updateMultiPlot()
    plt.show()

#plt.get_current_fig_manager().window.wm_geometry("+0+0")
def plot():
    global ax, fig, astock
    fig, ax = plt.subplots()
    configurePlots(fig)
    rebuild()
    plt.show()

def plotSelection(astock, local_ax, df):

    dates = list(df["Date"])
    print("dates : {}".format(len( dates)))
    for sel in sels:
        try :
            starti = dates.index(sel)
            print("sel: {}".format( sel))
            print("starti : {}".format( starti ))
            local_ax.scatter(starti, 0, s=80, color="orange")
        except:
            print ("todo {}".format(astock))

if __name__ == "__main__":
    lap = False
    if lap:
        plt.rcParams["figure.figsize"] = [10,5]
        xcount = 7
    else:
        plt.rcParams["figure.figsize"] = [11,8]
#        plt.rcParams["figure.figsize"] = [16,10]
        xcount = 10

    import argparse
    plt.rcParams['toolbar'] = 'None'
    parser = argparse.ArgumentParser()
    parser.add_argument('helpers', type=str, nargs='?', default = "")
    parser.add_argument('refs', type=str, nargs='?', default = "")
    args = parser.parse_args()

    try:
        savedhelper = args.helpers
        args.helpers = args.helpers.upper()
        astock = args.helpers
    except:
        exit()

    print("astock : {}".format( astock ))
    exit()

    print("astock : {}".format( astock ))
    try:
        plot()
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        print ('Failed3: '+ str(e))
        pass

