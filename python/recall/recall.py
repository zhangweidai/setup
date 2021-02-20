import pygame
import time
import pickle
import random
import traceback
import statistics
import os
from collections import defaultdict
from sortedcontainers import SortedSet
import threading 
import atexit
from datetime import datetime
import glob

pygame.init()

standard = 1080
infoObject = pygame.display.Info()
factor = infoObject.current_h / standard

did_answer_a_question = False
spacing = int(50 * factor)
lefty = spacing
FONT_SIZE = int(35*factor)
display_width = int(1500 * factor)
display_height = int(740 * factor)

centerwidth =  int(display_width/2)
centerheight =  int(display_height/2)

bottom = int(40 * factor)
center_start = int(80 * factor)
save = True
loading_wrong = True
wrong_dict_answers = None
wrong_dict_time = defaultdict(list)
word_elapsed_time = defaultdict(list)

time_allotted = 5
use_all = True
words_per_session = 20
seen_before_repeat = 20

report = ""
wrong_data_path = "wrong_data.pkl"
wrong_mode = True
wrong_count = 0
show_answer = False
correct_before = defaultdict(str)
answer_db = list()
keys = list()
load_map = dict()
all_map = dict()
thousand = 1000
progress = 0
mastery = 0
na = "N/A"

session_saved = list()
maxrange_score = 0
range_dict = defaultdict(list)
initial_time = None
CUR_WORD = ""
times = list()

answer_choices = set() 
choices = "asdfghjk"
lenchoices = len(choices)
CANSWERS = list()
start_time = None
done = False
CURRENT_FONT = None

black = (0,0,0)
grey = (120,120,120)
white = (255,255,255)
red = (195,0,0)
green = (0,160,0)
other = (255,0,255)
yellow = (255,255,0)

gameDisplay = None
clock = None

def correct_before_last(aword):
    try:
        return correct_before.get(aword, "")[-1] == "p"
    except:
        return False

def load_a_really_good_word():
    cword = load_a_good_word()

    # try one more time to not get a word that was passed
    last = correct_before.get(cword, "f")
    if last[-2:] == "pp":
        cword = load_a_good_word()

        last = correct_before.get(cword, "f")
        if last[-1] == "p":
            cword = load_a_good_word()

    last = correct_before.get(cword, "f")
    ctr = 0
    while last[-4:] == "pppp" and ctr < 5:
        cword = load_a_good_word()
        last = correct_before.get(cword, "f")
        ctr += 1

    return cword


def load_a_good_word():
    generated = random.randrange(maxrange_score)
    for word, arange in range_dict.items():
        if arange[0] <= generated <= arange[1]:
            return word
    return word

def setup_ranges():
    global maxrange_score 
    global range_dict 
    cmax = 0
    avg = list()
    range_dict.clear()

    for aword in all_map.keys():
        score = correct_before.get(aword, "")
        leny = len(score)
        avg.append(leny)
        if leny > cmax:
            cmax = leny

    avg = round(statistics.mean(avg))

    cmax += 2
    ocmax = cmax
    cmax = cmax * cmax
    start = 0
    end = 0

    for aword in all_map.keys():
        score = correct_before.get(aword, "")
        fails = score.count("f")
        passes = score.count("p")
        bonus = ocmax * 2 if score and score[-1] == "f" else 0
        bonus += -1*(ocmax*2) if score and score[-1] == "p" else 0

        len_score = len(score)

        if len_score < avg:
            bonus += ocmax

        if len_score == 0:
            bonus += (cmax + ocmax)

        word_score = round(cmax + (fails * ocmax) - (passes * 4 * ocmax) + bonus)
        if word_score <= 0:
            word_score = ocmax
        end = start + word_score

        range_dict[aword] = [start, end]
        start = end + 1

    maxrange_score = end
#    print("\nmaxrange_score  : {}".format( maxrange_score  ))
#    print("\nranges: {}".format( range_dict))

