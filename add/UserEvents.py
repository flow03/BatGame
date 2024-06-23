import pygame
from actors.Bat import BatMoving, BatSpecial
from actors.Dance_Girl import Dance_Girl

class UserEvents:
    def __init__(self, game):
        self.game = game
        self.isEvents = True
        self.isTenBats = False

        self.init()
        self.start()

    def init(self):
        self.BAT_TIMER = pygame.USEREVENT + 1
        self.BULLET_DROP_TIMER = pygame.USEREVENT + 2
        self.FOOD_DROP_TIMER = pygame.USEREVENT + 3
        self.BAT_SP_TIMER = pygame.USEREVENT + 4
        self.MUSHROOMS = pygame.USEREVENT + 5
        self.TEN_BATS = pygame.USEREVENT + 6
        # self.BAT_KILLED = pygame.USEREVENT + 7

    def update(self):
        drops = self.game.drops
        groups = self.game.groups
        # player = self.game.player

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.active = False
                # pygame.quit()
            # if not Girl:
            if event.type == self.BAT_TIMER:
                groups.add_bat(BatMoving(self.game))
            if event.type == self.BAT_SP_TIMER:
                groups.add_bat(BatSpecial(self.game))
            if event.type == self.BULLET_DROP_TIMER:
                drops.create_bulletDrop()
            if event.type == self.FOOD_DROP_TIMER:
                drops.create_foodDrop()
            if event.type == self.MUSHROOMS:
                drops.create_Mushrooms()
            if event.type == self.TEN_BATS:
                for i in range(10):
                    groups.add_bat(BatSpecial(self.game))
            # if event.type == self.BAT_KILLED:
            #     killedBats += 1

            self.key_pressed(event)

    def key_pressed(self, event):
        drops = self.game.drops
        groups = self.game.groups
        player = self.game.player
        # Створення кулі з позиції гравця до позиції миші
        if player.gameplay and event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot(self.game.groups.bullets, pygame.mouse.get_pos())
        if player.gameplay and event.type == pygame.KEYDOWN:
            # Створення кулі, яка летітиме у напрямку player.direction
            # if event.key == pygame.K_e or event.key == pygame.K_q:
            #     player.shoot(groups.bullets)
            if event.key == pygame.K_TAB:
                self.game.switch_text()
            if event.key == pygame.K_t:
                self.switch()
            if event.key == pygame.K_p:
                self.game.dummies.switchDummies()
            if event.key == pygame.K_1:
                player.add_effect("poison")
            if event.key == pygame.K_2:
                player.add_effect("onepunch")
            if event.key == pygame.K_3 or event.key == pygame.K_LSHIFT:
                player.add_effect("speed")
            if event.key == pygame.K_4:
                player.add_effect("ironskin")
            if event.key == pygame.K_5:
                player.add_effect("harmless")
            if event.key == pygame.K_6:
                player.add_effect("stand")
            if event.key == pygame.K_7 or event.key == pygame.K_x:
                player.add_effect("bullets")
            if event.key == pygame.K_m: # unlimited recreates
                if not groups.actors.get("girl"):
                    groups.add_actor("girl", Dance_Girl(self.game))
            if event.key == pygame.K_c:
                pygame.event.post(pygame.event.Event(self.BAT_SP_TIMER))
            if event.key == pygame.K_z:
                drops.create_foodDrop()
            if event.key == pygame.K_LEFTBRACKET or event.key == pygame.K_BACKQUOTE: # tilda
                drops.create_RedMushroom()
            if event.key == pygame.K_RIGHTBRACKET:
                drops.create_BlueMushroom()
            if event.key == pygame.K_j:
                player.get_joke()
            # if event.key == pygame.K_h:
            #     groups.actors_heal(5)
            #     player.set_heal(5)
            # if event.key == pygame.K_k:
            #     groups.actors_damage(5)
            #     player.set_damage(5)

        # працює незалежно від player.gameplay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game.restart()
            # if event.key == pygame.K_g:
            #     gc.collect()
            #     print(gc.get_stats())
                
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
