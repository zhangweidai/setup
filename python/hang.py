#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import urlparse
import pickle
import random

def setup():
    words = ["rabbit", "bunny", "carrot"]


def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]

words = ["rabbit", "bunny", "carrot"]
PORT_NUMBER = 8080
guesses = {}
guesses["default"] = ""
game = {}
game["default"] = random.choice(words)
letters = "abcdefghijklmnopqrstuvwyz"
cnextLetter = 0

def pretty(word):
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

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        if self.path.startswith("/favicon.ico"):
            return
        currentCount = 0
        namestr = "default"

        parsed_path = urlparse.urlparse(self.path)
        myDic = parseParse(parsed_path.query)
        if len(myDic) > 0:
            currentCount = int(myDic["count"])
            namestr = myDic["id"]

        self.writePage(namestr, currentCount)


    #Handler for the POST requests
    def do_POST(self):
        global guesses, game
        global cnextLetter
        currentCount = 0
        namestr = "default"

        form = None
        letter = ""
        if "cheat" in self.path:
            letter = nextLetterFrom(game[namestr])
            
        if "newgame" in self.path:
            print "newgame"
            cnextLetter = 0
            game[namestr] = random.choice(words)
            guesses[namestr] = ""

        if "guess" in self.path:
            form = cgi.FieldStorage(fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type'],
            })

            if form.has_key("letter"):
                letter = form["letter"].value

        #if "?" in self.path or "cheat" in self.path:
        parsed_path = urlparse.urlparse(self.path)
        print "parsed_path"
        print parsed_path
        myDic = parseParse(parsed_path.query)
        print myDic
        if not len(myDic) == 0:
            currentCount = int(myDic["count"])
            namestr = myDic["id"]
        else :
            currentCount = len(guesses[namestr])

        guesses[namestr] += letter

        currentCount += 1
        self.writePage(namestr, currentCount)
        return


    def writePage(self, namestr, currentCount):
        self.send_response(200)
        self.end_headers()
        guessesSoFar = showOnly(guesses[namestr], currentCount)
        word = game[namestr]
        vword = underscored(guessesSoFar, word)
        win = ""
        if (vword == word):
            win = '<h1>Win</h1>\
</form>'

        html = '\
<html>\
<h3> game is for : {} </h3>\
<h3> word is: {} </h3>\
<h3> user visible word is: {} </h3>\
<h3> guesses so far {} </h3>\
<form method="POST" action="/cheat">\
<input type="submit" value="cheat"/>\
</form>\
<form method="POST" action="/newgame">\
<input type="submit" value="newgame"/>\
</form>\
<form method="POST" action="/guess?id={}?count={}">\
<input type="text" name="letter"/>\
<input type="submit" value="guess"/>\
{}\
</form>'.format(
        namestr,
        word, 
        pretty(vword), 
        guessesSoFar, 
        namestr, 
        currentCount, 
        win)

        self.wfile.write(html)

#try:
#    #Create a web server and define the handler to manage the
#    #incoming request
#    server = HTTPServer(('', PORT_NUMBER), myHandler)
#    print 'Started httpserver on port ' , PORT_NUMBER
#    	
#    #Wait forever for incoming htto requests
#    server.serve_forever()
#
#except KeyboardInterrupt:
#    print '^C received, shutting down the web server'
#    server.socket.close()
