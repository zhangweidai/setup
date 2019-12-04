"""
Show how to connect to keypress events
"""
from termcolor import colored
import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from util import getCsv, getStocks, trimStock, getTrimStock
import util
import z
from matplotlib.pyplot import figure
from tkinter import simpledialog
from pyutil import Modes, Zen, settings
import pyutil
import os
import buy

loadFrom = "bigdic"
startd = None
def deleteStock(astock, force=False):
    global idx, stocks, stock_count
    if not force:
        print ("Not Deleting : {}".format(astock))
        return
    print ("Deleting : {}".format(astock))
    z.delStock(astock)
    idx += 1
    updateDisplay()
#    resetStocks(update = True)

def resetStocks(update=True):
    global stocks, stock_count, loadFrom
    z.getCsv.download = False

    alls = z.getp(loadFrom)
    stocks = []
    if type(alls) == dict:
        stocks = list(alls.keys())
    else:
        stocks = list(alls)

#    raise SystemExit
    stock_count = len(stocks)
    print("stock_count : {}".format( stock_count ))
    if update:
        updateDisplay()

def getCurrentStock(force_idx = None):
    global idx
    try :return stocks[force_idx or idx]
    except : 
        idx = 0 
        return stocks[0]

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



def displayStats(values, astock, date):
    avgby = pyutil.changeValues(values, rebuild.chaBy, negavg = True)
    try:
        highlow, vari, var2 = util.getRangedDist(values)
    except:
        highlow, vari, var2 = 0,0,0
        pass
#        deleteStock(astock)

    leng = len(values)
    print("\t{}  : Length:{}".format(date, leng))
    opens = df["Open"].tolist()
    avg, maxd, davg = pyutil.dailyAverage(opens, values)

    print("\tDailyAvg30  : {}".format(davg))
    print("\tDailyAvgDrop: {}".format(avg))
    print("\tMaxDailyDrop: {}".format(maxd))
    print("\tAvgDrop {}   : {}".format(rebuild.chaBy, avgby))

    half = int(leng/2)
    mid = values[-1 * half]

    changep = util.formatDecimal(values[-1]/values[0])

    csm = util.formatDecimal( mid / values[0])
    cme = util.formatDecimal( values[-1] / mid)

    if not changep[0] == "-":
        changep = colored(changep,"green")  
    if not csm[0] == "-":
        csm = colored(csm,"green")  
    if not cme[0] == "-":
        cme = colored(cme,"green")  

    print("\tChange      : {}".format(changep))
    print("\tCs-m        : {}".format(csm))
    print("\tCm-e        : {}".format(cme))

    if var2:
#        print("\tHighLow     : {}".format(highlow))
#        print("\tVariance    : {}".format(vari))
        print("\tVariance2   : {}".format(var2))
    try:
        score, dipScore = util.getScore(values)
#        print("\tScore       : {}".format(util.getScoreFromCsv(astock)))
        print("\tDip         : {}".format(dipScore))
    except:
        pass

    r1,r2 = util.getRangeScore(values, sub=True)
    if r1:
        print("\tRange1      : {}".format(r1))
    if r2:
        print("\tProbUpScore : {}".format(r2))
        pass


def nexti():
    global idx
    increment = 8 if Modes.multi in currentMode else 1

    if idx + increment < stock_count:
        idx += increment
        updateDisplay()
    else:
        print ("out of bounds")

def previ():
    global idx
    increment = 1
    if Modes.multi in currentMode:
        increment = 8

    if idx - increment >= 0:
        idx -= increment
        updateDisplay()

marked = []
def interpret(answer):
    global idx, stocks, previdx, stock_count, setstart_date, loadFrom
    print("answer: {}".format( answer))
    if not answer:
        return

    if "mark" in answer:
        date = answer.split(" ")[1].upper()
        marked.append(date)
        updateDisplay()

    elif "reset" in answer:
        stock = getCurrentStock()
        if Modes.multi in currentMode:
            stock = answer.split(" ")[1].upper()

        util.resetStock(stock)
        updateDisplay()

    elif "newscore" in answer:
        path = util.getPath("report/scores_new.csv")
        util.setWhatToBuy.fromfile = path
        util.setWhatToBuy(1, False)
        resetStocks()

    elif "sets" in answer:
        setstart_date = df.at[0,"Date"]
        updateDisplay()

    elif "/2" in answer:
        rebuild.recentIncrement = int(len(values)/2)
        toggleCurrentMode(Modes.recent)

    elif "recent" in answer:
        rebuild.recentIncrement = int(answer.split(" ")[1])
        util.loadBaseline(start=rebuild.recentIncrement)
        print (util.getStartDate())
        toggleCurrentMode(Modes.recent)

    elif "load" in answer:
        pckl = answer.split(" ")[1]
        loadFrom = pckl
        resetStocks()

    elif "delete" in answer:
        stock = getCurrentStock()
        if Modes.multi in currentMode:
            stock = answer.split(" ")[1].upper()
            print("stock : {}".format( stock ))
        deleteStock(stock, force = True)
    else:
        previdx = idx
        answer = answer.upper()
        try:
            idx = stocks.index(answer)
            updateDisplay()
        except Exception as e:
            try:
                setHistory(toggle=False)
                idx = stocks.index(answer)
            except:
                if util.getCsv(answer) is not None:
                    util.saveAdded(answer)
                    resetStocks(update=False)
                    idx = stocks.index(answer)
                    updateDisplay()
                else:
                    try:
                        ret = util.saveProcessedFromYahoo(answer, add=True)
                        if ret: 
                            util.saveAdded(answer)
                            resetStocks()
                        else:
                            print("Did not find : {}".format( answer))
                    except Exception as e:
                        print ('xFailed2: '+ str(e))
                        pass

