import random
from text.Button import WhiteText
import pygame.font
from pygame.display import get_surface
from pygame.math import Vector2
from add.Clock import Clock
import queue
from add.Path import resource_path, load_json
from os.path import join
from sys import argv


class Jokes:
    def __init__(self):
        self.data = {}
        self.data['common'] = self.load_jokes('Jokes.json')
        self.data['profanity'] = self.load_jokes('Jokes_prof.json') # profanity
        self.data['abscenity'] = self.load_jokes('Jokes_abs.json')  # abscenity
        self.data['tits'] = self.load_jokes('Jokes_tits.json')      # tits

        # print('abscenity', self.data['abscenity']['snow_white'])
        # print('tits', self.data['tits']['snow_white'])

        self.length = 0
        # 'common', 'profanity', 'abscenity', 'tits'
        self.combination = ['common', 'profanity', 'abscenity', 'tits'] # set не зберігає порядок елементів
        self.jokes = dict()
        self.create()  # uses jokes, combination and length

        # print(self.jokes)

    def load_jokes(self, file):
        path = resource_path(join('text', file))
        return load_json(path)  # dict
        # self.data.update(temp_dict)

    def create(self):
        self.jokes.clear()
        # print('combination', self.combination)
        for key in self.combination:
            # print(key)
            self.jokes.update(self.data[key])

        self.length = len(self)
        # return jokes

    def get_joke(self):

        if self.jokes and self.combination:
            key = random.choice(list(self.jokes.keys()))
            joke = Joke(self.jokes[key])
            self.jokes.pop(key, None)
        
            if not self.jokes: # and self.combination:
                self.jokes = self.create()
                
            return joke
        elif not self.combination:
            print('Список combination пустий')
    
    def get_some_joke(self, key):
        if key in self.jokes:
            return Joke(self.jokes[key])
        else:
            for category in self.data.values():
                if category.get(key, None):
                    return Joke(category[key])

    # повертає рядок з кількостю жартів для виводу на екран чи в меню
    def get_text(self):
        text = str(len(self.jokes)) + "/" + str(self.length)
        return text
    
    def on(self, category : str):
        if category in self.data.keys():
            self.combination.append(category)   # add для set
            self.jokes.update(self.data[category])
            self.length = len(self)
    
    def off(self, category : str):
        if category in self.data.keys() and category in self.combination:
            self.combination.remove(category)   # discard для set, не викликає KeyError, на відміну від remove
            for key in self.data[category]:
                if key in self.jokes:
                    self.jokes.pop(key)
            self.length = len(self)

    def __len__(self):
        length = 0
        for category in self.combination:
            length += len(self.data[category])

        return length

    def set_button(self, button : str):
        name, state = button.split('_')
        # print('name, state', name, state)
        if state == 'on':
            self.on(name)
        elif state == 'off':
            self.off(name)

class Joke:
    def __init__(self, joke_list : list):
        self.data = queue.Queue()
        for line in joke_list:
            self.data.put(line)

        # self.font = pygame.font.SysFont("Montserrat", 25)
        # self.font = pygame.font.SysFont("Arial", 25)
        # self.font = pygame.font.SysFont("Verdana", 20)
        # self.font = pygame.font.SysFont("Tahoma", 16)
        self.font = pygame.font.SysFont("Arial Narrow", 25)
        # self.font = pygame.font.SysFont("Calibri", 25)
        # self.font = pygame.font.SysFont("Courier New", 20)
        # self.font = pygame.font.SysFont("Times New Roman", 25)
        self.curent = self.get_line()
        self.screen = get_surface()
        self.active = True

    def display(self, pos):
        if self.curent.active:
            self.curent.update()
            self.curent.draw(self.screen, pos)
        else:
            self.curent = self.get_line()

    def get_line(self):
        if not self.data.empty():
            return Line(self.data.get(), self.font)
        else:
            self.active = False

class Line:
    def __init__(self, line : str, font):
        self.data = queue.Queue()
        for char in line:
            self.data.put(char)

        self.FRAME = 70 # frame time
        # self.time = len(self.data) * self.FRAME
        self.clock = Clock(self.FRAME)
        self.clock_after = None

        self.line = str()
        self.font = font
        self.active = True
        self.text = self.get_text()

    def get_text(self):
        if not self.data.empty():
            char = self.data.get()
            # self.line += char
            self.line = self.line + char
            return WhiteText(self.line, self.font)

    def update(self):
        if not self.data.empty():
            self.clock.start()
            if self.clock.next():
                self.text = self.get_text()
        elif not self.clock_after:
            self.clock_after = Clock(500)
            self.clock_after.start()
        elif self.clock_after.end():
            self.active = False

    def draw(self, screen, pos):
        # text = Button(self.line, self.font, midbottom=pos)
        self.text.update_pos(pos)
        self.text.draw(screen)

class JokeHandler:
    def __init__(self, jokes : Jokes):
        self.jokes = jokes
        # self.rect = rect
        self.joke = None

    def get_joke(self):
        if not self.joke:
            self.joke = self.jokes.get_joke()
            # self.joke = self.jokes.get_some_joke("pivonii") # jonny, kass, snow_white

    def draw_joke(self, midtop):
        if self.active():
            pos = Vector2(midtop)
            pos.y -= 20
            self.joke.display(pos)

    def active(self):
        if self.joke:
            if self.joke.active:
                return True
            else:
                self.joke = None
        #         return False
        # else:
        #     return False

        return False

    def clear(self):
        self.joke = None