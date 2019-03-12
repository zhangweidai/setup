"""
Show how to connect to keypress events
"""
from __future__ import print_function
import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from util import getCsv, getStocks, trimStock, getTrimStock
import util
from matplotlib.pyplot import figure
from tkinter import simpledialog; 
from pyutil import Modes, Zen, settings
import pyutil

currentMode = Modes.none

lap = True
if lap:
    plt.rcParams["figure.figsize"] = [11,6]
    xcount = 7
else:
    plt.rcParams["figure.figsize"] = [16,10]
    xcount = 10

#stocks = getCsv("analysis/why_buy_these.csv", 0)
stocks = getStocks(dev=True)
#stocks = [stock.split("/")[-1] for stock in stocks]


stock_count = len(stocks)
start = None
end = None
ax = None

def getCurrentStock():
    return stocks[current_idx]

values = None
df = None
dates = None
csvColumn = "Close"
endx = 0
maxvalues = 0
def rebuild(start = None, end = None):
    global ax, values, df, dates, maxvalues
    ax.cla()
    astock = stocks[current_idx]
    df = getCsv(astock)
    maxvalues = len(df)
    df = df[start:end]
    values = df[csvColumn].tolist()
    ax.plot(df["Low"].tolist())
    ax.plot(df["High"].tolist())
    ax.plot(values)

    if currentMode == Modes.average:
        ax.plot(pyutil.averageValues(values))

    ax.set_title(astock)

    startx = 0 
    endx = len(values)-1

    byx = int((endx-startx)/xcount)
    dates = df['Date'].tolist()

    xranges = [i for i in range(startx, endx, byx)]
    xlabels = [ "{}\n({})".format(i,dates[i]) for i in xranges]
    plt.xticks( xranges, xlabels)

    fig.canvas.draw()
    fig.canvas.get_tk_widget().focus_set()
                
def nexti():
    global current_idx
    if current_idx+1 < stock_count:
        current_idx += 1
        rebuild()

def previ():
    global current_idx
    if current_idx > 0:
        current_idx -= 1
        rebuild()

def interpret(answer):
    if answer == "reset":
        util.resetStock(getCurrentStock())
        rebuild()
    elif "recent" in answer:
        count = 15
        try: count = int(answer.split(' ')[1])
        except: pass
        rebuild(maxvalues-count, maxvalues)

def setCurrentMode(mode):
    global currentMode
    currentMode = mode
    rebuild()

def press(event):
    if len(event.key) == 1:
        try: press.last += event.key
        except: press.last = event.key
    if len(press.last) > 3: press.last = press.last[1:]

    global current_idx, fig, currentMode

    if press.last == "aa" or press.last == "aaa":
        press.last = ""
    elif press.last == "avg":
        setCurrentMode(Modes.average)
    elif press.last == "cle" or press.last == "cls":
        setCurrentMode(Modes.none)

    print('press', event.key)
    print(press.last)

    sys.stdout.flush()
#        visible = xl.get_visible()
#        xl.set_visible(not visible)
#    if event.key == 'left':
    if event.key == 'q':
        settings(Zen.lastStock, value=current_idx)
    # zz
    elif event.key == 'z':
        if not currentMode == Modes.zoom:
            currentMode = Modes.zoom
        else:
            rebuild()
            currentMode = Modes.none
    elif event.key == 'x':
        from pyutil import restart_program
        settings(Zen.lastStock, current_idx)
        restart_program()
    elif event.key == '0':
        current_idx = 0
        rebuild()
    elif event.key == '9':
        multiPlot()
    elif event.key == 'j':
        nexti()
    elif event.key == 'k':
        previ()
    elif event.key == 't':
        currentMode = Modes.trim
    elif event.key == ' ':
        answer = simpledialog.askstring("Advanced", "cmd:", parent = None)
        try:
            interpret(answer)
        except:
            pass
        fig.canvas.get_tk_widget().focus_set()
#            trimStock(getCurrentStock(), answer)
#            rebuild()
def handle_close(evt):
    settings(Zen.lastStock, value=current_idx)

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

xl = None
fig = None

savedxdata = None
#xadjust = 0
def onrelease(event):
    global values, currentMode
    if not savedxdata:
        return

    print("event: {}".format(event.xdata))
    print("savedxdata: {}".format( savedxdata))
    leng = len(values)
    if event.xdata > leng or savedxdata > leng:
        currentMode = Modes.none
        return

    x1 = int(event.xdata) 
    print("x1 : {}".format( x1 ))
    x2 = int(savedxdata) 
    print("x2 : {}".format( x2 ))
    endx = len(values)
    print("leng : {}".format( endx ))
    answer = values[x1] / values[x2]
    date1 = dates[x2]
    date2 = dates[x1]
#    date1 = df["Date"][x2]
#    date2 = df["Date"][x1]
    value1 = values[x1]
    value2 = values[x2]
#    value1 = df["Close"][x2]
#    value2 = df["Close"][x1]
    print ("\nChange: {}".format(util.formatDecimal(answer)))
    print ("Start : {}({})".format( date1, value1 ))
    print ("End   : {}({})".format( date2, value2 ))
    print ("Days  : {}".format( x1-x2 ))
    if currentMode == Modes.zoom:
        xadjust = x2
        rebuild(x2, x1)
        currentMode = Modes.none

def onclick(event):
    global df, savedxdata
    savedxdata = event.xdata
    print("savedxdata : {}".format( savedxdata ))
#    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#          ('double' if event.dblclick else 'single', event.button,
#           event.x, event.y, event.xdata, event.ydata))
    if currentMode == Modes.trim:
        astock = getCurrentStock()
        trimStock(astock, int(event.xdata))
        rebuild()
#print (getTrimStock("VST"))
def configurePlots(fig, ax):
    adjust = 0.10
    fig.subplots_adjust(left=adjust, bottom=adjust, 
                        right=1-adjust, top=1-adjust)

    move_figure(fig, 1920, 0)
    move_figure(fig, 0, 0)
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('scroll_event', handle_scroll)
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('button_release_event', onrelease)
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.mpl_connect('mouse_move_event', handle_close)


def multiPlot():
    global fig, ax
    plt.close(fig)
    fig, ax = plt.subplots(nrows=2, ncols=2)
    configurePlots(fig, ax)
    plt.show()

#plt.get_current_fig_manager().window.wm_geometry("+0+0")
def plot(astock, start = None, end = None):
    global xl, fig, ax, df, values

    df = getCsv(astock)
    df = df[start:end]
    values = df[csvColumn].tolist()
    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots()
    configurePlots(fig, ax)
    rebuild()

    plt.show()

try:
    current_idx = settings(Zen.lastStock, default=0)
    plot(stocks[current_idx])
except:
    pass


