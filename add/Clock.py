from pygame.time import get_ticks

class Clock:
    # set delay
    def __init__(self, delay : int):
        self.delay = delay
        self.nextFrame = None
        # self.remain = None  # remaining time

    def clock(self):
        return get_ticks()

    # check nextFrame and set new nextFrame based on delay if True
    def next(self):
        if self.nextFrame and self.clock() >= self.nextFrame:
            self.nextFrame += self.delay
            return True
        
        # return False
    
    def active(self):
        if self.nextFrame and self.clock() < self.nextFrame:
            return True

    # reverse to active
    def end(self):
        if self.nextFrame and self.clock() >= self.nextFrame:
            return True

    # set nextFrame
    def start(self):
        if not self.nextFrame:
            self.restart()

    def restart(self):
        self.nextFrame = self.clock() + self.delay
    
    def time(self):
        # time = None
        if self.nextFrame:
            return self.nextFrame - self.clock()
        # return time

    # def pause(self):
    #     self.remain = self.nextFrame - self.clock()

    # def go(self):
    #     if self.remain:
    #         self.nextFrame = self.clock() + self.remain

