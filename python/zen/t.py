import timeit
import z

def Test1():
    global i
    i += 1

i = 0
bar = -1
def Test2():
    global i, bar
    if i != bar:
        i += 1

def Test3():
    global i
    try:
        i += 1
    except:
        pass


if __name__ == '__main__':
    methods = dir()
    times = list()
    names = list()
    for method in methods:
        if not "Test" in method:
            continue

        print (method)
        names.append(method)
        answer = timeit.timeit("{}()".format(method), 
                    setup="from __main__ import {}".format(method),
                    number=100000000)
        i = 0
        times.append(answer)
        print (round(answer,4))

    if len(times) > 1:
        mint = min(times)
        maxt = max(times)
        idx = times.index(mint)
        from termcolor import colored
        msg = "\n{} is {:.2%} faster".format(names[idx], (maxt/mint)-1)
        print (colored(msg, "green"))
