import pygame
from pygame.math import Vector2
from pygame.display import get_surface
from add.Path import resource_path
from os.path import join
from random import choice
from text.Button import Button, SwitchButton, OnOffButton, ButtonsHandler, JokesBar
from text.Text import Text

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
    def __init__(self, text : Text, font : BiggerFont):
        # self.font = BiggerFont()
        self.font = font
        self.screen = get_surface()
        self.center = Vector2(self.screen.get_rect().center)
        self.center.y -= 85

        self.text = text
        # ----------------------------------------------------------------
        self.titles_list = []
        self.labels_list = []
        self.buttons_list = []
        # ----------------------------------------------------------------
        self.titles = {}
        self.labels = {}
        self.buttons = {}
        self.buttons_handler = None

        # self.create()
        self.TITLE_SPACING = 50
        self.SPACING = 30

    def init(self):
        # self.create(self.titles_list, self.buttons_list, self.labels_list) # list(self.labels.keys())
        for key in self.titles:
            self.titles[key].change_text(self.text[key])

        for key in self.labels:
            self.labels[key].change_text(self.text[key])

        for key in self.buttons:
            self.buttons[key].change_text(self.text[key])

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

    def create(self, titles : list, buttons : list, labels : list = None): # , position : Vector2 = None
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
        # print(type(self), "created")

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

    def change_color(self, color : str):
        self.buttons_handler.active.change_color(color)

    def back(self):
        return None
    
class Exit(Menu):
    def __init__(self, *args):
        super().__init__(*args)
        self.titles_list = ['over_1', 'over_2']
        self.buttons_list = ['restart_button', 'exit_button']
        self.create(self.titles_list, self.buttons_list)

class Pause(Menu):
    def __init__(self, *args):
        super().__init__(*args)
        self.titles_list = ['pause']
        self.buttons_list = ['continue', 'controls', 'jokes', 'settings', 'restart_button', 'exit_button']
        self.create(self.titles_list, self.buttons_list)

    def back(self):
        return "game"

class Start(Menu):
    def __init__(self, *args):
        super().__init__(*args)
        self.titles_list = ['start']
        self.buttons_list = ['new_game', 'controls', 'jokes', 'settings', 'exit_button']
        self.create(self.titles_list, self.buttons_list)

