import pygame
# from pygame import draw
# from Bat import Bat
# from Bullet import Bullet

class Actors:
    def __init__(self):
        self.actors = {}   # dict, not list

    # def add(self, name, object):
    #     if not self.actors.get(name):
    #         self.actors[name] = object

    def add_actor(self, key, actor):
        self.actors[key] = actor

    def update(self):
        if self.actors:
            for actor in list(self.actors.values()):
                actor.update()

    def draw(self, screen, colour = None):
        if self.actors:
            for actor in self.actors.values():
                actor.draw(screen)  # requre draw method
                if colour:
                    pygame.draw.rect(screen, colour, actor.rect, 2)

    def init(self):
        if self.actors:
            for actor in self.actors.values():
                actor.init()  # requre init method

    def get(self, key):
        return self.actors.get(key, None)

    def remove(self, key):
        return self.actors.pop(key, None)

    def clear(self):
        self.actors.clear()
    
    def keys(self):
        return self.actors.keys()
    
    def get_health(self, key):
        actor = self.get(key)
        if actor:
            return actor.health.health
        else:
            return None
    
    def set_damage(self, key, damage):
        actor = self.get_actor(key)
        if actor:
            actor.set_damage(damage)

    def set_heal(self, key, heal):
        actor = self.get_actor(key)
        if actor:
            actor.set_heal(heal)

    def damage_all(self, damage):
        for actor in self.actors.values():
            actor.set_damage(damage)

    def heal_all(self, heal):
        for actor in self.actors.values():
            actor.set_heal(heal)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, actor):
        self.add(key, actor)

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

    # add item to a group
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

class MyGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        
        # self.alpha_rect = pygame.Surface((100, 100)) #self.get_size()
        # print(self.alpha_rect.get_width(), " ", self.alpha_rect.get_height())
        # self.alpha_rect.set_alpha(100)

    def draw(self, screen, colour = None, alpha = False):
        sprites = self.sprites()
        # print(len(sprites))
        if sprites:
            for sprite in sprites:
                if colour and alpha:
                    alpha_rect = self.create_alpha(colour, sprite.rect.size)
                    screen.blit(alpha_rect, sprite.rect)
                    
                # screen.blit(sprite.image, sprite.rect)
                sprite.draw(screen)

                if colour and not alpha:
                    pygame.draw.rect(screen, colour, sprite.rect, 2)

    def create_alpha(self, colour, size):
        alpha_rect = pygame.Surface(size)
        alpha_rect.fill(colour)
        alpha_rect.set_alpha(100)
        return alpha_rect


class Groups:
    def __init__(self):
        self.bats = MyGroup()
        self.bullets = MyGroup()
        self.actors = Actors()

        self.screen = pygame.display.get_surface()

    # add bat to a group
    def add_bat(self, bat):
        self.bats.add(bat)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def add_actor(self, key, actor):
        self.actors.add_actor(key, actor)

    def update(self):
        self.bats.update()
        self.bullets.update()
        self.actors.update()

    def draw(self, colour = None):
        self.bats.draw(self.screen, colour)
        self.bullets.draw(self.screen, colour)
        self.actors.draw(self.screen, colour)

    def clear(self):
        self.bats.empty()
        self.bullets.empty()
        self.actors.clear() # dictionary
