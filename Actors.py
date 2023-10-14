from pygame import draw

class Actors:
    def __init__(self):
        self.actors = {}   # dict, not list

    def add(self, name, object):
        if not self.actors.get(name):
            self.actors[name] = object

    def update(self):
        if self.actors:
            for actor in self.actors.values():
                if actor:   # not None
                    actor.update()  # requre update method

    def draw(self, screen, colour = None):
        if self.actors:
            for actor in self.actors.values():
                if actor:
                    actor.draw(screen)  # requre draw method
                    if colour:
                        draw.rect(screen, colour, actor.rect, 2)

    def init(self):
        if self.actors:
            for actor in self.actors.values():
                actor.init()  # requre init method

    def get(self, name):
        return self.actors.get(name)

    def remove(self, name):
        if self.actors.get(name):
            return self.actors.pop(name)

    def clear(self):
        self.actors.clear()
