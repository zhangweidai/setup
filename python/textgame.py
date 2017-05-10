#from yahoo_finance import Share
from myshare import Share
from pprint import pprint
import menu as MENU
import readchar
import os.path
import pickle
import pygame

purchased = ["amd", "tsla"]
owned = {}
stockNames = ["yhoo", "intc", "amd", "tsla"]
stocks = []
start = '2014-01-01'
end = '2014-09-01'
prices = {}
cash = 10000
c = 0

class OwnedStock:
    price_ = 0
    quantity_ = 0
    def __init__(self, quantity, price)
        self.price_ = price
        self.quantity_ = quantity

def B(pos, quantity):
    global owned, cash
    if quantity == None or quantity == "ALL":
        quantity = 10

    stock = stockNames[pos]
    price = prices[stock][c]
    cost = price * quantity
    if cost > cash:
        return

    cash = cash - cost
    cOwned = owned.get(stock, 0)
    if cOwned == 0:
        purchased.append(stock)
    owned[stock] = OwnedStock(cOwned + quantity, price)
    print "Buying {} shares of {}; current price {}".format(quantity, stock, price)

def S(pos, quantity):
    if pos >= len(purchased) or len(purchased) == 0:
        return
    print pos
    print purchased

    global owned, cash
    stock = purchased[pos]
    price = prices[stock][c]
    if quantity == "ALL":
        quantity = owned[stock]
        owned[stock] = 0

    print "Selling {} shares of {}; current price {}".format(quantity, stock, price)
    gain = price * quantity
    cash = cash + gain
    del purchased[pos]

def getPrices(data):
    ret = []
    for d in data:
        ret.append(float(d['Open']))
        ret.append(float(d['Low']))
        ret.append(float(d['High']))
        ret.append(float(d['Close']))
    return ret

fname = 'prices.pkl'
shareQuery = not os.path.isfile(fname)

def init():
    global owned
    prices = {}

    for name in purchased:
        owned[name] = 10
        cStock = Share(name)
        if shareQuery:
            vec = getPrices(cStock.get_historical(start, end))
            prices[name] = vec

    for name in stockNames:
        cStock = Share(name)
        stocks.append(cStock)
        if shareQuery:
            vec = getPrices(cStock.get_historical(start, end))
            prices[name] = vec

    if not shareQuery:
        output = open(fname, 'r')
        print "loading prices"
        prices = pickle.load(output)

    return prices

prices = init()


if len(prices) == 0:
    print "no prices"
    exit()

maxC = len(prices[prices.keys()[0]])

if shareQuery:
    output = open(fname, 'w')
    print "dumping prices"
    pickle.dump(prices, output)


# yahoo = Share('YHOO')
# pprint(yahoo.get_historical('2014-04-25', '2014-04-29'))
def texts(screen, score):
    font = pygame.font.Font(None, 30)
    scoretext = font.render("Score: " + str(score), 1,(255,255,255))
    screen.blit(scoretext, (500, 457))


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
    cm.init([], screen)

    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    screen.blit(title, (320 - title.get_width() // 2, 240 - title.get_height() // 2))

    PLAYSOUNDEVENT = USEREVENT + 1
    pygame.time.set_timer(PLAYSOUNDEVENT, 1500)

    op = None
    quantity = None
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
                    if op == "Q":
                        pygame.quit()
                        quit()

                    op = "Q"

                # buy
                if event.key == pygame.K_b:
                    if op == "B":
                        op = None
                    else:
                        op = "B"

                # sell
                if event.key == pygame.K_s:
                    if op == "S":
                        op = None
                    else:
                        op = "S"


                if event.key == pygame.K_a and not op == None:
                    quantity = "ALL"
                    pos = cm.get_position()
                    cmd = "{}({}, '{}')".format(op, pos, quantity)
                    print cmd
                    eval(cmd)

                if event.key == pygame.K_UP:
                    cm.draw(-1)

                if event.key == pygame.K_DOWN:
                    cm.draw(1)

                if event.key == pygame.K_RETURN and not op == None:
                    pos = cm.get_position()
                    quantity = "ALL"
                    cmd = "{}({}, '{}')".format(op, pos, quantity)
                    print cmd
                    eval(cmd)

        if op == "B":
            operation = font.render("Buy", True, (128, 128, 0))
            cm.init(stockNames, screen)
        elif op == "S":
            operation = font.render("Sell", True, (128, 128, 0))
            cm.init(purchased, screen)
        elif op == "Q":
            operation = font.render("Quit? (q again)", True, (128, 0, 0))
        else:
            operation = None

        screen.fill((0, 0, 0))
        screen.blit(title, (0,0))

        if operation != None:
            screen.blit(operation, (100, title.get_height()))

        c_render = font.render("c = {}".format(c), True, (0, 128, 0))
        screen.blit(c_render, (0, display[1] - font_height))

        cash_render = font.render("$ = {}".format(cash), True, (0, 128, 0))
        screen.blit(cash_render, (0, display[1] - font_height * 2))

        nextLine = 200
        for i, name in enumerate(purchased):
            cprice = prices[name][c]
            line = "{} of {} ({})".format(owned[name], name)
            currentStock = font.render(line, True, (0, 128, 0))
            nextLine = nextLine + title.get_height() 
            screen.blit(currentStock, (10, nextLine))

        if op:
            cm.draw()

        pygame.display.flip()
        clock.tick(30)

main()
