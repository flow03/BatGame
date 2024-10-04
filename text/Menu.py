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
        self.center.y -= 85

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
        for key in buttons:
            self.createButton(key, pos)
            pos.y = self.buttons[key].get_bottom() + self.SPACING

    def createButton(self, key : str, pos : Vector2):
        self.buttons[key] = Button(key, self.text[key], self.font.myfont, pos)

    def createLabels(self, labels : list, pos : Vector2):
        for key in labels:
            self.labels[key] = Button(key, self.text[key], self.font.myfont, pos)
            pos.y = self.labels[key].get_bottom() + self.SPACING

    def createText(self, key : str, text : str, pos : Vector2):
        self.labels[key] = Button(key, text, self.font.myfont, pos)
        # return self.labels[key]

    # розміщує дві кнопки/написи рівновіддалено по боках від заданої точки
    def set_position(self, button1 : Button, button2 : Button, pos : Vector2, shift = 70):
        left = Vector2(pos)
        left.x -= shift
        button1.update_pos(left)

        right = Vector2(pos)
        right.x += shift
        button2.update_pos(right)

    def createTitles(self, titles : list, pos : Vector2):
        for key in titles:
            self.titles[key] = Button(key, self.text[key], self.font.myBiggerFont, pos)
            pos.y = self.titles[key].get_bottom() + self.TITLE_SPACING

    def create(self, titles : list, buttons : list, labels : list = None, position : Vector2 = None):
        if not position:
            position =  Vector2(self.center)
        # ----------------------------------------------------------------
        self.createTitles(titles, position)
        # TODO потенційна помилка, якщо self.titles пустий
        # last_title = next(reversed(self.titles)) # reversed iterator
        # last_title = titles[-1]
        # position.y = self.titles[last_title].get_bottom() + self.TITLE_SPACING
        # ----------------------------------------------------------------
        if labels:
            self.createLabels(labels, position)
            # last_label = next(reversed(self.labels)) # reversed iterator
            # last_label = labels[-1]
            # position.y = self.labels[last_label].get_bottom() + self.SPACING
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

    def change_Title(self):
        # self.font.change_BiggerFont()
        self.createTitles(list(self.titles.keys()), Vector2(self.center))

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
        buttons = ['continue', 'controls', 'settings', 'restart_button', 'exit_button']
        self.create(titles, buttons)

    def back(self):
        return "game"

class Start(Menu):
    def __init__(self, *argv):
        super().__init__(*argv)
        titles = ['start']
        buttons = ['new_game', 'controls', 'settings', 'exit_button']
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
        self.center.y = 50  # new title position
        
        self.create(titles, buttons, labels)
        self.buttons['back'].shift((0, self.SPACING))

    def back(self):
        return "back"

class Settings(Menu):
    def __init__(self, text, font, jokes):
        super().__init__(text, font)
        titles = ['settings']
        labels = ['language', 'color', 'jokes']
        buttons = ['language_select', 'color_select', 'back']
        
        self.jokes = jokes
        self.create(titles, buttons, labels)

    def back(self):
        return "back"
    
    def create(self, titles : list, buttons : list, labels : list = None, position : Vector2 = None):
        if not position:
            position = Vector2(self.center)
        # ----------------------------------------------------------------
        self.createTitles(titles, position) # змінює position.y
        back = Vector2(position)
        # ----------------------------------------------------------------
        self.createLabels(labels, position) # змінює position.y
        # ----------------------------------------------------------------
        self.createButtons(buttons, position) # змінює position.y
        # print("position after createButtons", position)
        # ----------------------------------------------------------------
        text = self.jokes.get_text()
        self.createText('jokes_count', text, Vector2(position))
        # ----------------------------------------------------------------
        position = Vector2(back)
        self.set_position(self.labels['language'], self.buttons['language_select'], Vector2(position))
        position.y = self.labels['language'].get_bottom() + self.SPACING
        self.set_position(self.labels['color'], self.buttons['color_select'], Vector2(position))
        position.y = self.labels['color'].get_bottom() + self.SPACING
        self.set_position(self.labels['jokes'], self.labels['jokes_count'], Vector2(position))
        # ----------------------------------------------------------------
        position.y = self.labels['jokes'].get_bottom() + self.SPACING
        self.buttons['back'].update_pos(position)
        # print("position after update_pos", position)
        
        # create iterator
        self.buttons_handler = ButtonsHandler(self.buttons)

class MenuContex:
    def __init__(self, text : dict, jokes):
        # таким чином усі меню мають однаковий шрифт
        # якби він був всередині класу Menu, усі меню мали б різний шрифт
        self.font = BiggerFont()

        self.start = Start(text, self.font)
        self.pause = Pause(text, self.font)
        self.controls = Controls(text, self.font)
        self.settings = Settings(text, self.font, jokes)
        self.exit = Exit(text, self.font)

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
            elif key == "settings":
                self.back_menu = self.menu
                self.menu = self.settings
            elif key == "back":
                self.menu = self.back_menu

            # print("Menu changed:", key)

    # визначає, чи може меню повертатись назад до попереднього меню, чи ні
    # повертає back - якщо так, None - якщо ні, і game - якщо повертає в гру
    def back(self):
        return self.menu.back()

    def display(self):
        self.menu.display()

    def change_BiggerFont(self):
        self.font.change_BiggerFont()

        self.exit.change_Title()
        self.pause.change_Title()
        self.controls.change_Title()
        self.settings.change_Title()
        self.start.change_Title()
