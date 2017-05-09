from yahoo_finance import Share
from pprint import pprint
import readchar


yahoo = Share('YHOO')
pprint(yahoo.get_historical('2014-04-25', '2014-04-29'))

import pygame
from pygame.locals import *
def main():
    pygame.init()
    display = (800,600)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGLBLIT)

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.SysFont("monospace", 15)

    # render text
    label = myfont.render("Some text!", 1, (255,0,0))
    screen.blit(label, (100, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.quit()
                    quit()


main()
