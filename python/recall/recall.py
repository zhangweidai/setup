import pygame
import time
import pickle
import random
import traceback
import statistics

from collections import defaultdict
from sortedcontainers import SortedSet

loading_wrong = False
time_allotted = 12

report = ""
# Program to cancel the timer 
import threading 

correct_before = dict()
answer_db = list()
keys = list()
load_map = dict()
thousand = 1000
words_per_session = 16

def get_loaded():
    global answer_db
    global load_map
    global keys
    global correct_before

    with open("db", "r") as f:
        bar = f.readlines()

    tload_map = dict()
    cword = None
    canswers = list()
    tkeys = list()
    for aline in bar:
        aline = aline.replace("\n", "")
        if aline == "":
            tload_map[cword] = canswers
            tkeys.append(cword)
            canswers = list()
            cword = None
        elif cword == None:
            cword = aline
        else:
            canswers.append(aline)

    keys = list()
    load_map.clear()

    if len(tkeys) > words_per_session:
        while (len(keys) < words_per_session):
            cword = random.choice(tkeys)
            if correct_before.get(cword):
                cword = random.choice(tkeys)
            if cword in keys:
                continue

            keys.append(cword)
            answers = tload_map[cword]
            load_map[cword] = answers
            answer_db.extend(answers)
    else:
        keys = tkeys
        for cword in tkeys:
            answers = tload_map[cword]
            answer_db.extend(answers)
        load_map = tload_map

    keys = list(keys)
    answer_db = list(set(answer_db))
    print("\n Available Words : {}".format( len(tkeys)))
    print(" Selected Words : {}\n".format( len(keys)))

get_loaded()
  
wrong_data_path = "wrong_data.pkl"
wrong_mode = True
wrong_count = 0
show_answer = False
def gfg(): 
    global wrong_timer
    global wrong_mode
    wrong_mode = False
    wrong_timer.cancel()

wrong_timer = threading.Timer(2.1, gfg) 

initial_time = time.time()
pygame.init()

display_width = 1800
display_height = 1000

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,160,0)
other = (255,0,255)
yellow = (255,255,0)

