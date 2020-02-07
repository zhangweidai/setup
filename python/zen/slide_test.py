import random, unittest
import sliding


class SlidingWindowMinMaxTest(unittest.TestCase):
    
    def test_randomly(self):
        trials = 3000
        for _ in range(trials):
            
            arraylen = random.randrange(300)
            array = [random.randrange(100) for _ in range(arraylen)]
            window = random.randrange(1, 31)
            maximize = random.randrange(2) != 0
            
            expect = _compute_naive(array, window, maximize)
            actual = sliding.compute(array, window, maximize)
            self.assertEqual(expect, actual)
    
    
    def test2_incremental(self):
        swm = sliding.WindowQueue(10)
        for val in range(30):
            swm.add_tail(val)
            items = swm.main
            print("items : {}".format( items ))
            bar = swm.get_minimum()
            print("bar : {}".format( bar ))
            bar = swm.get_maximum()
            print("bar : {}".format( bar ))

def _compute_naive(array, window, maximize):
    if window <= 0:
        raise ValueError()
    func = max if maximize else min
    return [func(array[i : i + window]) for i in range(len(array) - window + 1)]


if __name__ == "__main__":
    unittest.main()