class Controls(Menu):
    def __init__(self, *args):
        super().__init__(*args)
        self.titles_list = ['controls']
        # self.titles = dict.fromkeys(titles)
        self.labels_list = [
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
        self.buttons_list = ['back']
        # self.buttons = dict.fromkeys(buttons)
        self.SPACING = 15
        self.center.y = 50  # new title position
        
        self.create(self.titles_list, self.buttons_list, self.labels_list)

    # def init(self):
    #     self.create(list(self.titles.keys()), list(self.buttons.keys()), list(self.labels.keys()))

    def create(self, titles, buttons, labels):
        super().create(titles, buttons, labels)
        self.buttons['back'].shift((0, self.SPACING))

    def back(self):
        return "back"

class Settings(Menu):
    def __init__(self, text, font):
        super().__init__(text, font)
        self.titles_list = ['settings']
        self.labels_list = ['language', 'color']
        self.buttons_list = ['back']
        # switchers =  ['color_red', 'color_green', 'color_blue']
        
        # self.jokes = jokes
        self.create(self.titles_list, self.buttons_list, self.labels_list)

    def init(self):
        # self.create(list(self.titles.keys()), list(self.buttons.keys()), list(self.labels.keys()))
        for key in self.titles:
            self.titles[key].change_text(self.text[key])

        for key in self.labels:
            if key != 'jokes_count':
                self.labels[key].change_text(self.text[key])

        for key in self.buttons:
            if key == 'color_select' or key == 'language_select':
                self.buttons[key].change_text() # self.text.text
            else:
                self.buttons[key].change_text(self.text[key])

    def createSwitchers(self):
        color_select = ['color_white', 'color_red', 'color_green', 'color_blue', "color_yellow", "color_violet", "color_magenta", "color_purple", "color_orchid", "color_cyan", "color_black"]
        self.buttons['color_select'] = SwitchButton(color_select, self.text, self.font.myfont, (0,0))
        # ----------------------------------------------------------------
        language_select = ['lang_uk', 'lang_en']
        self.buttons['language_select'] = SwitchButton(language_select, self.text, self.font.myfont, (0,0))

    def back(self):
        return "back"
    
    def create(self, titles : list, buttons : list, labels : list = None): # , position : Vector2 = None
        # if not position:
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
        self.createSwitchers()
        # ----------------------------------------------------------------
        # text = self.jokes.get_text()
        # self.createText('jokes_count', text, Vector2(position))
        # ----------------------------------------------------------------
        position = Vector2(back)
        self.set_position(self.labels['language'], self.buttons['language_select'], Vector2(position))
        position.y = self.labels['language'].get_bottom() + self.SPACING
        self.set_position(self.labels['color'], self.buttons['color_select'], Vector2(position))
        # position.y = self.labels['color'].get_bottom() + self.SPACING
        # self.set_position(self.labels['jokes'], self.labels['jokes_count'], Vector2(position))
        # ----------------------------------------------------------------
        position.y = self.labels['color'].get_bottom() + self.SPACING
        self.buttons['back'].update_pos(position)
        # print("position after update_pos", position)
        
        # create iterator
        self.buttons_handler = ButtonsHandler(self.buttons)
        # print(type(self), "created")

class JokesMenu(Menu):
    def __init__(self, text, font, jokes = None):
        super().__init__(text, font)
        self.titles_list = ['jokes']
        self.labels_list = ['common', 'profanity', 'abscenity', 'tits']
        self.buttons_list = ['jokes_reload','back']
        self.jokes = jokes
        self.center.y -= 50

        self.create(self.titles_list, self.buttons_list, self.labels_list)

    def init(self):
        # self.create(list(self.titles.keys()), list(self.buttons.keys()), list(self.labels.keys()))
        for key in self.titles:
            self.titles[key].change_text(self.text[key])

        for key in self.labels:
            if key != 'jokes_count':
                self.labels[key].change_text(self.text[key])

        for key in self.buttons:
            if key in self.labels_list:
                self.buttons[key].change_text()
            else:
                self.buttons[key].change_text(self.text[key])

    def set_jokes(self, jokes):
        self.jokes = jokes
        position = Vector2(self.labels['tits'].get_center())
        position.y = self.labels['tits'].get_bottom() + self.SPACING
        self.createJokesText(position)
        # self.jokes_bar = JokesBar(self.jokes, self.buttons_handler)
        # ----------------------------------------------------------------
        self.buttons['back'].update_pos(position)

    def createJokesText(self, position):
        self.labels["jokes"] = Button("jokes", self.text["jokes"], self.font.myfont, (0,0))
        text = self.jokes.get_text()
        self.createText('jokes_count', text, (0,0))
        self.set_position(self.labels['jokes'], self.labels['jokes_count'], Vector2(position))
        position.y = self.labels['jokes'].get_bottom() + self.SPACING

    def createOnOffButton(self, name):
        self.buttons[name] = OnOffButton(name, self.text, self.font.myfont, (0,0))

    def createSwitchers(self):
        for label in self.labels_list:
            # if label != "jokes":
            self.createOnOffButton(label)

    def back(self):
        return "back"
    
    def create(self, titles : list, buttons : list, labels : list = None): # , position : Vector2 = None
        # if not position:
        position = Vector2(self.center)
        # ----------------------------------------------------------------
        self.createTitles(titles, position) # змінює position.y
        back = Vector2(position)
        # ----------------------------------------------------------------
        self.createLabels(labels, position) # змінює position.y
        # ----------------------------------------------------------------
        self.createButtons(buttons, position) # змінює position.y
        # ----------------------------------------------------------------
        self.createSwitchers()
        # ----------------------------------------------------------------
        position = Vector2(back)
        for label in self.labels_list:
            self.set_position(self.labels[label], self.buttons[label], Vector2(position))
            position.y = self.labels[label].get_bottom() + self.SPACING
        # ----------------------------------------------------------------
        if self.jokes:
            self.createJokesText(position)
        # ----------------------------------------------------------------
        self.buttons['jokes_reload'].update_pos(position)
        position.y = self.buttons['jokes_reload'].get_bottom() + self.SPACING - 10
        # ----------------------------------------------------------------
        # self.buttons['back'].update_pos(position)
        
        # create iterator
        self.buttons_handler = ButtonsHandler(self.buttons)

        self.buttons_handler.post(self.buttons['abscenity'].press())
        self.buttons_handler.post(self.buttons['tits'].press())
        # ----------------------------------------------------------------
        if self.jokes:
            self.jokes_bar = JokesBar(self.jokes, self.buttons_handler)
            self.jokes_bar.set_position(position)
            position.y += self.SPACING
            self.buttons['back'].update_pos(position)

    def update(self):
        super().update()
        text = self.jokes.get_text()
        if self.labels['jokes_count'].text != text:
            self.labels['jokes_count'].change_text(text)

        # TODO потенційна помилка, якщо jokes_bar не буде проініціалізовано на момент виклику update
        self.jokes_bar.update()

    def display(self):
        super().display()
        self.jokes_bar.draw(self.screen)

class MenuContex:
    def __init__(self, text : Text, jokes):
        # таким чином усі меню мають однаковий шрифт
        # якби він був всередині класу Menu, усі меню мали б різний шрифт
        self.text = text
        self.font = BiggerFont()
        self.color = "White"
        self.all_menu = {}

        self.all_menu["start"] = Start(text, self.font)
        self.all_menu["pause"] = Pause(text, self.font)
        self.all_menu["controls"] = Controls(text, self.font)
        self.all_menu["settings"] = Settings(text, self.font)
        self.all_menu["exit"] = Exit(text, self.font)
        self.all_menu["jokes"] = JokesMenu(text, self.font, jokes)
        # self.all_menu["jokes"].set_jokes(jokes)

        self.current = "start"
        self.back_menu = "start"
        # self.main_menu = self.pause

    def update(self):
        self.all_menu[self.current].update()
        # self.change(key)

    def change(self, key):
        if key:
            if key == "pause":
                self.current = key
                # self.back = None
            elif key == "exit":
                self.current = key
                # self.back = self.exit
                # self.back = None
            elif key == "controls":
                self.back_menu = self.current
                self.current = key
            elif key == "settings":
                self.back_menu = self.current
                self.current = key
            elif key == "jokes":
                self.back_menu = self.current
                self.current = key
            elif key == "back":
                self.current = self.back_menu

            # print("Menu changed:", key)

    # визначає, чи може меню повертатись назад до попереднього меню, чи ні
    # повертає back - якщо так, None - якщо ні, і game - якщо повертає в гру
    def back(self):
        return self.all_menu[self.current].back()

    def display(self):
        self.all_menu[self.current].display()

    def change_BiggerFont(self):
        self.font.change_BiggerFont()

        for menu in self.all_menu.values():
            menu.change_Title()

        # self.exit.change_Title()
        # self.pause.change_Title()
        # self.controls.change_Title()
        # self.settings.change_Title()
        # self.start.change_Title()

    def get_color(self, key):
        if key == "color_white":
            return "white"
        elif key == "color_black":
            return "Black"
        elif key == "color_red":
            return "Red"
        elif key == "color_green":
            return "Green"
        elif key == "color_blue":
            return "Blue"
        elif key == "color_yellow":
            return "yellow"
        elif key == "color_violet":
            return "darkviolet"
        elif key == "color_purple":
            return "purple4"
        elif key == "color_orchid":
            return "darkorchid4"
        elif key == "color_magenta":
            return "darkmagenta"
        elif key == "color_cyan":
            return "cyan"

    def change_color(self, color):
        self.color = color
        # self.exit.change_color(color)
        # self.pause.change_color(color)
        # self.controls.change_color(color)
        # self.settings.change_color(color)
        # self.start.change_color(color)

        for menu in self.all_menu.values():
            menu.change_color(color)

    def change_color_key(self, key):
        self.change_color(self.get_color(key))

    def reload(self):
        # TODO потрібно змінювати текст у кожного titles, labels, buttons
        # інакше змінюється стан SwitchButton, коли ми її перестворюємо з допомогою createSwitchers
        # це потрібно робити циклічно у методах init
        # потрібно всього лиш змінити текст кожної кнопки, а не перестворювати і виставляти їх усі заново
        # також варто приймати об'єкт Text за посиланням, а не dict за значенням
        for menu in self.all_menu.values():
            menu.init()
