import pygame

class UserEvents:
    def __init__(self):
        self.BAT_TIMER = pygame.USEREVENT + 1
        self.BULLET_DROP_TIMER = pygame.USEREVENT + 2
        self.FOOD_DROP_TIMER = pygame.USEREVENT + 3
        self.BAT_SP_TIMER = pygame.USEREVENT + 4
        self.MUSHROOMS = pygame.USEREVENT + 5
        self.TEN_BATS = pygame.USEREVENT + 6
        # self.BAT_KILLED = pygame.USEREVENT + 7

        self.isEvents = True
        self.start()
        
        self.isTenBats = False

    def update(self):
        # if not self.isTenBats and player.killedBats >= 10:
        #     pygame.event.post(pygame.event.Event(self.TEN_BATS))
        #     self.isTenBats = True
        pass

    def start_timer(self):
        pygame.time.set_timer(self.BAT_TIMER, 3500)
        pygame.time.set_timer(self.BULLET_DROP_TIMER, 4000)
        pygame.time.set_timer(self.FOOD_DROP_TIMER, 5000)
        pygame.time.set_timer(self.BAT_SP_TIMER, 4000)
        # pygame.time.set_timer(self.MUSHROOMS, 50)
        self.isEvents = True

    def stop_timer(self):
        pygame.time.set_timer(self.BAT_TIMER, 0)
        pygame.time.set_timer(self.BULLET_DROP_TIMER, 0)
        pygame.time.set_timer(self.FOOD_DROP_TIMER, 0)
        pygame.time.set_timer(self.BAT_SP_TIMER, 0)
        # pygame.time.set_timer(self.MUSHROOMS, 0)
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
