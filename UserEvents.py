import pygame

class UserEvents:
    def __init__(self):
        self.BAT_TIMER = pygame.USEREVENT + 1
        self.BULLET_DROP_TIMER = pygame.USEREVENT + 2
        self.FOOD_DROP_TIMER = pygame.USEREVENT + 3
        self.BAT_SP_TIMER = pygame.USEREVENT + 4

        self.isEvents = True

        self.set_timer()
sad
        pygame.time.set_timer(self.BAT_TIMER, 3000)
        pygame.time.set_timer(self.BULLET_DROP_TIMER, 3200)
        pygame.time.set_timer(self.FOOD_DROP_TIMER, 3500)
        pygame.time.set_timer(self.BAT_SP_TIMER, 6000)

    def stop_timer(self):
        pygame.time.set_timer(self.BAT_TIMER, 0)
        pygame.time.set_timer(self.BULLET_DROP_TIMER, 0)
        pygame.time.set_timer(self.FOOD_DROP_TIMER, 0)
        pygame.time.set_timer(self.BAT_SP_TIMER, 0) 

    def switch(self):
        if self.isEvents:
            self.stop_timer()
            self.isEvents = False
        else:
            self.set_timer()
            self.isEvents = True
