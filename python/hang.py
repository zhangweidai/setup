#!/usr/bin/python
from os import curdir, sep
import cgi
import random

MAX_MISSES = 2
LOST_RECORD = '|'

print "!!!!!!!!!!!!!!!!!!!!!!!!!!!"

#class GameInfo():



guesses = {}
guesses["default"] = ""
game = {}
letters = "abcdefghijklmnopqrstuvwyz"
cnextLetter = 0

words = ["rabbit", "bunny", "carrot"]
game["default"] = random.choice(words)

print words

def appendToGuesses(gameId, state, currentCount):
    global guesses

    if currentCount > len(guesses[gameId]):
        guesses[gameId] += state
    else:
        newGuess = guesses[gameId][:currentCount]+state
        print "newGuess"
        print newGuess
        guesses[gameId] = newGuess
        currentCount += 1
    return currentCount

def getCurrentGuesses(guessesSoFar):
    if not LOST_RECORD in guessesSoFar:
        return guessesSoFar
    index = guessesSoFar.rfind(LOST_RECORD)
    what =  guessesSoFar[index+1:]
    return what



def countIncorrects(underscoredWord, guessesSoFar):
    missed = 0
    currentGuesses = getCurrentGuesses(guessesSoFar)
    for guess in guessesSoFar:
        if guess not in underscoredWord:
            missed += 1
    return missed


def spaced(word):
    ret = ""
    for letter in word:
        ret += letter + " "
    return ret

def underscored(guesses, word):
    ret = ""
    for letter in word:
        if letter in guesses:
            ret += letter
        else:
            ret += "_"
    return ret

def nextLetterFrom(letters):
    global cnextLetter
    ret = letters[cnextLetter:cnextLetter+1]
    cnextLetter += 1
    return ret

def nextLetter(usedLetters):
    global cnextLetter
    ret = letters[cnextLetter:cnextLetter+1]
    cnextLetter += 1
    while ret in usedLetters and cnextLetter < len(letters):
        ret = letters[cnextLetter:cnextLetter+1]
        cnextLetter += 1

    return ret

def showOnly(namestr, currentCount):
    print "show only"
    print currentCount
    return namestr[:currentCount]

def parseParse(string):
    ret = {}
    tokens = string.split("?")
    for b in tokens:
        keys = b.split("=")
        if len(keys) == 2:
            ret[keys[0]] = keys[1]
        else:
            print "got this instead {} {}".format(len(keys), keys)
    return ret

def writePage(gameId, currentCount, letter):
    guessesSoFar = showOnly(guesses[gameId], currentCount)

    print "guessesSoFar" + guessesSoFar
    currentGuesses = getCurrentGuesses(guessesSoFar)
    print "currentGuesses" + currentGuesses

    word = game[gameId]
    underscoredWord = underscored(currentGuesses, word)

    msg = ""
    if (underscoredWord == word):
       msg += '<h1>Win</h1>'

    cheatBtn = '\
<form method="POST" action="/cheat">\
<input type="submit" value="Cheat"/></form>'\

    newGameBtn = '\
<form method="POST" action="/newgame">\
<input type="submit" value="Start Over"/></form>'\

    undoBtn = '\
<form method="POST" action="/guess?id={}?count={}">\
<input type="submit" value="undo"/ {}></form>'.format(
        gameId, 
        currentCount-1,
        "disabled" if currentCount < 1 else "")

    redoBtn = '\
<form method="POST" action="/guess?id={}?count={}">\
<input type="submit" value="redo"/ {}></form>'.format(
        gameId, 
        currentCount+1,
        "" if currentCount < len(guesses[gameId]) else "disabled")

    increment = 0
    if letter:
        increment = 1

    guess = '\
<form method="POST" action="/guess?id={}?count={}">\
<input type="text" name="letter"/ autocomplete="off">\
<input type="submit" value="guess"/></form>'.format(
        gameId, 
        currentCount + increment)

    incorrect = countIncorrects(underscoredWord, currentGuesses)

    msg += '\
<h3> game is for : {} </h3>\
<h3> word is: {} </h3>\
<h3> user visible word is: {} </h3>\
<h3> current guessed letters : {} </h3>\
<h3> guessed letters total : {} </h3>\
<h3> incorrect guesses: {} </h3>\
'.format(
        gameId,
        word, 
        spaced(underscoredWord), 
        currentGuesses,
        guessesSoFar,
        str(incorrect)
        ) 

    if incorrect >= MAX_MISSES:
        nextGameBtn = '\
<form method="POST" action="/nextgame?id={}?count={}">\
<input type="submit" value="Next Game"/></form>'.format(
        gameId, 
        currentCount + 1)

        msg += "<h2>Game Lost</h2>"
        msg += nextGameBtn
    else:
        msg += cheatBtn
        msg += undoBtn
        msg += redoBtn
        msg += guess
    msg += newGameBtn
    
    return '<html> {} </html>'.format(msg)


#Handler for the POST requests
def getHtml(env):
    query = env['QUERY_STRING']
    path = env['PATH_INFO']

    if "favicon" in path:
        return ""
    print "query"
    print query
    print "path"
    print path

    global guesses, game
    global cnextLetter

    currentCount = 1
    gameId = "default"

    form = None
    letter = ""
    noGuess = False
    if "cheat" in path:
        letter = nextLetterFrom(game[gameId])
        print letter
        
    if "newgame" in path:
        print "newgame"
        cnextLetter = 0
        game[gameId] = random.choice(words)
        guesses[gameId] = ""

    if "guess" in path:
        input = env['wsgi.input']
        form = cgi.FieldStorage(
                fp=input,
                environ=env)

        if form.has_key("letter"):
            letter = form["letter"].value
        else:
            noGuess = True


    #if "?" in self.path or "cheat" in self.path:
    if query:
        myDic = parseParse(query)

        if not len(myDic) == 0:
            print "fromA"
            currentCount = int(myDic["count"])
            gameId = myDic["id"]
        else :
            print "fromB"
            currentCount = len(guesses[gameId])

    if "nextgame" in path:
        print "currentCount"
        print currentCount
        currentCount = appendToGuesses(gameId, LOST_RECORD, currentCount)

        print "currentCount"
        print currentCount
        return writePage(gameId, currentCount, '')


    if letter:
        print "this is my letter : "  + letter
        print "this is my currentCount : " + str(currentCount)
        print "this is my len  of guesses: " + str(len(guesses[gameId]))
        currentCount = appendToGuesses(gameId, letter, currentCount)

    return writePage(gameId, currentCount, letter)

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    html = getHtml(env)
    return html
