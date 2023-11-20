from pygame import draw
from add.MyGroup import MyGroup

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

def get_colour(isBoundRects):
    colourGreen = None
    colourRed = None

    if isBoundRects:
        colourGreen = "Green"
        colourRed = "Red"

    return colourGreen, colourRed

class Actors_:
    def __init__(self):
        # dict of MyGroups
        self.actors = {
            'bats': MyGroup(),
            'bullets': MyGroup(),
            'actors': MyGroup()
        }

    # add item to group
    def add(self, name, object):
        self.actors[name].add(object)

    def update(self):
        for group in self.actors.values():
            if group:   # not empty
                group.update()

    def draw(self, screen, colour = None):
        # colourGreen, colourRed = get_colour(isBoundRects)
        # self.actors['bats'].draw(screen, colourRed)
        # self.actors['bullets'].draw(screen, colourGreen)
        # self.actors['actors'].draw(screen, colourRed)

        for group in self.actors.values():
            if group:   # not empty
                if colour and group == self.actors['bullets']:
                    self.actors['bullets'].draw(screen, 'Green')
                else:
                    group.draw(screen, colour)

    def init(self):
        if self.actors['actors']: # not empty
            for actor in self.actors['actors']:
                actor.init()

    # get group
    def get(self, name):
        return self.actors.get(name)

    # does nothing
    def remove(self, name):
        ...

    def empty(self, name):
        if self.actors.get(name):
            self.actors[name].empty()

    def clear(self):
        for group in self.actors.values():
            if group:
                group.empty()

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.add(index, value)
