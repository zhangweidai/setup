import timeit
import z

def Test1():
    print ("hello")

def Test2():
    z.getp("sorteddict")
    z.getp("prices")

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
                    number=30)
        times.append(answer)
        print (round(answer,4))

    if len(times) > 1:
        mint = min(times)
        maxt = max(times)
        idx = times.index(mint)
        from termcolor import colored
        msg = "\n{} is {:.2%} faster".format(names[idx], (maxt/mint)-1)
        print (colored(msg, "green"))
