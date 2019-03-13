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

def getCurrentStock():
    return stocks[idx]

def updateTitle(force_ax = None):
    global ax
    local_ax = ax
    if force_ax is not None:
        local_ax = force_ax

    addl = ""
    if Modes.target in currentMode:
        addl += "(TARGET)"
    if Modes.trim in currentMode:
        addl += "(TRIM)"
    local_ax.set_title("{}{}".format(getCurrentStock(), addl))
    fig.canvas.draw()


def rebuild(start = None, end = None, 
        force_ax = None,
        force_idx = None
        ):
    global ax, values, df, dates, maxvalues, idx, stocks
    local_ax = ax
    local_idx = idx
    if force_ax is not None: local_ax = force_ax
    if force_idx: local_idx = force_idx

    local_ax.cla()
    astock = stocks[local_idx]
    df = getCsv(astock)
    maxvalues = len(df)

    if Modes.recent in currentMode:
        start = maxvalues-rebuild.recentIncrement

    df = df[start:end]
    values = df[csvColumn].tolist()
    local_ax.plot(values)

    if Modes.more in currentMode:
        local_ax.plot(df["Low"].tolist(), linewidth = .5)
        local_ax.plot(df["High"].tolist(), linewidth = .5)

    if Modes.change in currentMode:
        modified = pyutil.averageValues(pyutil.changeValues(values))
        local_ax.plot(modified)
        local_ax.axhline(y=1)
    else:
        local_ax.plot(values)

    if Modes.average in currentMode:
        local_ax.plot(pyutil.averageValues(values))

    updateTitle(force_ax)

    startx = 0 
    endx = len(values)-1

    try: plt.scatter( endx, util.getTargetPrice(astock)[0], s=80, 
            color="red")
    except Exception as e:
        pass
#        print ('TargetPrice : '+ str(e))

    byx = int((endx-startx)/xcount)
    try:
        dates = df['Date'].tolist()
    except Exception as e:
        print ('Deleting : '+ str(e))
        print (astock)
        util.delStock(astock)
        stocks = getStocks(reset=True)
        idx += 1
        rebuild()
        return

    if not byx:
        byx = 1
    xranges = [i for i in range(startx, endx+1, byx)]
    xlabels = [ "{}\n({})".format(i,dates[i]) for i in xranges]
    plt.xticks( xranges, xlabels)

    fig.canvas.draw()
    fig.canvas.get_tk_widget().focus_set()
rebuild.recentIncrement = 35
                
def nexti():
    global idx
    if idx+1 < stock_count:
        idx += 1
        rebuild()

def previ():
    global idx
    if idx > 0:
        idx -= 1
        rebuild()

def interpret(answer):
    global idx, stocks
    print("answer: {}".format( answer))
    if answer == "reset":
        util.resetStock(getCurrentStock())
        rebuild()
#    elif "recent" in answer:
#        count = 15
#        try: count = int(answer.split(' ')[1])
#        except: pass
#        rebuild(maxvalues-count, maxvalues)
    else:
        try:
            idx = stocks.index(answer.upper())
            print("idx : {}".format(idx))
        except:
            try:
                answer = answer.upper()
                util.saveProcessedFromYahoo(answer, csvdir = "csv", add=True)
                stocks = getStocks()
                if answer in stocks:
                    print ("so far so good")
            except Exception as e:
                print ('Failed2: '+ str(e))
                pass
        rebuild()

def setCurrentMode(mode, build = True):
    global currentMode
    currentMode ^= mode
    if build:
        rebuild()
    else:
        updateTitle()

def press(event):
    if len(event.key) == 1:
        try: press.last += event.key
        except: press.last = event.key
    else : 
        return
    try: 
        if len(press.last) > 3 and len(event.key) == 1: 
            press.last = press.last[1:]
    except : pass

    global idx, fig, currentMode

    if press.last == "aa" or press.last == "aaa":
        press.last = ""
    elif press.last == "avg":
        setCurrentMode(Modes.average)
    elif press.last == "cle" or press.last == "cls":
        setCurrentMode(Modes.none)
    elif press.last == "mor":
        setCurrentMode(Modes.more)
    elif press.last == "cha":
        setCurrentMode(Modes.change)
    elif press.last == "tar":
        setCurrentMode(Modes.target, build=False)
    elif press.last == "rec":
        setCurrentMode(Modes.recent)
    elif press.last == "tri":
        setCurrentMode(Modes.trim, build=False)

    print("last press :{}".format(press.last))

    sys.stdout.flush()
