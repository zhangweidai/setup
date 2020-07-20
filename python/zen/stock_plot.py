"""
Show how to connect to keypress events
"""
import sys
import math
import matplotlib
import matplotlib.pyplot as plt
import z
from matplotlib.pyplot import figure
from tkinter import simpledialog
import os
from rows import *
from tkinter import *
from tkinter import Menu, messagebox,simpledialog,ttk

prevcommands = ["1 year", "1 month", "6 month"]

recent = z.getp("recent_plots")
recent = recent if recent else ["+IVV", "+VUG"]

class SimpleChoiceBox:
    def __init__(self,title,text,choices):
        try:
            print("choices: {}".format( choices))
            self.t = Toplevel()
            self.t.title(title if title else "")
            self.selection = None
            Label(self.t, text=text if text else "").grid(row=0, column=0)

            self.shortcuts = Listbox(self.t)
            self.shortcuts.grid(row=1,column=0)
            for item in prevcommands:
                self.shortcuts.insert(END, item)

            self.recentplots = Listbox(self.t)
            self.recentplots.grid(row=1,column=1)
            for item in recent:
                self.recentplots.insert(END, item)


            self.entry = Entry(self.t)
            self.entry.grid(row=2, column=0)

#            self.c.grid(row=0, column=1)
            self.shortcuts.bind("<<ListboxSelect>>", self.CurSelet)
            self.recentplots.bind("<<ListboxSelect>>", self.CurSelet)
            self.entry.bind('<Key-Return>', self.on_changed)
