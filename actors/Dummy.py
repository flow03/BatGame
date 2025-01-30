import pygame
import os.path
from pygame.math import Vector2
from interface.HealthBar import Health
import interface.HealthBar as HealthBar
import interface.Shields as Shields
from add.Path import resource_path
from add.Clock import Clock

class Dummy(pygame.sprite.Sprite):
    def __init__(self, pos, bullet_list, health = 100):
        super().__init__()
        
        self.load_images()
        self.rect = self.image.get_rect(center=pos)

        self.bullet_list = bullet_list
        self.re_delay = Clock(600)
        self.turn_delay = Clock(400)

        self.health = Health(health)
        # self.shield = None
        self.dead = False
        self.turned = False

        self.healthBarCreate()
        # self.update_bar_pos()
        # print("dummy ", self.health_bar.bordered_rect.width, self.health_bar.bordered_rect.height)

    def load_images(self):
        self.images = {}
        self.images['front'] = self.get_image('dummy_front.png')
        self.images['back'] = self.get_image('dummy_back.png')
        self.images['left'] = self.get_image('dummy_left.png')
        self.images['right'] = self.get_image('dummy_right.png')
        # self.images['right'] = pygame.transform.flip(self.images['left'], True, False)
        # for key in self.images:
        #     self.images[key] = self.resize_image(self.images[key], 100)
            
        self.image = self.images['front']

    def get_image(self, name):
        path = resource_path('img/dummy')
        img_url = os.path.join(path, name)
        image = pygame.image.load(img_url).convert_alpha()
        return image

    # TODO достатньо одного методу у об'єкті health_bar 
    def update_bar_pos(self):
        new_pos = Vector2(self.rect.midtop)
        new_pos.y -= 10
        self.health_bar.update_pos(new_pos)

    def healthBarCreate(self):
        self.health.restore()
        health_bar_rect = pygame.Rect((0, 0), (100, 8)) # (0, 0) position
        self.health_bar = HealthBar.FancyBoundHealthBar(health_bar_rect, self.health, 1)

        self.update_bar_pos()

    def init(self):
        # self.health_bar.init()
        self.healthBarCreate()
        self.dead = False

    def update(self):
        self.collide_bullet()
        
        if self.dead:
            if self.re_delay.end():
                self.healthBarCreate()
                self.dead = False
                self.image = self.images['front']
        else:
            if self.turned and self.turn_delay.end():
                self.turned = False
                self.image = self.images['front']
            # place for another not dead logic...

        self.health_bar.update_health()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.health_bar.draw(screen)

    def collide_bullet(self):
        if self.bullet_list:
            bullet = pygame.sprite.spritecollideany(self, self.bullet_list)
            if bullet:
                self.turn(bullet)
                self.set_damage(bullet.damage)
                bullet.kill()

        # if self.bullet_list:
        #     for bullet in self.bullet_list:
        #         if self.rect.colliderect(bullet.rect):
        #             self.set_damage(bullet.damage)
        #             bullet.kill()

    def set_damage(self, damage):
        self.health_bar.set_damage(damage)
        if self.health.empty():
            self.dead = True
            self.re_delay.restart()
            self.image = self.images['back']

    def set_heal(self, heal : int):
        self.health_bar.set_heal(heal)

    def resize_image(self, image : pygame.Surface, new_h):
        original_w = image.get_width()
        original_h = image.get_height()
        new_w = int(original_w * (new_h/original_h))
        # print(f"new_h: {new_h}, new_w: {new_w}")

        return pygame.transform.scale(image, (new_w, new_h))
    
    def get_direction(self, target : Vector2):
        target = Vector2(target)
        pos = Vector2(self.rect.center)
        diff = pos.x - target.x
        if diff > 0:
            return 'left'
        else:
            return 'right'

    def turn(self, bullet):
        self.turned = True
        direction = self.get_direction(bullet.rect.center)
        self.image = self.images[direction]
        self.turn_delay.restart()

