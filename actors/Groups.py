import pygame
from interface.Drawer import Drawer
# from Bullet import Bullet

class Actors:
    def __init__(self):
        self.actors = {}   # dict, not list

    # def add(self, name, object):
    #     if not self.actors.get(name):
    #         self.actors[name] = object
    def sprites(self):
        # return list(self.actors)
        return self.actors.values()

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

class MyGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

        # self.alpha_rect = pygame.Surface((100, 100)) #self.get_size()
        # print(self.alpha_rect.get_width(), " ", self.alpha_rect.get_height())
        # self.alpha_rect.set_alpha(100)

    # def draw(self):
    #     pass

class Groups:
    def __init__(self):
        self.bats = MyGroup()
        self.bullets = MyGroup()
        self.actors = Actors()
        self.dummies = Actors()

        self.drawer = Drawer()
        # self.screen = pygame.display.get_surface()

    # add bat to a group
    def add_bat(self, bat):
        self.bats.add(bat)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def add_actor(self, key, actor):
        self.actors.add_actor(key, actor)

    def update(self):
        self.dummies.update()
        self.bats.update()
        self.bullets.update()
        self.actors.update()

    def draw(self):
        self.drawer.draw_group(self.dummies)
        self.drawer.draw_group(self.bats)
        self.drawer.draw_group(self.bullets)
        self.drawer.draw_group(self.actors)

    def clear(self):
        self.dummies.clear()
        self.bats.empty()
        self.bullets.empty()
        self.actors.clear() # dictionary