def get_loaded():
    global answer_db
    global load_map
    global all_map
    global keys
    global report
    global words_per_session
    global progress
    global mastery

    with open("db.txt", "r") as f:
        bar = f.readlines()

    all_map = dict()
    cword = None
    canswers = list()
    temp_word_list = list()

    for aline in bar:
        aline = aline.replace("\n", "").strip()
        if aline == "" and cword:
            all_map[cword] = canswers
            temp_word_list.append(cword)
            canswers = list()
            cword = None
        elif cword == None:
            cword = aline
        else:
            if aline:
                canswers.append(aline)

    keys = list()
    load_map.clear()
    progress = 0
    for db_word in temp_word_list:

        if correct_before.get(db_word, "")[-5:].count("p") == 4:
            mastery += 1

        if correct_before_last(db_word):
            progress += 1

    report += "last correct {} out of {}\n".format(str(progress), str(len(temp_word_list)))

    items_in_wrong = 0
    for key, wrongs in wrong_dict_answers.items():
        items_in_wrong += len(wrongs)

    report += "items in wrong {}\n".format(str(items_in_wrong))

    setup_ranges()
    if use_all:
        words_per_session = len(temp_word_list)

    i = 0
    if len(temp_word_list) > words_per_session:

        while (len(keys) < words_per_session):
            cword = load_a_really_good_word()
            if cword in keys:
                continue

            keys.append(cword)
            answers = all_map.get(cword)
            load_map[cword] = answers
            answer_db.extend(answers)
    else:
        keys = temp_word_list
        for cword in temp_word_list:
            answers = all_map.get(cword)
            answer_db.extend(answers)
        load_map = all_map

    keys = list(keys)
    answer_db = list(set(answer_db))

    print("\n Available Words : {}".format( len(temp_word_list)))
    print(" Selected Words : {}\n".format( len(keys)))

    print("keys : {}".format( keys ))

def problem():
    for a_key in keys:
        if a_key not in load_map:
            print ("problem with {}".format(a_key))
            traceback.print_stack()
            exit()
  
