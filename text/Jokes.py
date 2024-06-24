import json
import sys
import random
from text.Text import Button
import pygame.font
from pygame.display import get_surface
from add.Clock import Clock
import queue
from add.Path import resource_path, load_json
from os.path import join

class Jokes:
    def __init__(self):
        path = resource_path(join('text','Jokes.json'))
        self.data = load_json(path)
        self.jokes = list(self.data.keys())

    def get_joke(self):
        if not self.jokes:
            self.jokes = list(self.data.keys())

        key = random.choice(self.jokes)
        joke = self.data[key]
        self.jokes.remove(key)
        # print(key)
        return Joke(joke)
    
    def get_some_joke(self, key):
        return Joke(self.data[key])

class Joke:
    def __init__(self, joke_list : list):
        self.data = queue.Queue()
        for line in joke_list:
            self.data.put(line)

        # self.font = pygame.font.SysFont("Montserrat", 25)
        # self.font = pygame.font.SysFont("Arial", 25)
        # self.font = pygame.font.SysFont("Verdana", 20)
        self.font = pygame.font.SysFont("Tahoma", 18)
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
            return Button(self.line, self.font)

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
