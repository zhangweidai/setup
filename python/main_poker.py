from deuces import Deck
from deuces import Card
from deuces import Evaluator
import random

minBet = 10
maxBet = minBet * minBet
money_ = 100

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    def __int__(self, name):
        if name == "BET":
            return 0
        if name == "FOLD":
            return 1
        if name == "PASS":
            return 2

    def __str__(self, index):
        if index == 0:
            return "BET"
        if index == 1:
            return "FOLD"
        if index == 2:
            return "PASS"

    def __getitem__(self, index):
        if index == 0:
            return "BET"
        if index == 1:
            return "FOLD"
        if index == 2:
            return "PASS"
        return "BET"

Actions = Enum(["BET", "FOLD", "PASS"])

def numberOfPlayers():
    return 1

def getActiveActor():
    return random.randint(0, numberOfPlayers())

def getCompAction():
    return Actions[random.randint(1, len(Actions))]

def getCompBet():
    return random.randint(minBet, maxBet)

def loopIt():
    turn = getActiveActor()
    if turn == 0:
        play = raw_input("Action: (b)et, (f)old, (r)aise : ")
        if play == "b":
            print "Betting"
        elif play == "f":
            print "Folding"
    else:
        compPlay = getCompAction()
        if compPlay == Actions.BET:
            compBet = getCompBet()
            print compBet
        elif compPlay == Actions.FOLD:
            print "pass"

    loopIt()



def playGame():
    deck = Deck()
    board = deck.draw(3)

    Card.print_pretty_cards(board)

    player1_hand = deck.draw(2)
    print "Your Hand:"
    Card.print_pretty_cards(player1_hand)

    for comp in range(numberOfPlayers()):
        hand = deck.draw(2)
        Card.print_pretty_cards(hand)
    
    loopIt()



evaluator = Evaluator()

play = raw_input("want to play: ")
while (play == "y"):
    playGame()
    play = raw_input("want to play: ")


#print evaluator.hand_summary(board, [player1_hand, player2_hand])
#print evaluator.evaluate(board, player2_hand)
