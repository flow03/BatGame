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
        self.labels = {}
        self.buttons = {}
        self.buttons_handler = None

        # self.create()
        self.LABEL_SP = 50
        self.SPACING = 30

    def createButtons(self, buttons : list, pos : Vector2):
        # pos = pos
        for key in buttons:
            self.buttons[key] = Button(self.text[key], self.font.myfont, pos)
            pos.y = self.buttons[key].get_bottom() + self.SPACING

    def createLabels(self, labels : list, pos : Vector2):
        # pos = pos
        for key in labels:
            self.labels[key] = Button(self.text[key], self.font.myBiggerFont, pos)
            pos.y = self.labels[key].get_bottom() + self.SPACING

    def create(self, labels : list, buttons : list):
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
        self.createLabels(labels, position)

        last_label = next(reversed(self.labels)) # reversed iterator
        # print('last_label', last_label)
        # TODO потенційна помилка, якщо self.labels пустий
        position.y = self.labels[last_label].get_bottom() + self.LABEL_SP
        self.createButtons(buttons, position)
        
        # create iterator
        self.buttons_handler = ButtonsHandler(self.buttons)

    def update(self):
        self.buttons_handler.update_mouse()
        self.buttons_handler.update_keys()

    def display(self):
        for label in self.labels.values():
            label.draw(self.screen)
        for button in self.buttons.values():
            button.draw(self.screen)

    def change_Font(self, ):
        # self.font.change_BiggerFont()
        self.create(list(self.labels.keys()), list(self.buttons.keys()))

    def back(self):
        return None
    
class Exit(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        labels = ['over_1', 'over_2']
        buttons = ['restart_button', 'exit_button']
        self.create(labels, buttons)

class Pause(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        labels = ['pause']
        buttons = ['continue', 'controls', 'restart_button', 'exit_button']
        self.create(labels, buttons)

    def back(self):
        return "game"

class Start(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        labels = ['start']
        buttons = ['new_game', 'controls', 'exit_button']
        self.create(labels, buttons)

class Controls(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        labels = ['controls']
        buttons = [
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
        'help',
        'back']
        self.SPACING = 15
        self.create(labels, buttons)

    def back(self):
        return "back"

    def create(self, labels : list, buttons : list):
        position = Vector2(self.center.x, 50)
        self.createLabels(labels, position)

        # last_label = next(reversed(self.labels)) # reversed iterator
        position.y = self.labels['controls'].get_bottom() + self.LABEL_SP
        self.createButtons(buttons, position)
        # self.buttons['back'].rect.center += 30
        self.buttons['back'].shift((0, self.SPACING))

        # create iterator
        self.buttons_handler = ButtonsHandler(self.buttons)

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
