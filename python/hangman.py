#!/usr/bin/python
import cgi
import random
import copy
import string

MAX_MISSES = 8
LOST_RECORD = '|'
NOMOREWORDS = "No More Words"
NOTAMPER = "No Tampering"
COUNT = "count"
ID = "id"
DEBUG = "debug"
VALID_QUERY_KEYS = [COUNT, ID, DEBUG]
defaultId = None
GLOBALWORDS = ["rabbit", "bunny", "carrot", "lettuce", "burrow", "fluffy", "floppy", "litter", "pellets"]

# holds all created games
games = {}

#######################################################

class GameInfo():
    def __init__(self):
        self.newGame()

    # prepares all the data for a new game
    def newGame(self):
        self.words = list(GLOBALWORDS)
        random.shuffle(self.words)
        self.guesses = ""
        self.currentCount = 0

    def getNextCount(self):
        return self.currentCount + 1

    def randomizeRemainingWords(self):
        cIdx = self.getCurrentWordIdx()
        wordsSaved = self.words[0 : cIdx + 1]
        shuffleWords = self.words[cIdx + 1:]
        random.shuffle(shuffleWords)
        self.words = wordsSaved  + shuffleWords

    def getCurrentCount(self):
        return self.currentCount

    def getUndoCount(self):
        return self.currentCount - 1

    def getNumOfCorrectWords(self):
        correct = 0
        activeGuesses = self.guesses[0:self.currentCount]
        for guess in activeGuesses:
            if guess.isdigit():
                correct += 1
        return correct

    def getGuessesLeft(self):
        incorrects = MAX_MISSES
        cWord = self.getCurrentWord()
        activeGuesses = self.guesses[0:self.currentCount]
        for char in reversed(activeGuesses):
            if char.isdigit():
                cWord = self.words[int(char)]
            elif char not in cWord:
                incorrects -= 1

            if incorrects == 0:
                return 0
        return incorrects

    def getGuesses(self):
        return self.guesses

    def noGuesses(self):
        return len(self.guesses) == 0

    def getCurrentWordIdx(self):
        if self.noGuesses():
            return 0

        activeGuesses = self.guesses[0:self.currentCount]
        for char in reversed(activeGuesses):
            if char.isdigit():
                return int(char)+1
        return 0

    def getCurrentWord(self):
        if self.currentCount < len(self.guesses) and self.guesses[self.currentCount].isdigit():
            return self.words[self.getCurrentWordIdx()]

        activeGuesses = self.guesses[0:self.currentCount]
        for undoItem in reversed(activeGuesses):

            # no more words
            if undoItem.isdigit():
                nextIdx = int(undoItem) + 1
                if nextIdx >= len(self.words):
                    return NOMOREWORDS
                return self.words[nextIdx]
        return self.words[0]

    def getWinState(self):
        if self.noGuesses() or self.currentCount == 0:
            return None

        undoItem = self.guesses[self.currentCount-1]
        if undoItem.isdigit():
            return True
        elif undoItem == LOST_RECORD or self.getGuessesLeft() == 0:
            return False
        return None

    # compare user entered word with the current word
    def processWordGuesses(self, undoItem):
        if len(undoItem) <= 1:
            return undoItem

        if undoItem == self.getCurrentWord():
            return self.getCurrentWordIdx()
        else:
            return LOST_RECORD

    def appendToUndoStack(self, undoItem, formCount):
        if not undoItem:
            return

        increment = 0
        if formCount == self.currentCount:
            increment = 1
        undoItem = self.processWordGuesses(undoItem)

        if self.getCurrentWord() == self.getUserVisibleWord(undoItem):
            undoItem = self.getCurrentWordIdx()

        if self.currentCount > len(self.guesses):
            self.guesses += undoItem
        else:
            newGuess = self.guesses[:formCount-increment]+str(undoItem)
            self.guesses = newGuess
            if not increment == 1:
                self.currentCount += 1

    def setCurrentCount(self, newCurrentCount):
        self.currentCount = newCurrentCount

    def getUserVisibleWord(self, tryLetter = None):
        if self.currentCount > len(self.guesses) and self.guesses[self.currentCount].isdigit():
            return self.getCurrentWord()
        ret = ""
        for letter in self.getCurrentWord():
            if letter in self.getCurrentGuesses() or letter == tryLetter:
                ret += letter
            else:
                ret += "_"
        return ret

    def getCurrentGuesses(self):
        index = 0 
        activeGuesses = self.guesses[0:self.currentCount]
        for i,undoItem in enumerate(reversed(activeGuesses)):
            if undoItem == LOST_RECORD or undoItem.isdigit():
                index = len(activeGuesses) - i
                break
        return self.guesses[index:self.currentCount]

#######################################################

def spaced(word):
    ret = ""
    for letter in word:
        ret += letter + " "
    return ret

def getUndoBtn(gameId, game, currentCount, debugging):
    return '\
<form method="POST" action="/{debug}?{id}={gameId}?{count}={gameCount}">\
<input type="submit" value="undo"/ {disabled}></form>'.format(
        debug = debugging,
        id = ID,
        gameId = gameId, 
        count = COUNT,
        gameCount = game.getUndoCount(),
        disabled = "disabled" if currentCount < 1 else "")

