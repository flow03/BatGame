import json
import sys
import random
from interface.Text import Button
import pygame.font
from pygame.display import get_surface
from add.Clock import Clock
import queue
from add.Path import resource_path
from os.path import join

class Jokes:
    def __init__(self):
        path = resource_path(join('interface','Jokes.json'))
        self.data = self.load(path)
        self.jokes = list(self.data.keys())

    def load(self, json_file):
        with open(json_file, 'r', encoding='utf-8-sig') as file: # відкриття файлу з кодуванням UTF-8-BOM
            try:
                loaded_data = json.load(file) # конвертує бінарні дані в текстовий рядок
                # self.jokes.update(loaded_data)
                return loaded_data # dict
            except json.JSONDecodeError as e:
                print(f"Неможливо прочитати JSON з файлу '{json_file}'")
                print(f"Line: {e.lineno}, Column: {e.colno}, {e.msg}")
                print(f"Content: {e.doc.splitlines()[e.lineno - 1]}")
                sys.exit(1)    

    def get_joke(self):
        if not self.jokes:
            self.jokes = list(self.data.keys())

        key = random.choice(self.jokes)
        joke = self.data[key]
        self.jokes.remove(key)
        return Joke(joke)

class Joke:
    def __init__(self, joke_list : list):
        self.data = queue.Queue()
        for line in joke_list:
            self.data.put(line)

        self.font = pygame.font.SysFont("Montserrat", 25)
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

    # def active(self):
    #     return self.active

class Line:
    def __init__(self, line : str, font):
        self.data = queue.Queue()
        for char in line:
            self.data.put(char)

        self.line = str()

        self.FRAME = 70 # frame time
        # self.time = len(self.data) * self.FRAME
        self.clock = Clock(self.FRAME)
        self.clock_after = None

        self.font = font
        self.active = True

    def add_char(self):
        if not self.data.empty():
            char = self.data.get()
            # self.line += char
            self.line = self.line + char
            # self.data = self.data[1:]

    def update(self):
        if not self.data.empty():
            self.clock.start()
            if self.clock.next():
                self.add_char()
        elif not self.clock_after:
            self.clock_after = Clock(500)
            self.clock_after.start()
        elif self.clock_after.end():
            self.active = False
            # return False

        # return True

    def draw(self, screen, pos):
        text = Button(self.line, self.font, pos)
        text.draw(screen)
