#from yahoo_finance import Share
from myshare import Share
from pprint import pprint
import menu as MENU
import readchar

purchased = ["amd", "tsla"]
stockNames = ["yhoo", "intc"]
stocks = []
start = '2014-01-01'
end = '2014-09-01'
prices = {}
cash = 10000

def getPrices(data):
    ret = []
    for d in data:
        ret.append(d['High'])
        ret.append(d['Low'])
        ret.append(d['High'])
        ret.append(d['Close'])
    return ret

for name in stockNames:
    cStock = Share(name)
    stocks.append(cStock)
    vec = getPrices(cStock.get_historical(start, end))
    maxC = len(vec)
    prices[name] = vec

import pygame

# yahoo = Share('YHOO')
# pprint(yahoo.get_historical('2014-04-25', '2014-04-29'))
def texts(screen, score):
    font = pygame.font.Font(None, 30)
    scoretext = font.render("Score: " + str(score), 1,(255,255,255))
    screen.blit(scoretext, (500, 457))

c = 0

from pygame.locals import *
def main():
    global c
    pygame.init()
    clock = pygame.time.Clock()
    display = (800,600)
    screen = pygame.display.set_mode(display)

    font_height = 42
    font = pygame.font.SysFont("arial", font_height)

    message = "Game Title"
    title = font.render(message, True, (0, 128, 0))
    operation = None
    cm = MENU.OpeningMenu() # Current menu reference
    titlesArray = ["a", "b"]
    cm.init(titlesArray, screen)

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    screen.blit(title, (320 - title.get_width() // 2, 240 - title.get_height() // 2))

    PLAYSOUNDEVENT = USEREVENT + 1
    pygame.time.set_timer(PLAYSOUNDEVENT, 1500)

    buy_or_sell = False
    while c < maxC:

        if pygame.event.get(PLAYSOUNDEVENT):
            c = c + 1
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

                # buy
                if event.key == pygame.K_b:
                    operation = font.render("Buy", True, (0, 128, 0))
                    cm.init(stockNames, screen)
                    buy_or_sell = True

                # sell
                if event.key == pygame.K_s:
                    operation = font.render("Sell", True, (0, 128, 0))
                    cm.init(purchased, screen)
                    buy_or_sell = True

                if event.key == pygame.K_UP:
                    cm.draw(-1)

                if event.key == pygame.K_DOWN:
                    cm.draw(1)

                if event.key == pygame.K_RETURN:
                    print cm.get_position()

        screen.fill((0, 0, 0))
        screen.blit(title, (0,0))

        if operation != None:
            screen.blit(operation, (100, title.get_height()))

        c_render = font.render("c = {}".format(c), True, (0, 128, 0))
        screen.blit(c_render, (0, 600 - font_height))

        cash_render = font.render("$ = {}".format(cash), True, (0, 128, 0))
        screen.blit(cash_render, (0, 600 - font_height))

        nextLine = 200
        for i, name in enumerate(stockNames):
            cprice = prices[name][c]
            line = name + " " + cprice
            currentStock = font.render(line, True, (0, 128, 0))
            nextLine = nextLine + title.get_height() 
            screen.blit(currentStock, (200, nextLine))

        if buy_or_sell:
            cm.draw()

        pygame.display.flip()
        clock.tick(30)

main()
