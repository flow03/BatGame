import pygame
from pygame.math import Vector2
from pygame.display import get_surface
from add.Path import resource_path
from os.path import join
from random import choice
from text.Button import Button, ButtonsHandler

class BiggerFont:
    def __init__(self):
        self.myfont = pygame.font.SysFont("Montserrat", 30) # Arial Narrow, Montserrat
        self.myBiggerFont = None
        
        self.default_fonts = ["Romashulka.ttf", "moonlight.ttf", "graf.ttf" ]
        self.fonts = list(self.default_fonts)
        self.change_BiggerFont()

    def change_BiggerFont(self):
        if not self.fonts:
            self.fonts = list(self.default_fonts)

        font_name = choice(self.fonts)
        self.fonts.remove(font_name)
        font_url = resource_path(join('fonts', font_name))
        
        self.myBiggerFont = pygame.font.Font(font_url, 60)

class Menu:
    def __init__(self, text : dict, font : BiggerFont):
        # self.font = BiggerFont()
        self.font = font
        self.screen = get_surface()
        self.center = Vector2(self.screen.get_rect().center)

        self.text = text
        # print(self.text.keys())
        self.titles = {}
        self.labels = {}
        self.buttons = {}
        self.buttons_handler = None

        # self.create()
        self.TITLE_SPACING = 50
        self.SPACING = 30

    def createButtons(self, buttons : list, pos : Vector2):
        # pos = pos
        for key in buttons:
            self.buttons[key] = Button(self.text[key], self.font.myfont, pos)
            pos.y = self.buttons[key].get_bottom() + self.SPACING

    def createLabels(self, labels : list, pos : Vector2):
        # pos = pos
        for key in labels:
            self.labels[key] = Button(self.text[key], self.font.myfont, pos)
            pos.y = self.labels[key].get_bottom() + self.SPACING

    def createTitles(self, titles : list, pos : Vector2):
        # pos = pos
        for key in titles:
            self.titles[key] = Button(self.text[key], self.font.myBiggerFont, pos)
            pos.y = self.titles[key].get_bottom() + self.SPACING

    def create(self, titles : list, buttons : list, labels : list = None, position : Vector2 = None):
        if not position:
            position = Vector2(self.center.x, self.center.y - 85)
        # ----------------------------------------------------------------
        self.createTitles(titles, position)
        # TODO потенційна помилка, якщо self.titles пустий
        # last_title = next(reversed(self.titles)) # reversed iterator
        last_title = titles[-1]
        position.y = self.titles[last_title].get_bottom() + self.TITLE_SPACING
        # ----------------------------------------------------------------
        if labels:
            self.createLabels(labels, position)
            # last_label = next(reversed(self.labels)) # reversed iterator
            last_label = labels[-1]
            position.y = self.labels[last_label].get_bottom() + self.SPACING
        # ----------------------------------------------------------------
        self.createButtons(buttons, position)
        
        # create iterator
        self.buttons_handler = ButtonsHandler(self.buttons)

    def update(self):
        self.buttons_handler.update_mouse()
        self.buttons_handler.update_keys()

    def display(self):
        for title in self.titles.values():
            title.draw(self.screen)
        for label in self.labels.values():
            label.draw(self.screen)
        for button in self.buttons.values():
            button.draw(self.screen)

    def change_Font(self, ):
        # self.font.change_BiggerFont()
        self.create(list(self.titles.keys()), list(self.buttons.keys()))

    def back(self):
        return None
    
class Exit(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        titles = ['over_1', 'over_2']
        buttons = ['restart_button', 'exit_button']
        self.create(titles, buttons)

class Pause(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        titles = ['pause']
        buttons = ['continue', 'controls', 'restart_button', 'exit_button']
        self.create(titles, buttons)

    def back(self):
        return "game"

class Start(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        titles = ['start']
        buttons = ['new_game', 'controls', 'exit_button']
        self.create(titles, buttons)

class Controls(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        titles = ['controls']
        # self.titles = dict.fromkeys(titles)
        labels = [
        'moving',
        'fire',
        'effects',
        'speed_key',
        'b_speed_key',
        'food',
        'bat',
        'mushrooms',
        'dummies',
        'girl',
        'joke',
        'events',
        # 'restart',
        'help']
        buttons = ['back']
        # self.buttons = dict.fromkeys(buttons)
        self.SPACING = 15
        
        self.create(titles, buttons, labels, Vector2(self.center.x, 50))
        self.buttons['back'].shift((0, self.SPACING))

    def back(self):
        return "back"

    # def create(self):
    #     position = Vector2(self.center.x, 50)
    #     # ----------------------------------------------------------------
    #     self.createTitles(self.titles, position)
    #     position.y = self.titles['controls'].get_bottom() + self.TITLE_SPACING
    #     # ----------------------------------------------------------------
    #     self.createLabels(self.labels, position)
    #     last_label = next(reversed(self.labels)) # reversed iterator
    #     position.y = self.labels[last_label].get_bottom() + self.SPACING
    #     # ----------------------------------------------------------------    
    #     self.createButtons(self.buttons, position)
    #     self.buttons['back'].shift((0, self.SPACING))

    #     # create iterator
    #     self.buttons_handler = ButtonsHandler(self.buttons)

class MenuContex:
    def __init__(self, text : dict):
        self.font = BiggerFont()

        self.exit = Exit(text, self.font)
        self.pause = Pause(text, self.font)
        self.controls = Controls(text, self.font)
        self.start = Start(text, self.font)

        self.menu = self.start
        self.back_menu = self.start
        # self.main_menu = self.pause

    def update(self):
        self.menu.update()
        # self.change(key)

    def change(self, key):
        if key:
            if key == "pause":
                self.menu = self.pause
                # self.back = None
            elif key == "exit":
                self.menu = self.exit
                # self.back = self.exit
                # self.back = None
            elif key == "controls":
                self.back_menu = self.menu
                self.menu = self.controls
            elif key == "back":
                self.menu = self.back_menu

            # print("Menu changed:", key)

    def back(self):
        return self.menu.back()

    def display(self):
        self.menu.display()

    def change_BiggerFont(self):
        self.font.change_BiggerFont()

        self.exit.change_Font()
        self.pause.change_Font()
        self.controls.change_Font()
        self.start.change_Font()