def text_objects(text, font, color = white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def get_instruction_font(size = int(FONT_SIZE/1.2)):
    if used_resource_font:
        return pygame.font.SysFont("calibri", size)
    return pygame.font.SysFont( available_fonts[1], size)

cfont_name = None
def update_font():
    global cfont_name
    cfont_name = random.choice(available_fonts)
    if not used_resource_font:
        return pygame.font.SysFont(cfont_name, FONT_SIZE )
    return pygame.font.SysFont("calibri", FONT_SIZE )

def message_word_answer(word, answer):
    centerd = center_start
    TextSurf, TextRect = text_objects(word, CURRENT_FONT, yellow)
    TextRect.center = (lefty, centerd)
    TextRect.left = lefty
    gameDisplay.blit(TextSurf, TextRect)

    for ans in answer:
        centerd += center_start
        TextSurf, TextRect = text_objects(ans, CURRENT_FONT)
        TextRect.center = (lefty, centerd)
        TextRect.left = lefty
        gameDisplay.blit(TextSurf, TextRect)

def show_try_again():
    TextSurf, TextRect = text_objects("Try again", get_instruction_font(int(FONT_SIZE * 1.5)), red)
    centerd = center_start
    TextRect.center = (10, int(display_height - (bottom * 3.5)))
    TextRect.left = lefty
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def show_press_any_key_to_continue(msg = "That's the answer.  Please press any key to continue."):
    TextSurf, TextRect = text_objects(msg, get_instruction_font(), white)
    centerd = center_start
    TextRect.center = (10, display_height - bottom - bottom )
    TextRect.left = lefty
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


def show_question_answers():
    TextSurf, TextRect = text_objects(CUR_WORD, CURRENT_FONT, yellow)
    centerd = center_start
    TextRect.center = (lefty, centerd)
    TextRect.left = lefty
    gameDisplay.blit(TextSurf, TextRect)

    for i, choice in enumerate(choices):

        answer = "answer"
        p_answer = "{} ) {}".format(choice, answer_choices[i])

        centerd += spacing
        show = True
        if show_answer:
            show = True if answer_choices[i] in CANSWERS else False

        if show:
            TextSurf, TextRect = text_objects(p_answer, CURRENT_FONT)
            TextRect.center = (lefty, centerd)
            TextRect.left = lefty
            gameDisplay.blit(TextSurf, TextRect)

        if show_answer:
            show_press_any_key_to_continue()

    pygame.display.update()

def display_quit(and_report = False):
    TextSurf, TextRect = text_objects("shift + q : to quit", get_instruction_font(), color = grey)
    TextRect.center = (10, display_height - bottom)
    TextRect.left = lefty
    gameDisplay.blit(TextSurf, TextRect)
    if and_report:
        TextSurf, TextRect = text_objects("shift + r : to open report", get_instruction_font(), color = grey)
        TextRect.center = (10, display_height - bottom - bottom)
        TextRect.left = lefty
        gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def save_pickle():
    obj = (wrong_dict_time, wrong_dict_answers, correct_before, word_elapsed_time)
    print("word_elapsed_time: {}".format( word_elapsed_time))
    print("correct_before: {}".format( correct_before))
    pickle.dump(obj, open(wrong_data_path, "wb"))

@atexit.register
def goodbye():
    global report
    global correct_before

    if not did_answer_a_question:
        return

    if save:
        for aword, items in correct_before.items():
            correct_before[aword] = items[-12:] 
        save_pickle()

    try:
        average = statistics.mean(times)
        report += "\n\naverage time : {} seconds\n".format(average)
    except:
        pass

    with open ("report_{}.txt".format(str(time.time())), "w") as f:
        f.write(report)

        f.write("correct_before:\n")
        for aword in all_map.keys():
            tally = correct_before.get(aword, "")
            try:
                calc = round(tally.count("p")/len(tally),2)
            except:
                calc = 0.0
            f.write("{}: {} {}\n".format(aword, tally, calc))

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
            wrong_mode = False
        else:
            wrong_mode = True
        wrong_dict_answers[CUR_WORD].add(answer)
        correct_before[CUR_WORD] += "f"
    else:

        correct_before[CUR_WORD] += "p"
        elapsed_time = round(time.time() - start_time)
        report += " correct elapsed time {}\n".format(elapsed_time)
        setAnswerQuestion()
        wrong_mode = False



def playSound(word):
    try:
        word = word.replace(" ", "_")
        path = os.path.join(os.getcwd(), "sounds", "{}.mp3".format(word))
        if not os.path.exists(path):
            return

        pygame.mixer.music.load(path)
        pygame.mixer.music.play(1)
    except:
        pass

def get_next_show_word():
    word = keys[get_next_show_word.cword_idx]
    answer = load_map.get(word)
    last = correct_before.get(word, "f")
    while last[-2:] == "pp" and last.count("f") < 4 :
        get_next_show_word.cword_idx += 1
        word = keys[get_next_show_word.cword_idx]
        last = correct_before.get(word, "f")
        answer = load_map.get(word)

    get_next_show_word.cword_idx += 1
    return word, answer
get_next_show_word.cword_idx = 0

def introduction():
    global keys
    global load_map

    def starting(message):
        good = 0
        while good < 40:
            good += 1
            gameDisplay.fill(green)
            TextSurf, TextRect = text_objects(message, CURRENT_FONT)
            TextRect.center = (centerwidth, centerheight)
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
            clock.tick(20)

    starting("Look Carefully at These Words")
    cword_idx= 0

    try:
        word, answer = get_next_show_word()
    except:
        starting("No Show words!")
        exit()

    gameDisplay.fill(black)
    message_word_answer(word, answer)
    playSound(word)
    show_press_any_key_to_continue("Press any key to look at the next word.")

    pygame.display.update()
    clock.tick(20)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    pygame.quit()
                    quit()

                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_q:
                        pygame.event.clear()
                        pygame.quit()
                        quit()
                else :

                    try:
                        word, answer = get_next_show_word()
                        gameDisplay.fill(black)
                        message_word_answer(word, answer)
                        playSound(word)
                        show_press_any_key_to_continue("Press any key to look at the next word.")
                        pygame.display.update()
                    except Exception as e:
                        done = True
                        pass

        clock.tick(20)
    starting("Get Ready!")

#shift
def genreport_data():
    size = 100000
    db_dict = defaultdict(int)
    for count in range(size):
        cword = load_a_really_good_word()
        db_dict[cword] += 1

    printed = 0
    perfects = list()

    wrong_sort = SortedSet()

    report_dict = dict()
    new_words = list()

    for aword in all_map.keys():
        score = correct_before.get(aword, "")
        value = db_dict[aword]
        perc = str(round((value / size) * 100,3))
        try:
            correct_percentage = round(score.count("p")/len(score),3)
            wrong_sort.add((correct_percentage, aword))
            correct_percentage = str(round(correct_percentage * 100,2))
        except:
            correct_percentage = "NA"
            new_words.append(aword)
        report_dict[aword] = [score, correct_percentage, perc]
        print("{} , report_dict: {}".format( aword, report_dict[aword]))

    return report_dict, wrong_sort, new_words



def refresh_report():
    gameDisplay.fill(black)
    report_dict, wrong_sort, new_words =  genreport_data()
    font = get_instruction_font()
    small = get_instruction_font(int(FONT_SIZE/2))
    lastTop = 10
    if len(wrong_sort) > 0:
        lastTop = show_top_missed(small, wrong_sort, report_dict)
    new_words_str = ", ".join(new_words)
    print("lastTop : {}".format( lastTop ))
    rect = pygame.Rect(0, lastTop , display_width, int(300 * factor))
    size = int(30*factor)
    msg = "{{size {}}} All words have been seen.".format(size)
    print("new_words: {}".format( new_words))
    if len(new_words) != 0:
        msg = "{{size {}}} New Words: {}".format(size, new_words_str)
    sftext = SFText(text=msg, screen_rect = rect, font_path=os.path.join('.', 'resources'))
    sftext.on_update()


def show_report():
    done = False
    refresh_report()
    display_quit()

    while not done:
        for event in pygame.event.get():
            if event.type != pygame.KEYDOWN:
                continue
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if event.key == pygame.K_q:
                    pygame.event.clear()
                    pygame.quit()
                    quit()

        clock.tick(20)


def show_top_missed(font, wrong_sort, report_dict):
    col2 = int(250 * factor)
    col3 = int(400 * factor)
    col4 = int(550 * factor)
    col5 = int(740 * factor)

    TextSurf, TextRect = text_objects("Top words missed", font, color=yellow)
    TextRect.top = 10
    TextRect.left = 10
    gameDisplay.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Results", font, color=yellow)
    TextRect.top = 10
    TextRect.left = col2
    gameDisplay.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("% Correct", font, color=yellow)
    TextRect.top = 10
    TextRect.left = col3
    gameDisplay.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("% select", font, color=yellow)
    TextRect.top = 10
    TextRect.left = col4
    gameDisplay.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("avg time (sec)", font, color=yellow)
    TextRect.top = 10
    TextRect.left = col5
    gameDisplay.blit(TextSurf, TextRect)

    lastTop = 0
    spacing_size = (FONT_SIZE/1.5)

    for i, aset in enumerate(wrong_sort[:20]):
        aword = aset[1]
        TextSurf, TextRect = text_objects(aword, font)

        lastTop = int(10 + ((1 + i) * spacing_size))
        TextRect.top = lastTop
        TextRect.left = 40
        gameDisplay.blit(TextSurf, TextRect)

        score , correct_percentage, perc = report_dict[aword]

        TextSurf, TextRect = text_objects(score, font)
        TextRect.top = lastTop
        TextRect.left = col2
        gameDisplay.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects(correct_percentage, font, color = red)
        TextRect.top = lastTop
        TextRect.left = col3
        gameDisplay.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects(perc, font)
        TextRect.top = lastTop
        TextRect.left = col4
        gameDisplay.blit(TextSurf, TextRect)

        try:
            avg_time = str(round(statistics.mean(word_elapsed_time.get(aword, [])[-10:]),2))
        except:
            avg_time = "na"

        TextSurf, TextRect = text_objects(avg_time, font)
        TextRect.top = lastTop
        TextRect.left = col5
        gameDisplay.blit(TextSurf, TextRect)


    bar = list()
    for aword, answers in word_elapsed_time.items():
        bar.append(statistics.mean(answers))
    try:
        avg = round(statistics.mean(bar),3)
    except:
        avg = na

    TextSurf, TextRect = text_objects("all words median time (sec):  {}".format(avg), font, color=yellow)
    TextRect.top = int (5* spacing)
    TextRect.left = col5 + (spacing * 3)
    gameDisplay.blit(TextSurf, TextRect)

    lastTop = int(10 + ((2 + i) * spacing_size))
    return lastTop


skip_intro = False
from sftext import SFText

def refresh_session(time, words_per, db_size):

    time = str(time)
    gameDisplay.fill(black)
    pygame.display.update()

    msg = "Time in minutes (up/down keys):   {}".format(time)
    display_quit(and_report = True)
    starting_top = int(centerheight - (spacing * 3))

    TextSurf, TextRect = text_objects(msg, CURRENT_FONT)
    TextRect.top = starting_top
    TextRect.left = spacing
    gameDisplay.blit(TextSurf, TextRect)
    clock.tick(20)
    answer = 90

    msg = "Words Per Session (left/right keys): {}".format(words_per)
    TextSurf, TextRect = text_objects(msg, CURRENT_FONT)
    TextRect.left = spacing
    TextRect.top = int(starting_top + (1 * spacing))
    gameDisplay.blit(TextSurf, TextRect)

    starting_top += spacing
    lenny = len(all_map)

    msg = "Entries found in database :  {}".format(lenny)
    TextSurf, TextRect = text_objects(msg, CURRENT_FONT)
    TextRect.left = spacing
    TextRect.top = int(starting_top + (4 * spacing))
    gameDisplay.blit(TextSurf, TextRect)

    last_modified = str(datetime.fromtimestamp(os.path.getmtime("db.txt")).strftime('%Y-%m-%d %H:%M:%S'))
    msg = "Database updated :  {}".format(last_modified)
    TextSurf, TextRect = text_objects(msg, CURRENT_FONT)
    TextRect.left = spacing
    TextRect.top = int(starting_top + (2 * spacing))
    gameDisplay.blit(TextSurf, TextRect)

    msg = "Words Correct So Far:  {}".format(progress)
    TextSurf, TextRect = text_objects(msg, CURRENT_FONT)
    TextRect.left = spacing
    TextRect.top = int(starting_top + (3 * spacing))
    gameDisplay.blit(TextSurf, TextRect)

    msg = "Mastery:  {}%".format(round((mastery/lenny) * 100,2))
    TextSurf, TextRect = text_objects(msg, CURRENT_FONT)
    TextRect.left = spacing
    TextRect.top = int(starting_top + (5 * spacing))
    gameDisplay.blit(TextSurf, TextRect)

    bar = list()
    for aword, answers in word_elapsed_time.items():
        bar.append(statistics.mean(answers))
    try:
        avg = round(statistics.mean(bar),3)
    except:
        avg = na

    TextSurf, TextRect = text_objects("Avg time per word:  {} secs".format(avg), CURRENT_FONT)
    TextRect.left = spacing
    TextRect.top = int(starting_top + (6 * spacing))
    gameDisplay.blit(TextSurf, TextRect)



def get_session_time():
    global skip_intro
    global use_all
    global words_per_session
    global seen_before_repeat
    words_per_session = 20

    db_size = len(all_map)

    time = 5
    words_per = "all" if use_all else words_per_session

    refresh_session(time, words_per, db_size)
    pygame.display.update()

    refresh_vec = [
        pygame.K_DOWN, 
        pygame.K_UP, 
        pygame.K_LEFT, 
        pygame.K_RIGHT ]

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if not use_all:
                        get_loaded()
                        seen_before_repeat = min((len(keys), seen_before_repeat))
                    return time

                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_q:
                        pygame.event.clear()
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_r:
                        show_report()
                        pygame.quit()
                        quit()

                if event.key == pygame.K_LEFT and words_per_session > lenchoices:
                    use_all = False
                    words_per_session = words_per_session - 1

                if event.key == pygame.K_RIGHT:
                    if words_per_session == db_size:
                        use_all = True
                    else:
                        words_per_session = words_per_session + 1

                if event.key == pygame.K_UP:
                    time = time + 1

                if event.key == pygame.K_DOWN and time > 1:
                    time = time - 1

                if event.key == pygame.K_s:
                    skip_intro = True
                    return time

                words_per = "all" if use_all else words_per_session

                if event.key in refresh_vec:
                    refresh_session(time, words_per, db_size)
#                    gameDisplay.fill(black)
#                    display_quit(and_report = True)
#                    TextSurf, TextRect = text_objects(msg.format(time), CURRENT_FONT)
#                    TextRect.center = (int(display_width/2),int(display_height/2))
#                    gameDisplay.blit(TextSurf, TextRect)

                    pygame.display.update()

        clock.tick(60)


def game_loop():
    global CURRENT_FONT
    global show_answer
    global initial_time

    if not skip_intro:
        introduction()
    initial_time = time.time()

    pygame.event.clear()
    setAnswerQuestion()

    gameDisplay.fill(black)
    show_question_answers()
    display_quit()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_q:
                        pygame.event.clear()
                        pygame.quit()
                        quit()

                    if event.key == pygame.K_a:
                        show_answer = not show_answer

                    if event.key == pygame.K_d:

                        try:
                            available_fonts.remove(cfont_name)
                            pickle.dump(available_fonts, open(available_fonts_path, "wb"))
                        except:
                            pass

                else :

                    if show_answer:
                        show_answer = False

                        setAnswerQuestion()
                        gameDisplay.fill(black)
                        show_question_answers()
                        display_quit()

                    else:

                        try:
                            choice = str(event.unicode)
                            if not choice:
                                continue

                            idx = choices.index(choice)
                            answer = answer_choices[idx]
                            isCorrect(answer)

                            gameDisplay.fill(black)

                            if wrong_mode:
                                show_try_again()

                            show_question_answers()
                            display_quit()

                        except Exception as e:
                            pass

#        clock.tick(20)

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



##################################################################
# wrong stuff


def calc_wrong_ranges():
    wrong_sort = SortedSet()
    running_total = 0
    for dict_answer, the_set in wrong_dict_time.items():

        if dict_answer not in keys:
            continue

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

def get_a_word_answer():
    retword =  load_a_really_good_word()
    while not use_all and retword not in keys:
        retword =  load_a_really_good_word()
    return retword, load_map.get(retword)

def setAnswerQuestion():
    global CUR_WORD
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
    global session_saved
    global did_answer_a_question

    elapsed_time = round((time.time() - initial_time)) / 60 
    if elapsed_time > time_allotted:
        done = True
        return

    if start_time and CUR_WORD:
        elapsed_time = round(time.time() - start_time)

        if elapsed_time == 0:
            elapsed_time = 1

        times.append(elapsed_time)
        word_elapsed_time[CUR_WORD].append(elapsed_time)
        did_answer_a_question = True

        if wrong_count:
            report += " elapsed time : {}\n".format(elapsed_time)
            wrong_dict_time[CUR_WORD].append(elapsed_time)

        elif wrong_count == 0:

            if session_saved.count(CUR_WORD) <= 2:
                session_saved.append(CUR_WORD)

                if wrong_dict_time.get(CUR_WORD):
                    new_times = wrong_dict_time.get(CUR_WORD, list())[1:]
                    if new_times:
                        wrong_dict_time[CUR_WORD] = new_times
                    else:
                        del(wrong_dict_time[CUR_WORD])

                if wrong_dict_answers.get(CUR_WORD):
                    answers = wrong_dict_answers.get(CUR_WORD, list())
                    answers.pop()

                    if len(wrong_dict_answers.get(CUR_WORD)) == 0:
                        del(wrong_dict_answers[CUR_WORD])
                    else:
                        wrong_dict_answers[CUR_WORD] = answers

    start_time = time.time()

    CURRENT_FONT = update_font()

    wrong_mode = False
    wrong_count = 0

    # why are keys not matching load_map
    problem()

    CUR_WORD, CANSWERS = get_a_word_answer()


    len_seen = len(times)
    if len_seen > 0 and len_seen % 9 == 0:
        setup_ranges()

    while (len(setAnswerQuestion.seen_today) < seen_before_repeat and CUR_WORD in setAnswerQuestion.seen_today):
        CUR_WORD, CANSWERS = get_a_word_answer()
    else:
        setAnswerQuestion.seen_today.add(CUR_WORD)

    if not CANSWERS:
        print("no CANSWERS: {}".format( CANSWERS))
        if CUR_WORD in load_map:
            print("load_map: {}".format( load_map))
            print("could not find: {}".format( CUR_WORD))
        exit()
    playSound(CUR_WORD)

    report += "\n({}-{})".format(CUR_WORD, correct_before.get(CUR_WORD, ""))

    needed_answers = len(choices)
    answer_choices = set() 
    try:
        answer_choices.add(random.choice(CANSWERS))
    except:
        pass

    prev_wrong = wrong_dict_answers.get(CUR_WORD, list())

    if prev_wrong:
        prev_wrong = list(prev_wrong)
        random.shuffle(prev_wrong)
        for answer in prev_wrong[:4]:
            answer_choices.add(answer)

    while len(answer_choices) != needed_answers:
        answer_choices.add(random.choice(answer_db))

    answer_choices = list(answer_choices)
    random.shuffle(answer_choices)
setAnswerQuestion.seen_today = set()

def load_wrong():
    global wrong_dict_answers
    global correct_before
    global wrong_dict_time
    global word_elapsed_time

    try:
        wrong_dict_time, wrong_dict_answers, correct_before, word_elapsed_time = pickle.load(open(wrong_data_path, "rb"))
        print("word_elapsed_time : {}".format( word_elapsed_time ))
    except Exception as e:
        try:
            wrong_dict_time, wrong_dict_answers, correct_before = pickle.load(open(wrong_data_path, "rb"))
            word_elapsed_time = defaultdict(list)
        except:
            wrong_dict_time = defaultdict(list)
            wrong_dict_answers = defaultdict(set)
            correct_before = defaultdict(str)
            word_elapsed_time = defaultdict(list)
    
    if not loading_wrong:
        wrong_dict_time = defaultdict(list)
        wrong_dict_answers = defaultdict(set)
        correct_before = defaultdict(str)
        word_elapsed_time = defaultdict(list)

available_fonts_path = "available_fonts.pkl"
used_resource_font = False
if __name__ == '__main__':
    try:
        gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF)
        clock = pygame.time.Clock()
        try:
            available_fonts = pickle.load(open(available_fonts_path, "rb"))
        except:
            available_fonts = list()
            pass
        
        if len(available_fonts) < 5:
            used_resource_font = True
            pat = os.path.join(os.getcwd(), "resources")
            pat = os.path.join(pat, "fonts")
            pat = os.path.join(pat, "*.ttf")
            available_fonts = glob.glob(pat)
    
        CURRENT_FONT = update_font()
    
        load_wrong()
        get_loaded()
    
        problem()
        try:
            time_allotted = get_session_time()
            game_loop()
            pygame.quit()
            quit()
        except Exception as e:
            traceback.print_exc() 
            print (e)

    except Exception as e:
        traceback.print_exc()
        print (str(e))

