import time


class Bucket(object):

    # constructor to set self.value and self.refill_time
    def __init__(self, max_amount, refill_time):
        self.max_amount = max_amount
        self.refill_time = refill_time
        self.reset()

    # setClick() accepts and sets new max_amount
    def setClick(self,maxClick):
        self.max_amount = maxClick

    # setRefresh() accepts and sets new refill_time
    def setRefresh(self,refreshLim):
        self.refill_time = refreshLim

    # getClick() returns self.max_amount
    def getClick(self,):
        return self.max_amount

    # getRefresh() returns self.refill_time
    def getRefresh(self,):
        return self.refill_time

    # reset() refreshes values of self.value , self.last_update
    def reset(self):
        self.value = self.max_amount
        self.last_update = time.time()

    # get() returns clicks left and time left after which it will be refreshed
    # returns pair (clicks left , time left)
    def get(self):
        return (self.value, self.refill_time - int(time.time() - self.last_update))

    # reduce() reduces value of self.value by 1(default).
    # If self.value turns out to be less than 0, reduce returns false otherwise
    # true
    def reduce(self, tokens = 1):
        if int(time.time() - self.last_update) >= self.refill_time:
            self.reset()
        if tokens > self.value:
            return False
        self.value -= tokens
        return True

# ignore
def Main():
    b = Bucket(10, 60)
    print (b.get())
    print (b.reduce(1))

    print (b.get())
    print (b.reduce(1))

    print (b.get()[0])
    print (b.reduce(1))

    print (b.get()[1])
    print (b.reduce(1))

if __name__ == '__main__':
        Main()
# ignore
