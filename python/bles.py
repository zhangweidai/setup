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
import curses
def draw_menu(stdscr):
    stdscr.clear()
    stdscr.refresh()
    from blessings import Terminal
    term = Terminal()

    title = "This is a much longer string"
    start_x_title = int((term.width // 2) - (len(title) // 2) - len(title) % 2) 
#    print(term.move(10, start_x_title) + title)
    start_x_title = int((term.width // 2) - (len(title) // 2) - len(title) % 2) - 40
    print(term.move(10, start_x_title) + title)

    k = stdscr.getch()
curses.wrapper(draw_menu)

#term = Terminal()
#term.clear()
#term.refresh()
#print(dir(term))
