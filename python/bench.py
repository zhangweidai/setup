# time python bench.py
# time { python bench.py }
def test():
    """Stupid test function"""
    lst = []
    for i in range(100):
        lst.append(i)

if __name__ == '__main__':
    print (dir(__main__))
#    import timeit
#    print(timeit.timeit("test()", setup="from __main__ import test"))
