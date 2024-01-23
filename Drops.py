import pygame
from random import randint
# import math
from pygame.math import Vector2
# from add.Spritesheet import SpriteSheet
from Food import Food
from add.MyGroup import MyGroup
from add.Path import resource_path

class BulletDrop(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()
        img_url = resource_path('img/bullet.png')
        self.image = pygame.image.load(img_url).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 9))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.group = group
        self.group.add(self)
        self.screen = pygame.display.get_surface()

    def set_random_coordinates(self, offset = 30):
        coords = Vector2()
        coords.x = randint(offset, self.screen.get_width() - offset)
        coords.y = randint(offset, self.screen.get_height() - offset)
        self.rect.center = coords

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Drop(pygame.sprite.Sprite):
    def __init__(self, drop_obj, start_pos, dest_pos):
        super().__init__()
        self.drop_obj = drop_obj # object reference
        self.drop_obj.rect.center = start_pos
        self.dest_pos = Vector2(dest_pos) # destination
        self.speed = 3

    def update(self):
        if self.drop_obj.group.has(self.drop_obj):  # Group method
        # if self.drop_obj in self.drop_obj.group:
            direction = self.dest_pos - self.drop_obj.rect.center

            if direction.length() <= self.speed:
                self.drop_obj.rect.center = self.dest_pos
                self.kill()
            else:
                direction.normalize_ip()
                self.drop_obj.rect.center += direction * self.speed
        else:
            self.kill()

class Drops():
    def __init__(self):
        self.bulletDrops = MyGroup()
        self.foodDrops = MyGroup()
        self.fallen_drops = MyGroup()

        self.screen = pygame.display.get_surface()
        # self.fallen_count = 0

    def createFallenDrop(self, start_pos):
        rand_drop = randint(0, 1)
        new_drop = None

        if rand_drop:
            new_drop = Food(self.foodDrops)
        else:
            new_drop = BulletDrop(self.bulletDrops)

        start_pos = Vector2(start_pos)
        dest_pos = Vector2()
        dest_pos.x = start_pos.x
        max_y = self.screen.get_height() - new_drop.rect.height//2

        if max_y > start_pos.y:
            dest_pos.y = randint(start_pos.y, max_y)
        else:
            dest_pos.y = start_pos.y

        self.fallen_drops.add(Drop(new_drop, start_pos, dest_pos))

        # self.fallen_count += 1
        # print(type(new_drop), " created ", self.fallen_count)

    def update(self):
        if self.fallen_drops:
            for drop in self.fallen_drops:
                drop.update()

    def draw(self, screen, colour):
        self.bulletDrops.draw(screen, colour)
        self.foodDrops.draw(screen, colour)

    def create_bulletDrop(self):
        new_bullet_drop = BulletDrop(self.bulletDrops)
        new_bullet_drop.set_random_coordinates()
        # self.bulletDrops.add(new_bullet_drop)

    def create_foodDrop(self):
        new_food = Food(self.foodDrops)
        new_food.check_random_coordinates()  # collide before add
        # self.foodDrops.add(new_food)

    def clear(self):
        self.bulletDrops.empty()
        self.foodDrops.empty()
        self.fallen_drops.empty()