#            self.c.bind("<<ListboxSelected>>", self.combobox_select)
        except Exception as e:
            z.trace(e)

    def on_changed(self, event):
        interpret(self.entry.get())
        return True

    def CurSelet(self,event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            picked = widget.get(selection[0])
            interpret(picked)


colors = ["tab:green", "tab:blue", "red", "black", "pink"]
types = "ETFs"
increment = 10
default = 700 
start = default 
dates = z.getp("dates")
end = start
ax = None
ax2 = None
axs = None
fig = None
lastworking = None
ref_astock = "USMV"
stocks = []
showing = 5
starting = 0
idx = 0

def resetingStarting():
    global showing, starting, idx
    showing = 5
    starting = 0
    idx = 0

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

startdate = None
def rebuild():
    global ax, fig, start, lastworking, ax2, axs, stocks, startdate, recent

    vdict = dict()
    istart = start * -1
    startdate = dates[istart]
    tmaxv = 0
    tminv = 1
    cstocks = stocks[starting + idx : showing + idx]

    print("stocks: {}".format( stocks))
    for cstock in stocks:

        if cstock in recent:
            recent.remove(cstock)
        recent.insert(0, cstock)

        values = list()
        print("startdate: {}".format( startdate))
        for i, row in enumerate(getRowsRange(cstock, count=end, date=startdate)):
            c_close = float(row[z.closekey])
            values.append(c_close)
        try:
            fv = values[0]
        except Exception as e:
            z.trace(e)
            break
        v1 = [ round((i/fv)-1,3) for i in values ]
        vdict[cstock] = v1
        minv = min(v1)
        maxv = max(v1)
        tmaxv = max(maxv, tmaxv)
        tminv = min(minv, tminv)

    tminv -= .02
    tmaxv += .02
    iend = istart + end

    if iend == 0:
        iend = None
    try:
        date_range = dates[istart:iend]
        xranges = [i for i in range(0, end, round(end/9))]
        xlabels = ["{}\n({})".format(i, date_range[i]) for i in xranges]
    except Exception as e:
        z.trace(e)
        start = lastworking
        rebuild()
        return

    lastworking = start

    ax.cla()
    plt.grid(color='black', linestyle='-', linewidth=0.5)
    ax.set_title("{} {}".format(types, startdate))
    ax.set_ylim([tminv,tmaxv])

    for i,cstock in enumerate(cstocks):
        color = colors[i]
        line, = ax.plot(vdict[cstock], color=color)
        line.set_label(cstock)

    ax.legend()
    ax.set_xticklabels(xlabels)
    ax.set_xticks(xranges)
    fig.tight_layout()
    fig.canvas.draw()
    fig.canvas.get_tk_widget().focus_set()
    plt.grid(color='black', linestyle='-', linewidth=0.5)


import atexit
@atexit.register
def goodbye():
    z.setp( recent[:20], "recent_plots", True)

def restart_program():
    z.setp( recent[:20], "recent_plots", True)
    try:
        p = Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except:
        pass
    python = sys.executable
    os.execl(python, python, *sys.argv)

def updateTitle():
    global ax, mode, types, startdate
    mod = ""
    if mode:
        mod = "({})".format(mode)
    print("mode: {}".format( mode))
    ax.set_title("{} {} {}".format(types, startdate, mod))
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
    global idx, previdx, stock_count, setstart_date, loadFrom
    global start, end, stocks
    print("answer: {}".format( answer))

    if not answer:
        return

    elif "save" in answer:
        name = answer.split(" ")[1]
        z.setp((stocks,start,end), name)
        print ("saved {}".format(name))

    elif "load" in answer:
        name = answer.split(" ")[1]
        prev_stocks, prev_start, prev_end = stocks, start, end
        try:
            stocks, start, end = z.getp(name)
            print ("loaded {}".format(name))
        except:
            stocks, start, end = prev_stocks, prev_start, prev_end 
        rebuild()

    elif "end" in answer:
        end = end - int(answer.split(" ")[1])
        rebuild()

    elif "-" in answer:
        start = len(dates)
        start = start - dates.index(answer)
        print("start : {}".format( start ))
        end = start
        rebuild()

    elif "year" in answer:
        month = answer.split(" ")[0]
        start = 252 * int(month)
        end = start
        rebuild()


    elif "month" in answer:
        month = answer.split(" ")[0]
        start = 22 * int(month)
        end = start
        rebuild()

#    if "regen" in answer:
#        import regen_stock
#        regen_stock.process(astock)
#        rebuild()

    elif "reset" in answer:
        stock = getCurrentStock()


    elif "newscore" in answer:
        resetStocks()

    elif "sets" in answer:
        setstart_date = df.at[0,"Date"]

    else:
        idx = 0
        answer = answer.upper()
        if answer[0] == "+":
            stocks.append(answer[1:])
        else:
            stocks = answer.split(",") if "," in answer else [answer]
        rebuild()

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

mode = ""
answer = None
def press(event):
    global answer, recent
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

    global idx, fig, currentMode, ivvonly, start, end, increment, stocks, mode

    sys.stdout.flush()

    print(event.key)
    try:
        intkey = int(event.key)
        if intkey:
            print("intkey: {}".format( intkey))
            if mode == "dropping":
                mode = ""
                updateTitle()
                stocks.pop(intkey-1)
                rebuild()
    except:
        pass

    mode = ""

    if event.key == 'q':
        exit()
        return

    elif event.key == 'l':
        mode = "loading"
        updateTitle()
        answer = simpledialog.askstring("Loading", "name:", parent = None, initialvalue=None)
        updateTitle()
        types, stocks = z.getStocks(answer)

        updateTitle()
        resetingStarting()
        rebuild()
        return

    elif event.key == 'd':
        mode = "dropping"
        updateTitle()
        return

    elif event.key == 'n':
        idx += 1
        rebuild()
        return

    elif event.key == 'p':
        idx -= 1
        rebuild()
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
        pass
    elif event.key == 'z':
        pass
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

        answer = simpledialog.askstring("Advanced", "cmd:", parent = None, initialvalue=answer)
        try:
            interpret(answer)
            recent.insert(0,answer)
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
    print("backend : {}".format( backend ))
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
    x2 = int(savedxdata) 
    endx = len(values)
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
#    fig.subplots_adjust(left=adjust, bottom=adjust, 
#                        right=1-adjust, top=1-adjust)
#    move_figure(fig, 0, 0)
#    move_figure(fig, 0, 0)
    fig.canvas.mpl_connect('key_press_event', press)
    fig.canvas.mpl_connect('scroll_event', handle_scroll)
    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('button_release_event', onrelease)
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.mpl_connect('mouse_move_event', handle_close)

#plt.get_current_fig_manager().window.wm_geometry("+0+0")
def plot():
    global ax, fig 
    fig, ax = plt.subplots()
    configurePlots(fig)
    rebuild()
    fig.canvas.get_tk_widget().focus_set()

    answer = SimpleChoiceBox("Advanced", "cmd:", stocks)
    plt.show(block=True)

def preplot(astocks = None):
    global stocks

    if astocks:
        stocks = astocks

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

#    parser = argparse.ArgumentParser()
#    parser.add_argument('helpers', type=str, nargs='?', default = "")
#    parser.add_argument('refs', type=str, nargs='?', default = "")
#    parser.add_argument('--s', default=None)
#    args = parser.parse_args()

#    if args.s:
#        stocks = args.s.upper().split(",")

    if not stocks:
        if "," in args.helpers:
            stocks = args.helpers.upper().split(",")
        else:
            if args.helpers == "":
                stocks = z.getEtfList(buys=True)
            else:
                types, stocks = z.getStocks(args.helpers)

    print("stocks : {}".format( stocks ))
    try:
        plot()
    except Exception as e:
        import traceback
        print (traceback.format_exc())
        print ('Failed3: '+ str(e))
        pass

if __name__ == "__main__":
    stocks = ["BA", "AMD"]
    import args
    if len(args.args.stocks) == 1:
        stocks.append(args.args.stocks[0])
    print("stocks: {}".format( stocks))
    preplot(stocks)
