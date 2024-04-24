import pygame
from add.Path import resource_path
from interface.Text import Text
from loot.Drops import Drops
from actors.Groups import Groups
from add.UserEvents import UserEvents
from actors.Player import Player
from actors.Dummy import DummyCreator

class Game():
    def __init__(self):
        pygame.init()
        self.FPS = pygame.time.Clock()
        self.screen_init()

        self.text = Text(self.screen)
        self.blit_loading()

        self.drops = Drops()
        self.groups = Groups()
        self.Events = UserEvents()

        self.player = Player(self.screen.get_size()//2, self.drops)
        self.dummies = DummyCreator(self.groups)

    def screen_init(self):
        WIDTH = 1200
        HEIGHT = 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bat Game")
        icon = pygame.image.load(resource_path('img/fangs.ico')).convert_alpha()
        pygame.display.set_icon(icon)
        self.bg_init(WIDTH, HEIGHT)

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