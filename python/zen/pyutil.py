import os
import sys
from multiprocessing import Process
from enum import Enum
from util import getp, setp
import logging

class Modes(Enum):
    none = 0
    trim = 1
    zoom = 2

class Zen(Enum):
    lastStock = 0

#def setSettings():
#def saveSettings():
def settings(setting, value = None, default = None):
    if value != None:
        try : settings.setdict[setting] = value
        except : 
            try : 
                settings.setdict = getp("settings")
                settings.setdict[setting] = value
            except : 
                settings.setdict = dict()
                settings.setdict[setting] = value
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