def getUserVisibleText(game):
    return '\
<h3> user visible word is: {word} </h3>\
<h3> current guessed letters : {letters} </h3>\
<h3> guesses left : {left} </h3>\
<h3> number of correct words guessed: {correct} out of {total}</h3>\
'.format(
        word = spaced(game.getUserVisibleWord()),
        letters = game.getCurrentGuesses(),
        left = game.getGuessesLeft(),
        correct = game.getNumOfCorrectWords(),
        total = len(GLOBALWORDS)
        )

def getGuessForm(gameId, game, currentWord, debugging):
    disableGuess = "disabled" if currentWord == NOMOREWORDS else ""
    return '\
<form method="POST" action="/{}?id={}?count={}">\
<input type="text" name="letter"/ autocomplete="off" {}>\
<input type="submit" value="guess" {}/></form>'.format(
        debugging,
        gameId, 
        game.getNextCount(),
        disableGuess,
        disableGuess)

def getDebugMsgs(gameId, currentWord, game):
    return '<hr>\
<h3> game is for : {} </h3>\
<h3> word is: {} </h3>\
<h3> guessed letters total : {} </h3>\
<h3> currentCount : {} </h3>\
<h3> size of undo : {} </h3><hr>\
'.format(
        gameId,
        currentWord,
        game.getGuesses(),
        game.getCurrentCount(),
        str(len(game.getGuesses())))

newGameBtn = '\
<form method="POST" action="/{}">\
<div data-tip="Restart everything over.  Clear undo history">\
<input type="submit" value="Start Over"/></div></form>'\

def generateRandomId():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for character in range(8))

def getGameCopy(sourceId):
    global games
    game = None
    if copy and games.has_key(sourceId):
        game = copy.deepcopy(games[sourceId])
        game.randomizeRemainingWords()
    else:
        return None, None
#        game = GameInfo()

    gameId = generateRandomId()
    games[gameId] = game
    return game, gameId

def getGame(gameId):
    global games
    if not games.has_key(gameId):
        games[gameId] = GameInfo()
    return games[gameId]


# returns None if parsed query string contains invalid keys
# returns a query map of valid keys
def parseQueryString(string):
    ret = {COUNT : None, ID : None}
    tokens = string.split("?")
    for b in tokens:
        keys = b.split("=")
        if len(keys) == 2:
            cKey = keys[0]
            if not cKey in VALID_QUERY_KEYS:
                return None
            ret[cKey] = keys[1]
    return ret

def generateHTML(gameId, debugging):
    global games
    game = games[gameId]

    msg = ""
    winState = game.getWinState()
    if winState == True:
        msg += '<h1>Correct Guess, Next Word</h1>'
    elif winState == False:
        msg += '<h1>Wrong Guess. Please Undo or Start a New Game.</h1>'
    else:
        # help with spacing 
        msg += '<h1>HangMan</h1>'

    currentCount = game.getCurrentCount()

    currentWord = game.getCurrentWord()

    guessForm = getGuessForm(gameId, game, currentWord, debugging)
    if currentWord == NOMOREWORDS:
        msg = '<h1> No more words to guess. </h1>'
    elif not winState == False:
        msg += getUserVisibleText(game)
        
    if debugging:
        msg += getDebugMsgs(gameId, currentWord, game);

    if not winState  == False:
        msg += guessForm

    msg += getUndoBtn(gameId, game, currentCount, debugging)
    msg += newGameBtn.format(debugging)
    
    return '<html> {} </html>'.format(msg)


def validPath(path):
    if path == "/":
        return True
    return False

#Handler for the GET/POST requests
def playHangMan(env):
    global defaultId
    query = env['QUERY_STRING']
    path = env['PATH_INFO']

    if "favicon" in path:
        return ""

    if not validPath(path):
        return NOTAMPER

    parsedData = parseQueryString(query)

    if parsedData == None:
        return NOTAMPER

    game = None
    gameId = parsedData[ID]
    method = env['REQUEST_METHOD']

    # determine what game we are playing:
    if method == "GET" and gameId:
        # GET and passed in GameId when user pastes URL, thus gets a game copy
        game, gameId = getGameCopy(gameId)
        if game == None:
            return NOTAMPER
    else:
        # get existing game or new game based on parsed gameId
        if defaultId == None:
            gameId = generateRandomId()
            # reuse a default Id when one has been created and non passed in.
            defaultId = gameId
        else:
            gameId = defaultId
        game = getGame(gameId)

    form = None
    letter = ""

    # debug mode allows additional developer information
    debugging = ""
    if parsedData.has_key(DEBUG):
        debugging = "?debug=1"

    if not query or (parsedData[COUNT] == None and debugging):
        game.newGame()

    else:
        form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env)

        if form.has_key("letter"):
            # qualify letter received from form
            letter = form["letter"].value
            letter = letter.lower()
            if letter in game.getCurrentGuesses() or not letter.isalpha():
                letter = ""

        formCount = int(parsedData[COUNT])
        if not formCount == None and formCount <= len(game.getGuesses()):
            # process undo and game discontinuity
            game.setCurrentCount(formCount)

        if letter:
            game.appendToUndoStack(letter.lower(), formCount)

    return generateHTML(gameId, debugging)


# required for wsgi
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return playHangMan(env)
