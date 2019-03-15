"""
Show how to connect to keypress events
"""
import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from util import getCsv, getStocks, trimStock, getTrimStock
import util
from matplotlib.pyplot import figure
from tkinter import simpledialog; 
try:
    from pyutil import Modes, Zen, settings
    import pyutil
except
    pass

def getCurrentStock(force_idx = None):
    return stocks[force_idx or idx]

def updateTitle(force_ax = None, force_idx = None):
    global ax
    local_ax = force_ax if force_ax is not None else ax

    addl = ""
    if Modes.target in currentMode:
        addl += "(TARGET)"
    if Modes.trim in currentMode:
        addl += "(TRIM)"
    local_ax.set_title("{}{}".format(getCurrentStock(force_idx), addl))
    fig.canvas.draw()


def rebuild(start = None, end = None, 
        force_ax = None,
        force_idx = None):

    global ax, values, df, dates, maxvalues, idx, stocks
    local_ax = ax
    if not force_idx: force_idx = idx
    if force_ax is not None: local_ax = force_ax

    local_ax.cla()
    astock = stocks[force_idx]
    df = getCsv(astock)
    if df is None:
        return

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

    updateTitle(force_ax, force_idx)

    startx = 0 
    endx = len(values)-1

    try: local_ax.scatter(endx, util.getTargetPrice(astock)[0], s=80, color="red")
    except Exception as e: pass

    byx = int((endx-startx)/xcount)
    try:
        dates = df['Date'].tolist()
    except Exception as e:
        print ('Deleting : '+ str(e))
        print (astock)
        util.delStock(astock)
        stocks = getStocks(reset=True, ivv=ivvonly)
        idx += 1
        rebuild()
        return

    if not byx:
        byx = 1
    xranges = [i for i in range(startx, endx+1, byx)]
    xlabels = ["{}\n({})".format(i,dates[i]) for i in xranges]
#    plt.xticks( xranges, xlabels)
    if Modes.multi in currentMode:
        xlabels[1] = ""
        xlabels[2] = ""

    local_ax.set_xticklabels(xlabels)
    local_ax.set_xticks(xranges)

    fig.canvas.draw()
    fig.canvas.get_tk_widget().focus_set()
rebuild.recentIncrement = 35
                
def nexti():
    global idx
    increment = 1
    if Modes.multi in currentMode:
        increment = 8

    if idx + increment < stock_count:
        idx += increment
        updateDisplay()

def previ():
    global idx
    increment = 1
    if Modes.multi in currentMode:
        increment = 8

    if idx - increment >= 0:
        idx -= increment
        updateDisplay()

def interpret(answer):
    global idx, stocks
    print("answer: {}".format( answer))
    if not answer:
        return
    if answer == "reset":
        util.resetStock(getCurrentStock())
        rebuild()
    else:
        try:
            idx = stocks.index(answer.upper())
            print("idx : {}".format(idx))
        except:
            try:
                answer = answer.upper()
                util.saveProcessedFromYahoo(answer, add=True)
                stocks = getStocks(ivv=ivvonly)
            except Exception as e:
                print ('Failed2: '+ str(e))
                pass

        updateDisplay()

def setCurrentMode(mode, build = True):
    global currentMode, ivvonly
    currentMode ^= mode
    if build:
        updateDisplay()
    else:
        if Modes.multi in currentMode:
            updateMultiPlot(titlesOnly = True)
        else:
            updateTitle()
    ivvonly = Modes.history in currentMode

