import pygame
from add.Path import resource_path_args
from text.Text import Text, DebugInfo, DebugDisplay
from loot.Drops import Drops
from actors.Groups import Groups
from Events import Events
from actors.Player import Player
from actors.Dummy import DummyCreator
from pygame.math import Vector2
from text.Jokes import JokesCreator
from text.Menu import MenuContex

class Game():
    def __init__(self):
        pygame.init()
        self.FPS = pygame.time.Clock()
        self.screen_init()
        self.screen_center = Vector2(self.screen.get_size())//2

        self.text = Text()
        self.info = DebugInfo(self, self.text)
        self.debug = DebugDisplay(self, self.info)
        # self.blit_loading()
        self.jokes = JokesCreator()

        self.drops = Drops()
        self.groups = Groups()
        self.events = Events(self)

        self.player = Player(self.screen_center, self)
        self.dummies = DummyCreator(self.groups)

        self.displayText = False
        self.active = True
        self.state = "menu"
        self.menu = MenuContex(self.text, self.jokes)
        # self.pause = Pause(self.text.text)

        self.killedBats = 0

    def game(self):
        return self.state == "game"

    def screen_init(self):
        WIDTH = 1200
        HEIGHT = 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bat Game")
        icon = pygame.image.load(resource_path_args('img','fangs.ico')).convert_alpha()
        pygame.display.set_icon(icon)
        self.bg_init(WIDTH, HEIGHT)
        # self.screen_center = Vector2(WIDTH//2, HEIGHT//2)

    def bg_init(self, WIDTH, HEIGHT):
        bg = pygame.image.load(resource_path_args('img','bg','Work-2.jpg')).convert()
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
        self.info.blit_loading_text(self.screen)
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
        self.events.start()
        # self.dummies.is_dummies = False
        self.dummies.create() # after groups.clear
        self.menu.change_BiggerFont()
        # isTenBats = False
        self.state = "game"
        self.killedBats = 0

    # Main loop    
    def run(self):
        # self.dummies.is_dummies = True
        # self.dummies.create()

        while self.active:
            self.FPS.tick(60)

            self.screen.blit(self.background, self.bg_pos)

            if self.state == "game": # self.game()
                
                self.player.input()

                self.update_objects()
                self.draw_objects()
                
                # self.events.update()
                # self.events.restart_pressed()
                self.debug.display()

            elif self.state == "menu":
                self.menu.update()
                self.menu.display()

            # elif self.state == "pause":
            #     # self.events.stop()
            #     self.pause.update()
            #     self.pause.display()

            pygame.display.update() 

            # події продовжуюють оновлюватись навіть після виходу у меню програми
            self.events.update()
            # self.events.restart_pressed()

        pygame.quit()

    # призначений лише для зміни пунктів меню
    def menu_change(self, key):
        self.menu.change(key)
        self.state = "menu"
        self.events.stop()

    # призначений лише для реагування на клавішу Назад
    # def menu_back(self):
    #     state = self.menu.back()
    #     # print("back state", state)
    #     if state == "game":
    #         self.state = "game"
    #         self.events.start()
    #     elif state == "back":
    #         self.menu_change("back")

    def menu_back(self):
        if self.state == "menu":
            back_state = self.menu.back()

            if back_state == "game":
                self.state = "game"
                self.events.start()
