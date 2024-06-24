import pygame
from add.Path import resource_path
from text.Text import Text
from loot.Drops import Drops
from actors.Groups import Groups
from add.UserEvents import UserEvents
from actors.Player import Player
from actors.Dummy import DummyCreator
from pygame.math import Vector2
from text.Jokes import Jokes

class Game():
    def __init__(self):
        pygame.init()
        self.FPS = pygame.time.Clock()
        self.screen_init()
        self.screen_center = Vector2(self.screen.get_size())//2

        self.text = Text(self)
        # self.blit_loading()
        self.jokes = Jokes()

        self.drops = Drops()
        self.groups = Groups()
        self.Events = UserEvents(self)

        self.player = Player(self.screen_center, self.drops, self.jokes)
        self.dummies = DummyCreator(self.groups)

        self.displayText = False
        self.active = True

    def screen_init(self):
        WIDTH = 1200
        HEIGHT = 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bat Game")
        icon = pygame.image.load(resource_path('img/fangs.ico')).convert_alpha()
        pygame.display.set_icon(icon)
        self.bg_init(WIDTH, HEIGHT)
        # self.screen_center = Vector2(WIDTH//2, HEIGHT//2)

    def bg_init(self, WIDTH, HEIGHT):
        bg = pygame.image.load(resource_path('img/bg/Work-2.jpg')).convert()
        bg_width, bg_height = bg.get_size()
        scale_factor = max(WIDTH / bg_width, HEIGHT / bg_height)
        scaled_bg_width = int(bg_width * scale_factor)
        scaled_bg_height = int(bg_height * scale_factor)
        self.background = pygame.transform.scale(bg, (scaled_bg_width, scaled_bg_height))
        bg_x = (WIDTH - scaled_bg_width) // 2
        bg_y = (HEIGHT - scaled_bg_height) // 2
        self.bg_pos = (bg_x, bg_y)

    def blit_loading(self):
        self.screen.blit(self.background, self.bg_pos)
        self.text.blit_loading_text(self.screen)
        pygame.display.update()

    def update_objects(self):
        # bat_list.update()
        self.player.update()
        # bullets.update()
        self.drops.update()
        self.groups.update()
        # Events.update()

    def draw_objects(self):
        self.drops.draw()
        self.groups.draw()
        self.player.draw(self.screen) 

    def restart(self):
        self.player.init()
        self.groups.clear()
        self.drops.clear()
        # jump.is_jump = False
        self.Events.start()
        self.dummies.create() # after groups.clear
        self.text.exit.change_BiggerFont()
        # isTenBats = False

    def switch_text(self):
        if not self.displayText:
            self.displayText = True
        else:
            self.displayText = False

        if self.displayText:
            self.groups.drawer.rect()
            self.drops.drawer.rect()
        else:
            self.groups.drawer.common()
            self.drops.drawer.common()

    # Main loop    
    def run(self):
        while self.active:
            self.FPS.tick(60)

            self.screen.blit(self.background, self.bg_pos)

            if self.player.gameplay:
                
                self.player.input()

                self.update_objects()
                self.draw_objects()
                
                # self.Events.update()
                # self.Events.restart_pressed()
                if self.displayText:            
                    self.text.display()
            else:
                self.text.exit.blitExitButtons()

                if pygame.mouse.get_pressed()[0]:   # left mouse key
                    mouse_pos = pygame.mouse.get_pos()
                    if self.text.exit.restart_text.collide(mouse_pos):
                        self.restart()
                    elif self.text.exit.exit_text.collide(mouse_pos):
                        self.active = False
            
            pygame.display.update()

            self.Events.update()
            # self.Events.restart_pressed()

        pygame.quit()