def text_objects(text, font, color = white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

CTEXT = ""
FONT_SIZE = 65
def update_font():
    return pygame.font.SysFont( random.choice(available_fonts), FONT_SIZE )

answer_choices = set() 
USER_ANSWER = ""
choices = "asdfghjkl;"
CANSWERS = list()
start_time = None
done = False
lefty = 200

def message_word_answer(word, answer):
    centerd = 80
    TextSurf, TextRect = text_objects(word, CURRENT_FONT, yellow)
    TextRect.center = (lefty, centerd)
    TextRect.left = lefty
    gameDisplay.blit(TextSurf, TextRect)

    for ans in answer:
        centerd += 80
        TextSurf, TextRect = text_objects(ans, CURRENT_FONT)
        TextRect.center = (lefty, centerd)
        TextRect.left = lefty
        gameDisplay.blit(TextSurf, TextRect)


def message_display():
    TextSurf, TextRect = text_objects(CTEXT, CURRENT_FONT, yellow)
    centerd = 80
    TextRect.center = (lefty, centerd)
    TextRect.left = lefty
    gameDisplay.blit(TextSurf, TextRect)

    for i, choice in enumerate(choices):

        answer = "answer"
        p_answer = "{} ) {}".format(choice, answer_choices[i])

        centerd += 80
        show = True
        if show_answer:
            show = True if answer_choices[i] in CANSWERS else False

        if show:
            TextSurf, TextRect = text_objects(p_answer, CURRENT_FONT)
            TextRect.center = (lefty, centerd)
            TextRect.left = lefty
            gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

#def display():
#    global CTEXT
#    message_display(CTEXT)
    
import atexit
@atexit.register
def goodbye():
    global report
    obj = (wrong_dict_time, wrong_dict_answers, correct_before)
    pickle.dump(obj, open(wrong_data_path, "wb"))

    try:
        average = statistics.mean(times)
        report += "\n\naverage time : {} seconds\n".format(average)
    except:
        pass

    with open ("report", "w") as f:
        f.write(report)

        f.write("\ncorrect before: \n{}\n".format("\n".join(correct_before.keys())))

        f.write("\nwrongs:\n")
        for aword, answers in wrong_dict_answers.items():
            f.write("{} - tries: {}\n".format(aword, ", ".join(answers)))

        f.write("\nwrongs elapsed time:\n")
        for aword, answers in wrong_dict_time.items():
            answers = ["{}s".format(str(time)) for time in answers]
            f.write("{} - tries: {}\n".format(aword, ", ".join(answers)))

def isCorrect(answer):
    global wrong_mode
    global wrong_count
    global show_answer
    global report
    global correct_before

    if answer not in CANSWERS:
        wrong_count += 1
        report += " wrong"
        if wrong_count == 2:
            show_answer = True
            report += "\n"
        else:
            wrong_mode = True
            wrong_timer.start()
        wrong_dict_answers[CTEXT].add(answer)

        if CTEXT in correct_before:
            del(correct_before[CTEXT])
        print("wrong_dict_answers: {}".format( wrong_dict_answers))

    else:
        correct_before[CTEXT] = True
        elapsed_time = round(time.time() - start_time)
        report += " correct elapsed time {}\n".format(elapsed_time)
        setAnswerQuestion()


def starting(message):
    good = 0
    while good < 40:
        good += 1

        gameDisplay.fill(green)
        TextSurf, TextRect = text_objects(message, CURRENT_FONT)
        TextRect.center = (int(display_width/2),int(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(20)

def introduction():
    starting("Look Carefully at These Words")
    cword_idx= 0

    word = keys[cword_idx]
    answer = load_map[word]

    gameDisplay.fill(black)
    message_word_answer(word, answer)
    pygame.display.update()

    while cword_idx < len(keys):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_q:
                        quit()
                else :
                    cword_idx += 1

                    try:
                        word = keys[cword_idx]
                        answer = load_map[word]
                        gameDisplay.fill(black)
                        message_word_answer(word, answer)
                        pygame.display.update()
                    except:
                        pass

        clock.tick(20)
    starting("Get Ready!")


saved_fonts = set()
def game_loop():
    global CURRENT_FONT
    global saved_fonts
    global USER_ANSWER
    global show_answer

    introduction()

    pygame.event.clear()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_q:
                        quit()

                    if event.key == pygame.K_a:
                        show_answer = not show_answer

                    if event.key == pygame.K_d:
                        CURRENT_FONT = update_font()

                    if event.key == pygame.K_n:
                        CURRENT_FONT = update_font()
                        setAnswerQuestion()
                        
                else :
                    if show_answer:
                        show_answer = False
                        setAnswerQuestion()
                    else:
                        try:
                            choice = str(event.unicode)
                            idx = choices.index(choice)
                            answer = answer_choices[idx]
                            isCorrect(answer)

                        except:
                            pass

        bg = black if not wrong_mode else red
        if show_answer:
            bg = red

        gameDisplay.fill(bg)
        message_display()
        clock.tick(20)

    endGame()

def endGame():
    good = 0

    while good < 35:
        good += 1

        CURRENT_FONT = update_font()
        gameDisplay.fill(green)
        TextSurf, TextRect = text_objects("Thanks!", CURRENT_FONT)
        TextRect.center = (int(display_width/2),int(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(10)

    exit()


gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
available_fonts_path = "available_fonts.pkl"

try:
    available_fonts = pickle.load(open(available_fonts_path, "rb"))
except:
    available_fonts = list()
    pass

if len(available_fonts) < 5:
    available_fonts = pygame.font.get_fonts()

#print("loaded saved_fonts: {}".format( len(available_fonts)))
CURRENT_FONT = update_font()

##################################################################
# wrong stuff

try:
    wrong_dict_time, wrong_dict_answers, correct_before = pickle.load(open(wrong_data_path, "rb"))
except:
    wrong_dict_time = defaultdict(list)
    wrong_dict_answers = defaultdict(list)
    correct_before = dict()

if not loading_wrong:
    wrong_dict_time = defaultdict(list)
    wrong_dict_answers = defaultdict(set)
    correct_before = dict()
else:
    print("\nwrong_dict_time : {}\n".format( wrong_dict_time ))
    print("\nwrong_dict_answers : {}\n".format( wrong_dict_answers ))
    print("\ncorrect_before : {}\n".format( correct_before ))

#wrong_dict_time["zzzz2"] = [3,4]
#wrong_dict_time["bb"] = [3,24]
#wrong_dict_time["one"] = [24]
#wrong_dict_time["more"] = [13,4]
#wrong_dict_time["zzzze"] = [2,4,5,7]
#wrong_dict_answers["relationship"] = set(["AAAAAAA", "BBBBBBBB"])
#wrong_dict_answers["one"] = set(["AAAAAAA", "BBBBBBBB"])
#wrong_dict_answers["three"] = set(["AAAAAAA", "BBBBBBBB"])

def calc_wrong_ranges():
    wrong_sort = SortedSet()
    running_total = 0
    for dict_answer, the_set in wrong_dict_time.items():
        try:
            average = statistics.mean(the_set)
            running_total += average
            wrong_sort.add((average, dict_answer))
        except:
            print("the_set: {}".format( the_set))
            print("wrong_dict_time: {}".format( wrong_dict_time))
            pass
    
    range_start = 0
    wrong_ranges = list()
    for avg_time, word in wrong_sort:
        range_value = round(avg_time/running_total * thousand)
        start = range_start 
        end = start + range_value 
        wrong_ranges.append([start, end, word])
        range_start = end

    return wrong_ranges

##################################################################

times = list()

def get_a_word_answer():
    global correct_before
    word = None
    answer = None

    wrong_ranges = calc_wrong_ranges()
    has_enough_wrongs = len(wrong_ranges) > 4
    found = False
    if has_enough_wrongs:
        selector = random.randrange(100)

        # 45 percent chance of a previously wrong word
        if selector > 65:
            sub_selector = random.randrange(thousand)
            for start, end, word in wrong_ranges:
                if start <= sub_selector <= end:
                    return word, load_map[word]

    word = random.choice(keys)
    if correct_before.get(word):
        try_again = random.randrange(100)

        # 70 percent chance of a new word if you've gotten this word correct before
        if try_again > 30:
            word = random.choice(keys)
    answer = load_map[word]
    return word, answer

def setAnswerQuestion():
    global CTEXT
    global CANSWERS
    global answer_choices
    global answer_db
    global wrong_mode
    global CURRENT_FONT
    global wrong_count
    global start_time
    global done
    global wrong_dict_time
    global times
    global report

    elapsed_time = round((time.time() - initial_time)) / 60 
    if elapsed_time > time_allotted:
        done = True
        return

    if start_time and CTEXT:
        elapsed_time = round(time.time() - start_time)

        if elapsed_time == 0:
            elapsed_time = 1

        times.append(elapsed_time)

        print("wrong_count : {}".format( wrong_count ))
        if wrong_count:
            report += " elapsed time : {}\n".format(elapsed_time)
            wrong_dict_time[CTEXT].append(elapsed_time)
        else:
            if wrong_dict_time.get(CTEXT):
                new_times = wrong_dict_time.get(CTEXT, list())[1:]
                if new_times:
                    wrong_dict_time[CTEXT] = new_times
                else:
                    del(wrong_dict_time[CTEXT])

    start_time = time.time()

    CURRENT_FONT = update_font()

    wrong_mode = False
    wrong_count = 0

    CTEXT, CANSWERS = get_a_word_answer()

    report += "\n({})".format(CTEXT)

    needed_answers = len(choices)
    answer_choices = set() 
    answer_choices.add(random.choice(CANSWERS))

    prev_wrong = wrong_dict_answers.get(CTEXT, list())

    if prev_wrong:
        prev_wrong = list(prev_wrong)
        random.shuffle(prev_wrong)
        for answer in prev_wrong[:5]:
            answer_choices.add(answer)

    while len(answer_choices) != needed_answers:
        answer_choices.add(random.choice(answer_db))

    answer_choices = list(answer_choices)
    random.shuffle(answer_choices)

setAnswerQuestion()

try:
    game_loop()
    quit()
except Exception as e:
    traceback.print_exc() 
    print (e)