def setCurrentMode(mode, build = True):
    if mode not in currentMode:
        toggleCurrentMode(mode, build)

def toggleCurrentMode(mode, build = True):
    global currentMode, ivvonly
    currentMode ^= mode
    if build:
        updateDisplay()
    else:
        if Modes.multi in currentMode:
            updateMultiPlot(titlesOnly = True)
        else:
            updateTitle()

def handleModifier(key):
    print("key: {}".format( key))
    global previdx, idx
    if key == "control" and previdx != idx:
        previdx, idx = idx, previdx
        updateDisplay()

def handleSort(sort_col = None, overrideSrc = None):
    global idx, stocks, currentMode

    setCurrentMode(Modes.sort, build=False)
    if Modes.history not in currentMode:
        currentMode ^= Modes.history
    
    rebuild.recentIncrement = util.getBuyBackTrack()

    if sort_col:
        handleSort.curr_sort_col = sort_col

    sort_col = sort_col or handleSort.curr_sort_col 
    col_name = util.getSortVec()[sort_col-1]

    util.setWhatToBuy.fromfile = overrideSrc
    if overrideSrc:
        if Modes.recent in currentMode:
            currentMode ^= Modes.recent

    idx = 0
    if Modes.sort in currentMode:
        util.setWhatToBuy(col_name, handleSort.curr_sort_ascend)
    else:
        util.setWhatToBuy(None)

    try:
        resetStocks()
    except:
        print(overrideSrc)
        util.setWhatToBuy.fromfile = None
        resetStocks()

def setHistory(toggle=True):
    global currentMode, ivvonly, stocks, stock_count

    if toggle and Modes.history in currentMode:
        return

    getStocks.totalOverride = True

    if Modes.sort in currentMode:
        rebuild.recentIncrement = rebuild.recentIncrement * 4
        updateDisplay()
        return
 
    currentMode ^= Modes.history
    ivvonly = Modes.history in currentMode
 
    if Modes.history in currentMode:
        getCsv.csvdir = "historical"
        if Modes.recent in currentMode:
            currentMode ^= Modes.recent
    else:
        getCsv.csvdir = "csv"
    resetStocks()

def handleSelectionMode(increment = 1):
    rebuild.showSelections = True
    col_name = util.getSortVec()[handleSort.curr_sort_col-1]
    util.fromSelection.mode = "{}/{}".format(col_name, 
            handleSort.curr_sort_ascend)
    handleSort(overrideSrc=pyutil.getNextHisSelection(increment))

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

#    print("last press :{}".format(press.last))

    global idx, fig, currentMode, stocks, ivvonly

    if press.last == "aa" or press.last == "aaa":
        press.last = ""
    elif press.last == "avg":
        toggleCurrentMode(Modes.average)
    elif press.last == "cle" or press.last == "cls":
        toggleCurrentMode(Modes.none)
    elif press.last == "mor":
        toggleCurrentMode(Modes.more)
    elif press.last == "cha":
        toggleCurrentMode(Modes.change)
    elif press.last == "tar":
        toggleCurrentMode(Modes.target, build=False)
    elif press.last == "rec":
        toggleCurrentMode(Modes.recent)
    elif press.last == "tri":
        toggleCurrentMode(Modes.trim, build=False)
    elif press.last == "his":
        setHistory()
    elif press.last == "all":
        setHistory()
        return

    sys.stdout.flush()
#        visible = xl.get_visible()
#        xl.set_visible(not visible)
#    if event.key == 'left':
    if event.key == 'q':
        saveSettings()
        return

    elif event.key == '`':
        handleSort()

    elif event.key == '<':
        handleSelectionMode(increment=-1)
    elif event.key == '>':
        handleSelectionMode(increment=1)
    elif event.key == ']':
        handleSort(overrideSrc=pyutil.getNextHis())
    elif event.key == '[':
        handleSort(overrideSrc=pyutil.getNextHis(increment=False))
    # zz
    elif event.key == 'z':
        if not currentMode == Modes.zoom:
            currentMode = Modes.zoom
        else:
            updateDisplay()
            rebuild.recentIncrement = 35
            currentMode = Modes.none
        return

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
        prev = settings(Zen.prevAnswer, default="")

        answer = simpledialog.askstring("Advanced", "cmd:", 
                parent = None, initialvalue=prev)

        settings(Zen.prevAnswer, answer)
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

    if Modes.sort in currentMode:
        if event.key == 'f':
            handleSort.curr_sort_ascend = not handleSort.curr_sort_ascend
            if rebuild.showSelections:
                pyutil.getNextHisSelection.idx = 0
                handleSelectionMode(increment = 0)
            else:
                handleSort(handleSort.curr_sort_col)
    if event.key in [str(i) for i in range(1, 6)]:
        mode = int(event.key)
        if mode == 1:
            handleSort.curr_sort_ascend = True
        elif mode == 2:
            handleSort.curr_sort_ascend = False
        elif mode == 3:
            handleSort.curr_sort_ascend = False
        elif mode == 4:
            handleSort.curr_sort_ascend = True
        elif mode == 5:
            handleSort.curr_sort_ascend = False
            
        handleSort(mode)
