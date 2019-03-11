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
print (matplotlib.matplotlib_fname())
from tkinter import simpledialog; 
from enum import Enum

class Modes(Enum):
    none = 0
    trim = 1

currentMode = Modes.none

#print("figure: {}".format(figure))
#fig_size = plt.rcParams["figure.figsize"]
#print ("Current size:", fig_size)
  
 # Set figure width to 12 and height to 9
plt.rcParams["figure.figsize"] = [16,10]
stocks = getCsv("analysis/why_buy_these.csv", 0)
stocks = [stock.split("/")[-1] for stock in stocks]
stocks_idx = 0
stock_count = len(stocks)
start = None
end = None
ax = None

def getCurrentStock():
    return stocks[stocks_idx]


values = None
df = None

def rebuild():
    global ax, values, df
    ax.cla()
    astock = stocks[stocks_idx]
    df = getCsv(astock)
    df = df[start:end]
    values = df[csvColumn].tolist()
    ax.plot(values)
    ax.set_title(astock)
    fig.canvas.draw()

def press(event):
    global stocks_idx, fig, currentMode
    print('press', event.key)
    sys.stdout.flush()
#        visible = xl.get_visible()
#        xl.set_visible(not visible)
#    if event.key == 'left':
    if event.key == 'z':
        from pyutil import restart_program
        restart_program()
    if event.key == '0':
        stocks_idx = 0
        rebuild()
    elif event.key == 'j' and stocks_idx+1 < stock_count:
        stocks_idx += 1
        rebuild()
    elif event.key == 'k' and stocks_idx > 0 :
        stocks_idx -= 1
        rebuild()
    elif event.key == 't':
        currentMode = Modes.trim
    elif event.key == ' ':
        answer = simpledialog.askstring("Advanced", "cmd:", parent = None)
        if answer == "reset":
            util.resetStock(getCurrentStock())
        fig.canvas.get_tk_widget().focus_set()
        rebuild()
#            trimStock(getCurrentStock(), answer)
#            rebuild()
def handle_close(evt):
    print('Closed Figure!')

def handle_scroll(evt):
    print("evt: {}".format( evt))

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

csvColumn = "Close"
xl = None
fig = None

def onclick(event):
    global df, currentMode
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    astock = getCurrentStock()
    if currentMode == Modes.trim:
        trimStock(astock, int(event.xdata))
        rebuild()
        currentMode = Modes.none
        print(getTrimStock(astock))
#print (getTrimStock("VST"))

#plt.get_current_fig_manager().window.wm_geometry("+0+0")
def plot(astock, start = None, end = None):
    global xl, fig, ax, df

    df = getCsv(astock)
    df = df[start:end]
    values = df[csvColumn].tolist()
    plt.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots()

    adjust = 0.05
    fig.subplots_adjust(left=adjust, bottom=adjust, 
                        right=1-adjust, top=1-adjust)

    move_figure(fig, 1920, 0)
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('scroll_event', handle_scroll)
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('close_event', handle_close)

    ax.plot(values)
    ax.set_title(astock)
    plt.show()

plot(stocks[stocks_idx])
