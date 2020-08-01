import argparse
import z
import __main__
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--mode', default=None)
parser.add_argument('--debug', nargs='?', const=True, default=False)
parser.add_argument('--live', nargs='?', const=True, default=False)
parser.add_argument('--flive', nargs='?', const=True, default=False)
parser.add_argument('--noupdate', nargs='?', const=True, default=False)
parser.add_argument('--full', nargs='?', const=True, default=False)
parser.add_argument('--override', default=None)

parser.add_argument('--quick', nargs='?', const=True, default=False)
parser.add_argument('--drop', default=None)
parser.add_argument('--nc', nargs='?', const=True, default=False)
parser.add_argument('--first', nargs='?', const=True, default=False)
parser.add_argument('--second', nargs='?', const=True, default=False)
parser.add_argument('--bta', nargs='?', const=True, default=False)
parser.add_argument('--section', default=None)
parser.add_argument('stocks', type=str, nargs='?', default = [])
args = parser.parse_args()

#if __main__.full == True:
#    args.args.full = True

print("args : {}".format( args ))

try:
    if __main__.stocks:
        pass
except Exception as e:
    print("args : {}".format( args ))
    __main__.stocks = []


if args.override:
    z.getp.quick_list = True
    z.getp.override = args.override
    print("override : {}".format( z.getp.override ))

if args.live:
    z.online.online = True

def restart_program():
    import os
    import sys
    try:
        p = Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except:
        pass
    python = sys.executable
    os.execl(python, python, *sys.argv)


z.getp.quick_list = not args.full

try:
    z.getp.quick_list = not __main__.full
except Exception as e :
    pass

__main__.debug = None if not args.stocks else args.stocks.upper()
if "," in args.stocks:
    __main__.stocks = args.stocks.upper().split(",")
else:
    __main__.stocks = [__main__.debug.upper()] if __main__.debug else z.getp("listofstocks")

if args.quick == True:
    args.stocks = "savePs"

came_from_list = False
came_from_dict = dict()
if "," not in args.stocks:
    try:
        arg_is_pkl = z.getp(args.stocks, retfile=True)
        if arg_is_pkl:
            __main__.debug = None 
            __main__.stocks = list()
            temp = z.getp(args.stocks)
            temp_type = type(temp)
            came_from_list = (temp_type is list)
            if temp_type is defaultdict:
                temp = temp.keys()

            for astock in temp:
                if type(astock) is str:
                    __main__.stocks = temp
                    break
                else:
                    __main__.stocks.append(astock[1])
                    came_from_dict[astock[1]] = astock[0]

            if args.first: 
                num = len(__main__.stocks)
                __main__.stocks = __main__.stocks[:int(num/2)]
            elif args.second: 
                num = len(__main__.stocks)
                __main__.stocks = __main__.stocks[int(num/2):]

    except:
        pass

__main__.debug = args.debug
__main__.dates = z.getp("dates")

if len(__main__.stocks) >= 5:
    z.gonna_need_alot = True