#        visible = xl.get_visible()
#        xl.set_visible(not visible)
#    if event.key == 'left':
    if event.key == 'q':
        saveSettings()

    # zz
    elif event.key == 'z':
        if not currentMode == Modes.zoom:
            currentMode = Modes.zoom
        else:
            rebuild()
            currentMode = Modes.none
    elif event.key == 'x':
        from pyutil import restart_program
        saveSettings()
        restart_program()

    elif event.key == '0':
        idx = 0
        rebuild()
    elif event.key == '9':
        multiPlot()
    elif event.key == 'j':
        nexti()
    elif event.key == 'k':
        previ()
    elif event.key == ' ':
        answer = simpledialog.askstring("Advanced", "cmd:", parent = None)
        try:
            interpret(answer)
        except Exception as e:
            print ('Failed2: '+ str(e))
            pass
        fig.canvas.get_tk_widget().focus_set()

    handleIncrease(event.key)
press.last = ""

def handle_close(evt):
    saveSettings()

def handleIncrease(key):
    if key == '=':
        if Modes.average in currentMode:
            pyutil.increaseAvg(True)
        if Modes.recent in currentMode:
            rebuild.recentIncrement += 5
        rebuild()
    elif key == '-':
        if Modes.average in currentMode:
            pyutil.increaseAvg(False)
        if Modes.recent in currentMode and rebuild.recentIncrement > 6:
            rebuild.recentIncrement -= 5 
        rebuild()

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
    global values, currentMode
    if not savedxdata:
        return

#    print("event: {}".format(event.xdata))
#    print("savedxdata: {}".format( savedxdata))
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
    value1 = values[x2]
    value2 = values[x1]
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
    if Modes.target in currentMode and event.ydata:
        util.setTargetPrice(getCurrentStock(), round(event.ydata,3))
        nexti()
        return

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
def configurePlots(fig):
    adjust = 0.10
    fig.subplots_adjust(left=adjust, bottom=adjust, 
                        right=1-adjust, top=1-adjust)

#    move_figure(fig, 1920, 0)
    move_figure(fig, 0, 0)
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('scroll_event', handle_scroll)
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('button_release_event', onrelease)
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.mpl_connect('mouse_move_event', handle_close)

multiax = None
def updateMultiPlot():
    next_idx = idx
    for ax1 in multiax:
        for ax2 in ax1:
            rebuild(force_ax = ax2, force_idx = next_idx)
            next_idx += 1

def multiPlot():
    global fig, multiax
    plt.close(fig)
    fig, multiax = plt.subplots(nrows=2, ncols=2)
    configurePlots(fig)
    updateMultiPlot()
    plt.show()

#plt.get_current_fig_manager().window.wm_geometry("+0+0")
def plot(astock, start = None, end = None):
    global xl, fig, ax, df, values

    df = getCsv(astock)
    df = df[start:end]
    values = df[csvColumn].tolist()
    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots()
    configurePlots(fig)
    rebuild()

    plt.show()

def saveSettings():
    donotPersist = [Modes.target, Modes.trim]
    global currentMode
    settings(Zen.lastStock, setValue = idx)
    for mode in donotPersist:
        if mode in currentMode:
            currentMode ^= mode
    settings(Zen.lastMode, setValue = currentMode)
    util.saveTargets()

if __name__ == "__main__":
    currentMode = settings(Zen.lastMode, default=Modes.none)
    lap = False
    if lap:
        plt.rcParams["figure.figsize"] = [11,6]
        xcount = 7
    else:
        plt.rcParams["figure.figsize"] = [16,10]
        xcount = 10

    stocks = getStocks()
    stock_count = len(stocks)
    start = None
    end = None
    ax = None
    values = None
    df = None
    dates = None
    csvColumn = "Close"
    endx = 0
    maxvalues = 0
    xl = None
    fig = None
    savedxdata = None

    try:
        idx = settings(Zen.lastStock, default=0)
        plot(stocks[idx])
    except Exception as e:
        print ('Failed3: '+ str(e))
        pass

