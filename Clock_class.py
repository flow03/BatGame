import pygame

class Clock:
    def __init__(self, delay : int):
        self.delay = delay
        # self.nextFrame = self.clock() + self.delay
        self.set_nextFrame()

    def clock(self):
        return pygame.time.get_ticks()

    def isNextFrame(self):
        if (self.clock() >= self.nextFrame):
            self.nextFrame += self.delay
            return True
        else:
            return False

    def set_nextFrame(self):
        self.nextFrame = self.clock() + self.delay
