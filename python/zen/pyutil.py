import os
import sys
from multiprocessing import Process
from enum import IntFlag, Enum
from util import getp, setp
import logging
import util

class Modes(IntFlag):
    none = 0
    trim = 1
    zoom = 2
    average = 4
    more = 8
    change = 16
    target = 32
    recent = 64
    multi = 128
    history = 256
    sort = 512

#bar = Modes.zoom 
#bar |= Modes.average
#if Modes.zoom in bar:
#    print ("so far so good")
#bar ^= Modes.zoom
#if Modes.zoom in bar:
#    print ("so far so good")

class Zen(Enum):
    lastStock = 0
    lastMode = 1

#def setSettings():
def settings(setting, setValue = None, default = None):
    if setValue != None:
        try : settings.setdict[setting] = setValue
        except : 
            try : 
                settings.setdict = getp("settings")
                settings.setdict[setting] = setValue
            except : 
                settings.setdict = dict()
                settings.setdict[setting] = setValue
        setp(settings.setdict, "settings")
    else:
        try : return settings.setdict[setting]
        except : 
            try:
                settings.setdict = getp("settings")
                return settings.setdict[setting]
            except: pass
    return default
#print (settings(Zen.lastStock))
#settings(Zen.lastStock, 2)
#print (settings(Zen.lastStock))

#    if setting == Settings.lastStock:
#        return True
#

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

class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()


class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):

        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        indx = np.searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        print('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()

avgFactor = 5
def increaseAvg(add):
    global avgFactor
    if add:
        avgFactor += 2
    elif avgFactor > 4:
        avgFactor -= 2

def averageValues(values):
    ret = []
    lastavg = 0
    leng = len(values)
    for i,value in enumerate(values):
        end = i+avgFactor
        if end < leng:
            avg = round(sum(values[i:end])/float(avgFactor), 4)
        else:
            avg = lastavg
        ret.append(avg)
        lastavg = avg
    return ret

def changeValues(values, by = 5, negavg = False):
    ret = []
    last = 0
    leng = len(values)
    negs = []
    for i,value in enumerate(values):
        end = i+by
        if end < leng:
            change = round(values[end]/float(values[i]), 4)
            if negavg and change < 1:
                negs.append(change)
        else:
            change = last
        ret.append(change)
        last = change

    if negavg:
        return util.formatDecimal(sum(negs)/len(negs))

    return ret
#print changeValues([i for i in range(1,40)])
#print [i for i in range(40)]