press.last = ""

def handle_close(evt):
    saveSettings()

def handleIncrease(key):
    if key == '=':
        if Modes.average in currentMode:
            pyutil.increaseAvg(True)
        elif Modes.recent in currentMode:
            rebuild.recentIncrement += 5
        else:
            rebuild.chaBy += 1
        updateDisplay()
    elif key == '-':
        if Modes.average in currentMode:
            pyutil.increaseAvg(False)
        elif Modes.recent in currentMode and \
                rebuild.recentIncrement > 6:
            rebuild.recentIncrement -= 5 
        elif rebuild.chaBy > 1:
            rebuild.chaBy -= 1
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
    try:
        if event.xdata > leng or savedxdata > leng:
            currentMode = Modes.none
            return
    except:
        return

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
    print ("\nChange: {}".format(util.formatDecimal(answer)))
    print ("Start : {}({})".format( date1, value1 ))
    print ("End   : {}({})".format( date2, value2 ))
    print ("Days  : {}".format( x1-x2 ))
    if currentMode == Modes.zoom:
        xadjust = x2
        rebuild(x2, x1)
        print("x1: {}".format( x1))
        print("x2: {}".format( x2))
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
#    print("savedxdata : {}".format( savedxdata ))
#    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#          ('double' if event.dblclick else 'single', event.button,
#           event.x, event.y, event.xdata, event.ydata))
    if Modes.trim in currentMode:
        if Modes.multi not in currentMode:
            astock = getCurrentStock()
            print("astock : {}".format( astock ))
            trimStock(astock, int(event.xdata))
            updateDisplay()

def configurePlots(fig):
    adjust = 0.05
    fig.subplots_adjust(left=adjust, bottom=adjust, 
                        right=1-adjust, top=1-adjust)

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


def saveSettings():
    return
    donotPersist = [Modes.target, Modes.trim, Modes.history, Modes.sort]
    global currentMode, idx
    settings(Zen.lastStock, setValue = idx)
    for mode in donotPersist:
        if mode in currentMode:
            currentMode ^= mode
    settings(Zen.lastMode, setValue = currentMode)
    util.saveTargets()
    z.removeFromStocks(z.delStock.items)

def plotIdx():
    global idx, xcount, stocks
    xcount = 10
    idx = settings(Zen.lastStock, default=0)
    if idx >= len(stocks):
        idx = 0
    plot(stocks[idx])


def plotSelection(astock, local_ax, df):
    sels = util.fromSelection.ddict[astock]
    print("sels : {}".format( sels ))
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


def plot(astock, start = None, end = None):
#    global xl, fig, ax, df, values
#    plt.close(fig)

    if not start:
        start = dates[-252]

    fig, ax = plt.subplots()
    plt.get_current_fig_manager().window.wm_geometry("+0+0")
    configurePlots(fig)

    ax.cla()
    values = list()
    started = False
    ldates = list()
    for i, row in enumerate(buy.getRows(astock, start)):
        if row['Date'] == start:
            started = True
#        c_open = float(row['Open'])
        if started:
            c_close = float(row[z.closekey])
            values.append(c_close)
            ldates.append(row['Date'])

#    print (dir(ax))
#    print ("Fig")
#    print (dir(fig))
    ax.plot(values)
    ax.grid(color='grey', linestyle=':', linewidth=1)

    label = "hello"
    plt.annotate(label, # this is the text
                 (50,270), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center

    num_dates = len(ldates)
    print("ldates: {}".format( ldates[-1]))
#    print(round(num_dates/25))
    xranges = [i for i in range(0, num_dates, round(num_dates/9))]
#    xranges.append(num_dates-1)

    xlabels = ["{}\n({})".format(i, ldates[i]) for i in xranges]
#    xlabels.append("{}\n({})".format(num_dates-1, ldates[-1]))

    ax.set_title("{} {}".format(astock, start))
    ax.set_xticklabels(xlabels)
    ax.set_xticks(xranges)
    fig.canvas.draw()
    fig.canvas.get_tk_widget().focus_set()
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--stock', default="IVV")
    astock = None
    args = parser.parse_args()
    astock = args.stock

    currentMode = Modes.none
    savedxdata = None
    dates = z.getp("dates") 
    startd = dates[-252]
    lap = False
    if lap:
        plt.rcParams["figure.figsize"] = [10,5]
    else:
        plt.rcParams["figure.figsize"] = [11,8]

    plot(astock)
