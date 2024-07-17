import pygame
from pygame.math import Vector2
from pygame.display import get_surface
from add.Path import resource_path
from os.path import join
from random import choice
from text.Button import Button, ButtonsHandler

class Exit:
    def __init__(self, text : dict):
        self.myfont = pygame.font.SysFont("Montserrat", 30) # Arial Narrow, Montserrat
        self.default_fonts = ["Romashulka.ttf", "moonlight.ttf", "graf.ttf" ]
        self.fonts = list(self.default_fonts)
        self.myBiggerFont = self.get_BiggerFont()
        self.screen = get_surface()
        self.center = Vector2(self.screen.get_rect().center)

        self.text = text
        # print(self.text.keys())
        self.labels = {}
        self.buttons = {}
        self.buttons_handler = None
        # self.active_color = "Red"
        # self.key_pressed = False
        # self.b_iter = None

        self.create()

    def get_BiggerFont(self):
        if not self.fonts:
            self.fonts = list(self.default_fonts)

        font_name = choice(self.fonts)
        self.fonts.remove(font_name)
        font_url = resource_path(join('fonts', font_name))
        
        return pygame.font.Font(font_url, 60)

    def change_BiggerFont(self):
        self.myBiggerFont = self.get_BiggerFont()
        self.create()
    
    def createButtons(self, buttons : list, pos : Vector2):
        # pos = pos
        for key in buttons:
            self.buttons[key] = Button(self.text[key], self.myfont, pos)
            pos.y = self.buttons[key].get_bottom() + 30

    def createLabels(self, labels : list, pos : Vector2):
        # pos = pos
        for key in labels:
            self.labels[key] = Button(self.text[key], self.myBiggerFont, pos)
            pos.y = self.labels[key].get_bottom() + 30

    def create(self):
        # print("createExitRects call")
        # self.myBiggerFont = self.get_BiggerFont()
        # ----------------------------------------------------------
        # position = Vector2(self.center.x, self.center.y - 85)
        # self.game_over = Button(self.text['over_1'], self.myBiggerFont, position)
        # position.y = self.game_over.get_bottom() + 30
        # self.game_over_2 = Button(self.text['over_2'], self.myBiggerFont, position)
        # position.y = self.game_over_2.get_bottom() + 50
        # self.restart_text = Button(self.text['restart_button'], self.myfont, position)
        # position.y = self.restart_text.get_bottom() + 30
        # self.exit_text = Button(self.text['exit_button'], self.myfont, position)
        # ----------------------------------------------------------
        position = Vector2(self.center.x, self.center.y - 85)
        labels = ['over_1', 'over_2']
        self.createLabels(labels, position)

        last_label = next(reversed(self.labels)) # reversed iterator
        # print('last_label', last_label)
        position.y = self.labels[last_label].get_bottom() + 50
        buttons = ['restart_button', 'exit_button']
        self.createButtons(buttons, position)
        
        # create iterator
        self.buttons_handler = ButtonsHandler(self.buttons)

    def update(self):
        key = self.buttons_handler.update_mouse()
        if key:
            return key
        
        key = self.buttons_handler.update_keys()
        if key:
            return key

    def display(self):
        for label in self.labels.values():
            label.draw(self.screen)
        for button in self.buttons.values():
            button.draw(self.screen)
