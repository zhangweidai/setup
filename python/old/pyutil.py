import os
import sys
from multiprocessing import Process
from enum import Enum
try:
    from enum import IntFlag
except:
    pass
from z import getp, setp
import logging
import util

try:
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
except:
    pass
    
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
    prevAnswer = 2

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

def dailyAverage(opens, closes):
    negs = []
    davg = len(opens) - 60

    davglist = []
    for i,closed in enumerate(closes):

        temp = closed/opens[i]
        if i > davg:
            davglist.append(temp)
        if temp < 1:
            negs.append(temp)
    try:
        ret1 = util.formatDecimal(sum(negs)/len(negs))
        ret2 = util.formatDecimal(min(negs))
        davg = util.formatDecimal(sum(davglist)/len(davglist))
        return ret1, ret2, davg
    except:
        pass
    return None, None, None


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

def clearDir(dirname, search = None):
    path = util.getPath(dirname)
    if "zen_dump" not in path:
        return

    try:
        cmd = ""
        if search:
            cmd = "find {} | grep {} | xargs rm -rf".format(path, search)
        else:
            cmd = "find {} -type f | xargs rm -rf".format(path)
        os.system(cmd)
    except:
        pass

def getFiles(where, his_idx = None):
    import fnmatch
    if getFiles.rememberedFiles:
        return getFiles.rememberedFiles
    holds = []
    parentdir = util.getPath(where)
    listOfFiles = os.listdir(parentdir)
    for entry in listOfFiles:  
        date = entry.split("_")
        try:
            if len(date) < 3 or date[0] != where or \
                (his_idx and int(date[1]) != his_idx) or \
                "csv" not in date[2]:
                    continue
        except:
            continue
        pattern =  "{}*".format(where)
        if fnmatch.fnmatch(entry, pattern):
            getFiles.rememberedFiles.append("{}/{}".format(parentdir, entry))
    getFiles.rememberedFiles.sort()
    return getFiles.rememberedFiles
getFiles.rememberedFiles = []

def getNextHisSelection(increment = 1):
    count = [i for i in range(3,10)]
    index = count[getNextHisSelection.idx]
    path = util.getPath("history/selection_standard_{}.csv".format(index))
    getNextHisSelection.idx += increment
    return path
getNextHisSelection.idx = 0

def getNextHis(increment = True):
    try :
        if increment:
            getNextHis.idx += 1
        elif getNextHis.idx > 0:
            getNextHis.idx -= 1
        ret = getFiles(where = "history")[getNextHis.idx]
        if ret:
            return ret
        getNextHis.idx = 0
        return getFiles(where = "history")[getNextHis.idx]
    except:
        getNextHis.idx = 0
        return getFiles(where = "history")[getNextHis.idx]
    return None
getNextHis.idx = 0

