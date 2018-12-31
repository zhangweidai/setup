from deuces import Deck
from deuces import Card
from deuces import Evaluator
import random
from enum import Enum
import readchar

class Actions(Enum):
    bet = 1
    fold = 2
    call = 3
    check = 4

deck = None
compPlay = Actions.check
ANTI = 10
minBet = 10
maxBet = minBet * minBet
money_ = 10000
turn = 0

def numberOfPlayers():
    return 1

def getActiveActor():
    global turn
    turn = turn + 1
    return turn % (numberOfPlayers() + 1)

def getCompAction(betSize, exclude = []):
    action = Actions(random.randint(1, len(Actions)))
    if action == Actions.bet:
        return getCompBet()

    if betSize == 0:
        while action in [Actions.fold]:
            action = Actions(random.randint(1, len(Actions)))
        return action
    return action

def getCompBet():
    return random.randint(minBet, maxBet)

def decrementMoney(decrement = ANTI):
    global money_
    money_ = money_ - decrement
    return decrement

def playerWins():
   money_ = money_ + potSize_ 
   potSize_ = 0

betOnTable_ = 0
potSize_ = 0
betSize = 0

def antiUp():
    global potSize_
    potSize_ = potSize_ + decrementMoney() + ANTI
    
def loopIt():
    global betOnTable_, potSize_, betSize, compPlay
    checks = 0
    antiUp()

    while(True):
        turn = getActiveActor()
        if checks == 2:
            checks = 0

            if len(board) == 5:
                checkWinner()
            else:
                board.append(deck.draw(1))

        if turn == 0:
            print "Money : {} \t Pot : {}".format(money_, potSize_)
            if betOnTable_:
                print "Action: (c)all, (f)old, (r)aise (q)uit: "
            else:
                print "Action: (c)heck (b)et, (f)old, (r)aise (q)uit: "

            play = readchar.readkey()
            while (play not in ["c", "b", "f", "q"]):
                play = readchar.readkey()

            if play == "c":
                betOnTable_ = 0
                potSize_ = potSize_ + betOnTable_
                betSize = 0
                checks = checks + 1

            if play == "b":
                print "Betting"
                betSize = raw_input("Size: ")
                decrementMoney(betSize)
                potSize_ = potSize_ + betSize

            elif play == "f":
                print "Folding"
                return

            elif play == "q":
                exit()
        else:

            compPlay = getCompAction(betSize)
            compPlay = Actions.check

            if isinstance(compPlay, int) and compPlay >= minBet:
                betOnTable_ = compPlay
                potSize_ = potSize_ + betOnTable_ + betSize

            elif compPlay == Actions.fold:
                playerWins()

            elif compPlay == Actions.check or compPlay == Actions.call:
                potSize_ = potSize_ + betSize
                betSize = 0
                checks = checks + 1
        
        if checks == numberOfPlayers() + 1 and len(board) == 5:
            checkWinner()
        else:
            printBoard()

myHand = None
hands = []
board = None

def printBoard():
    import os
    os.system("clear")
    print "Board:"
    Card.print_pretty_cards(board)
    print "Your Hand:"
    Card.print_pretty_cards(myHand)
    print "Bet On Table: {}".format(betOnTable_)
    print "Last Comp Action: {}".format(compPlay)
    print "----------"
    for hand in hands:
        Card.print_pretty_cards(hand)

def playGame():
    global hands, board, myHand, deck
    deck = Deck()
    board = deck.draw(3)
    myHand = deck.draw(2)
    for comp in range(numberOfPlayers()):
        hands.append(deck.draw(2))

    loopIt()

evaluator = Evaluator()
print dir(evaluator)
def checkWinner():
    evaluator = Evaluator()
#    print evaluator.hand_summary(board, [myHand] + hands)
#    print evaluator.evaluate(board, [myHand] + hands)

while(True):
    playGame()

