import pygame
import time
import pickle
import random
import traceback
import statistics

from collections import defaultdict
from sortedcontainers import SortedSet

available_fonts_path = "available_fonts2.pkl"

report = ""
# Program to cancel the timer 
import threading 

answer_db = set()
keys = list()
load_map = dict()
thousand = 1000
words_per_session = 10

pygame.init()

display_width = 1800
display_height = 1000

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,160,0)
other = (255,0,255)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

FONT_SIZE = 65
def update_font():
    try:
        return pygame.font.SysFont(available_fonts[next_font], FONT_SIZE )
    except:
        exit()

answer_choices = set() 
USER_ANSWER = ""
choices = "asdfghjkl;"
CANSWERS = list()
start_time = None
done = False
lefty = 200

import atexit
@atexit.register
def goodbye():
    pickle.dump(saved_fonts, open(available_fonts_path, "wb"))

saved_fonts = list()

def game_loop():
    global CURRENT_FONT
    global saved_fonts
    global USER_ANSWER
    global next_font

    centerd = 80

    CURRENT_FONT = update_font()
    TextSurf, TextRect = text_objects("abcdefg", CURRENT_FONT)
    TextRect.center = (lefty, centerd)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_q:
                        quit()

                if event.key == pygame.K_o:
                    saved_fonts = saved_fonts[:-1]
                    print ("ooops")

                if event.key == pygame.K_u or event.key == pygame.K_j:

                    if event.key == pygame.K_u:
                        saved_fonts.append(available_fonts[next_font])

                    print("saved_fonts: {}".format( saved_fonts))
                    next_font += 1
                    CURRENT_FONT = update_font()
                    TextSurf, TextRect = text_objects("abcdefg", CURRENT_FONT)
                    TextRect.center = (lefty, centerd)
                    gameDisplay.blit(TextSurf, TextRect)
                    pygame.display.update()

        gameDisplay.fill(black)
        clock.tick(10)


gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

try:
    available_fonts = pickle.load(open(available_fonts_path, "rb"))
except:
    available_fonts = list()
    pass

print("available_fonts : {}".format( available_fonts ))

available_fonts = pygame.font.get_fonts()
next_font = 0

#print("loaded saved_fonts: {}".format( len(available_fonts)))

try:
    game_loop()
    quit()
except Exception as e:
    traceback.print_exc() 
    print (e)