class CellDummy(Dummy):
    def __init__(self, *args):
        super().__init__(*args)

    def healthBarCreate(self):
        self.health.restore()
        health_bar_rect = pygame.Rect((0, 0), (100, 8))
        self.health_bar = HealthBar.FancyCellHealthBar(health_bar_rect, self.health, 1)
        self.update_bar_pos()

class BlueDummy(Dummy):
    def __init__(self, *args):
        super().__init__(*args)

    def healthBarCreate(self):
        self.health.restore()
        health_bar_rect = pygame.Rect((0, 0), (100, 8))
        self.health_bar = Shields.ShiftBlueShield(health_bar_rect, self.health, 1)
        # self.health_bar.shifting = True
        self.update_bar_pos()

class GrayDummy(Dummy):
    def __init__(self, *args):
        super().__init__(*args)

    def healthBarCreate(self):
        self.health.restore()
        health_bar_rect = pygame.Rect((0, 0), (100, 8))
        self.health_bar = Shields.GrayShield(health_bar_rect, self.health, 1)
        self.update_bar_pos()

class FancyBlueDummy(Dummy):
    def __init__(self, shield = 0, *args):
        self.shield = Health(shield)
        super().__init__(*args)

    def healthBarCreate(self):
        self.health.restore()
        self.shield.restore()
        health_bar_rect = pygame.Rect((0, 0), (100, 8))
        health_bar = HealthBar.FancyHealthBar(health_bar_rect, self.health, 1)
        shield_bar = Shields.BlueShield(health_bar_rect, self.shield, 1)
        self.health_bar = Shields.AllHealthBars(health_bar, shield_bar)
        self.update_bar_pos()

class FancyGrayDummy(Dummy):
    def __init__(self, shield = 0, *args):
        self.shield = Health(shield)
        super().__init__(*args)

    def healthBarCreate(self):
        self.health.restore()
        self.shield.restore()
        health_bar_rect = pygame.Rect((0, 0), (100, 8))
        health_bar = HealthBar.FancyBoundHealthBar(health_bar_rect, self.health, 1)
        shield_bar = Shields.GrayShield(health_bar_rect, self.shield, 1)
        self.health_bar = Shields.AllHealthBars(health_bar, shield_bar)
        self.update_bar_pos()

class DummyCreator():
    def __init__(self, groups):
        self.groups = groups
        self.is_dummies = False
        screen = pygame.display.get_surface()
        self.center = Vector2(screen.get_size())//2

    def create(self):
        if self.is_dummies:
            self.createDummies()

    def createDummies(self):
        pos = Vector2(self.center.x - 200, self.center.y)
        left_dummy = FancyBlueDummy(5, pos, self.groups.bullets, 50)
        pos = Vector2(self.center.x + 200, self.center.y)
        right_dummy = FancyGrayDummy(30, pos, self.groups.bullets, 50)
        pos = Vector2(self.center.x - 200, self.center.y - 200)
        topleft_dummy = BlueDummy(pos, self.groups.bullets, 3)
        pos = Vector2(self.center.x + 200, self.center.y - 200)
        topright_dummy = GrayDummy(pos, self.groups.bullets, 50)
        pos = Vector2(self.center.x, self.center.y + 200)
        down_dummy = CellDummy(pos, self.groups.bullets, 15)

        self.groups.dummies.add_actor("left_dummy", left_dummy)
        self.groups.dummies.add_actor("right_dummy", right_dummy)
        self.groups.dummies.add_actor("topleft_dummy", topleft_dummy)
        self.groups.dummies.add_actor("topright_dummy", topright_dummy)
        self.groups.dummies.add_actor("down_dummy", down_dummy)

    def deleteDummies(self):
        self.groups.dummies.clear()

    def switchDummies(self):
        if self.is_dummies:
            self.deleteDummies()
            self.is_dummies = False
        else:
            self.createDummies()
            self.is_dummies = True

# class NewDummy(Dummy):
#     def __init__(self, *args):
#         super().__init__(*args)

        