import collections
import statistics

class WindowQueue(object):
    
    def __init__(self, maxsize=15, needMin=False, needMax=False):
        self.maxsize = maxsize
        self.needMin = needMin
        self.needMax = needMax

        self.clear()
    
    def clear(self):
        self.main = collections.deque()
        if self.needMin:
            self.mindeque = collections.deque()
        if self.needMax:
            self.maxdeque = collections.deque()

    def get_minimum(self):
        return self.mindeque[0]
    
    def full(self):
        return len(self.main) == self.maxsize

    def get_size(self):
        return len(self.main)

    def get_maximum(self):
        return self.maxdeque[0]

    def score(self, more_last = True):
        if not more_last:
            return statistics.median(self.main)

        last_part = round(self.maxsize/4)
        try:
            rm1 = statistics.median(self.main + self.main[-1*last_part:])
        except:
            rm1 = statistics.median(self.main)
        return round(rm1,3), round(min(self.main),3), round(self.main[-1],3)
    
    def add_tail(self, val):
        if self.needMin:
            while len(self.mindeque) > 0 and val < self.mindeque[-1]:
                self.mindeque.pop()
            self.mindeque.append(val)
        
        if self.needMax:
            while len(self.maxdeque) > 0 and val > self.maxdeque[-1]:
                self.maxdeque.pop()
            self.maxdeque.append(val)

        self.main.append(val)
        if len(self.main) > self.maxsize:
            self._remove_head()
    
    def get(self, idx=0):
        return self.main[idx]

    def _remove_head(self):
        val = self.main.popleft()

        if self.needMin:
            if val < self.mindeque[0]:
                raise ValueError("Wrong value")
            elif val == self.mindeque[0]:
                self.mindeque.popleft()
        
        if self.needMax:
            if val > self.maxdeque[0]:
                raise ValueError("Wrong value")
            elif val == self.maxdeque[0]:
                self.maxdeque.popleft()