def press(event):
    if event.key and len(event.key) == 1:
        try: press.last += event.key
        except: press.last = event.key
    else : 
        return
    try: 
        if len(press.last) > 3 and len(event.key) == 1: 
            press.last = press.last[1:]
    except : pass

    global idx, fig, currentMode, stocks

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
    elif press.last == "his":
        setCurrentMode(Modes.history, build=False)

        if Modes.history in currentMode:
            getCsv.csvdir = "historical"
        else:
            getCsv.csvdir = "csv"

        stocks = getStocks(ivv=ivvonly)
        updateDisplay()

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
            updateDisplay()
            currentMode = Modes.none
    elif event.key == 'x':
        from pyutil import restart_program
        saveSettings()
        restart_program()

    elif event.key == '0':
        idx = 0
        updateDisplay()
    elif event.key == '9':
        toggleMulti()
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
        updateDisplay()
    elif key == '-':
        if Modes.average in currentMode:
            pyutil.increaseAvg(False)
        if Modes.recent in currentMode and rebuild.recentIncrement > 6:
            rebuild.recentIncrement -= 5 
        updateDisplay()

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

        astock = event.inaxes.get_title().split("(")[0]
        print("astock : {}".format( astock ))
        util.setTargetPrice(astock, round(event.ydata,3))

        if Modes.multi in currentMode:
#            updateDisplay()
            local_idx = stocks.index(astock)
            rebuild(force_ax = event.inaxes, force_idx = local_idx)
        else:
            nexti()
        return

    global df, savedxdata
    savedxdata = event.xdata
    print("savedxdata : {}".format( savedxdata ))
#    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#          ('double' if event.dblclick else 'single', event.button,
#           event.x, event.y, event.xdata, event.ydata))
    if currentMode == Modes.trim:
        if Modes.multi not in currentMode:
            astock = getCurrentStock()
            trimStock(astock, int(event.xdata))
            rebuild()

def configurePlots(fig):
    adjust = 0.05
    fig.subplots_adjust(left=adjust, bottom=adjust, 
                        right=1-adjust, top=1-adjust)

    move_figure(fig, 1920, 0)
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
            else:
                rebuild(force_ax = next_ax, force_idx = next_idx)
            next_idx += 1

def updateDisplay():
    if Modes.multi in currentMode:
        updateMultiPlot()
    else:
        rebuild()

def toggleMulti(toggle = True):
    global currentMode
    if toggle:
        currentMode ^= Modes.multi
    if Modes.multi in currentMode:
        print ("getting here")
        multiPlot()
    else:
        plotIdx()


def multiPlot():
    global fig, multiax, xcount, idx
    xcount = 3
    plt.close(fig)
    fig, multiax = plt.subplots(nrows=3, ncols=3)
    configurePlots(fig)
    updateMultiPlot()
    plt.show()

#plt.get_current_fig_manager().window.wm_geometry("+0+0")
def plot(astock, start = None, end = None):
    global xl, fig, ax, df, values
    plt.close(fig)

    fig, ax = plt.subplots()
    configurePlots(fig)
    rebuild()

    plt.show()

def saveSettings():
    donotPersist = [Modes.target, Modes.trim]
    global currentMode, idx
    settings(Zen.lastStock, setValue = idx)
    for mode in donotPersist:
        if mode in currentMode:
            currentMode ^= mode
    settings(Zen.lastMode, setValue = currentMode)
    util.saveTargets()

def plotIdx():
    global idx, xcount
    xcount = 10
    idx = settings(Zen.lastStock, default=0)
    plot(stocks[idx])

if __name__ == "__main__":

    currentMode = settings(Zen.lastMode, default=Modes.none)
    ivvonly = Modes.history in currentMode
    lap = False
    if lap:
        plt.rcParams["figure.figsize"] = [11,6]
        xcount = 7
    else:
        plt.rcParams["figure.figsize"] = [16,10]
        xcount = 10

    idx = 0
    stocks = getStocks(ivv = ivvonly)
    stock_count = len(stocks)
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

    plt.rcParams['toolbar'] = 'None'

    try:
        if Modes.multi in currentMode:
            idx = settings(Zen.lastStock, default=0)
            multiPlot()
        else:
            plotIdx()
    except Exception as e:
        print ('Failed3: '+ str(e))
        pass

