import pygame

class Clock:
    # set delay
    def __init__(self, delay : int):
        self.delay = delay
        self.nextFrame = None
        # self.nextFrame = self.clock() + self.delay
        # self.start()

    def clock(self):
        return pygame.time.get_ticks()

    # check nextFrame and set new nextFrame if True
    def isNextFrame(self):
        if self.nextFrame:
            if (self.clock() >= self.nextFrame):
                self.nextFrame += self.delay
                return True
        
        return False

    # set nextFrame
    def start(self):
        if not self.nextFrame:
            self.nextFrame = self.clock() + self.delay

    # check nextFrame and disable nextFrame if True
    def end(self):
        if self.nextFrame:
            if self.clock() >= self.nextFrame:
                self.nextFrame = None
                return True

        return False
