#from blessings import Terminal
#
#term = Terminal()
#with term.location(0, term.height - 1):
#    print ('This is', term.underline('pretty!'))
#print term.move_up + 'Howdy!'


#from blessings import Terminal
#t = Terminal()
#print(t.bold('Hi there!'))
#print(t.bold_red_on_bright_green('It hurts my eyes!'))
#with t.location(0, t.height - 1):
#    print('This is at the bottom.')
import z
import curses
stocks = ["a","b","c"]

cols = ["Stock", "price", 
     ["avgC",7], 
     "median", "probD", 
     ["avgD",7], 
     ["avgG",7], 
     ["d0",7], 
     ["d1",7], 
     ["d2",7], 
     ["ChgT",7], 
     ["Chg1",7], 
     ["Chg3",7], 
     ["Live",7], 
     "etf", "recov", "mcchg", "beta", "pe", "largest",  "erank", "div", "mcrnk",
     ["Y1W",7], 
     ["Y1M",7], 
     ["Y1L",7], 
     "ultrank"]
#cols = [
#    ["Stock",8], 
#    ["Value"]
#]

from blessings import Terminal
term = Terminal()

def debug(msg):

    print( term.move(debug.i,50) + str(msg))
    debug.i += 1
debug.i = 50

def getColData(astock, coldata):
    if coldata == "Stock":
        return astock
#    debug("astock: {}".format( coldata))
    return coldata

def getColStarting(starting, coldata):
    if type(coldata) == str:
        return starting + len(coldata) + 2
    else:
        return starting + coldata[1] + 1

tableStartRow = 3
tableStartCol = 2
currentIdx = 0

def draw_menu(stdscr):
    global currentIdx

    drawTable(stdscr)
    k = None
    while (k != "q"):
        k = stdscr.getkey()
        if k == "KEY_RIGHT":
            currentIdx += 1
        if k == "KEY_LEFT":
            currentIdx -= 1
        debug(k)
        drawTable(stdscr)
#    k = stdscr.getch()

buySaved = z.getp("buySaved")
def drawTable(stdscr):

    stdscr.clear()
    stdscr.refresh()

    title = list(buySaved.keys())[currentIdx]
    values = buySaved[title]

    print(term.move(1, tableStartCol) + title)
    row = tableStartRow - 1
    starting = tableStartCol
    for col, coldata in enumerate(cols):

        if type(coldata) is str:
            colLabel = term.underline(coldata)
        else:
            colLabel = term.underline(coldata[0])

        print(term.move(row , starting) + colLabel)
        starting = getColStarting(starting, coldata)

    for row, value in enumerate(values):
        srow = row + tableStartRow
        starting = tableStartCol
        for col, coldata in enumerate(cols):
#            data = getColData(astock, coldata[0])
            try:
                print(term.move(srow , starting) + str(values[row][col]))
            except:
                debug("value : {}".format( value ))
            starting = getColStarting(starting, coldata)

curses.wrapper(draw_menu)

#term = Terminal()
#term.clear()
#term.refresh()
#print(dir(term))
