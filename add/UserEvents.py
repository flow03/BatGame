import pygame

class UserEvents:
    def __init__(self):
        self.BAT_TIMER = pygame.USEREVENT + 1
        self.BULLET_DROP_TIMER = pygame.USEREVENT + 2
        self.FOOD_DROP_TIMER = pygame.USEREVENT + 3
        self.BAT_SP_TIMER = pygame.USEREVENT + 4

        self.isEvents = True
        # self.start_timer()
        # self.stop_timer()

    def start_timer(self):
        pygame.time.set_timer(self.BAT_TIMER, 3000)
        pygame.time.set_timer(self.BULLET_DROP_TIMER, 2000)
        pygame.time.set_timer(self.FOOD_DROP_TIMER, 2500)
        # pygame.time.set_timer(self.BAT_SP_TIMER, 4000)
        self.isEvents = True

    def stop_timer(self):
        pygame.time.set_timer(self.BAT_TIMER, 0)
        pygame.time.set_timer(self.BULLET_DROP_TIMER, 0)
        pygame.time.set_timer(self.FOOD_DROP_TIMER, 0)
        pygame.time.set_timer(self.BAT_SP_TIMER, 0)
        self.isEvents = False 

    def switch(self):
        if self.isEvents:
            self.stop_timer()
        else:
            self.start_timer()

    # reverse to switch
    def start(self):
        if self.isEvents:
            self.start_timer()
        else:
            self.stop_timer()
