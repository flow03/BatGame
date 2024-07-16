import pygame
from random import randint #, uniform
# import math
from pygame.math import Vector2
# from add.Spritesheet import SpriteSheet
from loot.Food import FoodCreator
from actors.Groups import MyGroup
from add.Path import resource_path
from interface.Drawer import Drawer

class Drops():
    def __init__(self):
        self.bulletDrops = MyGroup()
        self.foodDrops = MyGroup()
        self.fallen_drops = MyGroup()

        self.foodCreator = FoodCreator()
        self.screen = pygame.display.get_surface()
        self.drawer = Drawer()
        # self.fallen_count = 0

    def createFallenDrop(self, start_pos):
        # rand_drop = randint(0, 1)
        new_drop = None

        if randint(0, 1): # 1
            new_drop = self.foodCreator.createFood()
            self.foodDrops.add(new_drop)
        else: # 0
            new_drop = BulletDrop()
            self.bulletDrops.add(new_drop)

        start_pos = Vector2(start_pos)
        dest_pos = Vector2()
        dest_pos.x = start_pos.x
        max_y = self.screen.get_height() - new_drop.rect.height//2

        if max_y > start_pos.y:
            # print(start_pos.y, max_y)
            dest_pos.y = randint(int(start_pos.y), max_y)
            # print("dest_pos.y", dest_pos)
            # dest_pos.y = int(uniform(start_pos.y, max_y))
        else:
            dest_pos.y = start_pos.y

        self.fallen_drops.add(FallenDrop(new_drop, start_pos, dest_pos))

        # self.fallen_count += 1
        # print(type(new_drop), " created ", self.fallen_count)

    def update(self):
        if self.fallen_drops:
            for drop in self.fallen_drops:
                drop.update()

    def draw(self):
        self.drawer.draw_group(self.bulletDrops)
        self.drawer.draw_group(self.foodDrops)
        # self.foodCreator.blit_dict()
        # self.foodCreator.blit_other()

    def create_bulletDrop(self):
        new_bullet = BulletDrop()
        self.bulletDrops.add(new_bullet)
        self.check_and_set_random_coords(new_bullet, self.bulletDrops)
        # self.set_random_coords(new_bullet)

    def add_food(self, food):
        self.foodDrops.add(food)
        self.check_and_set_random_coords(food, self.foodDrops)

    def create_foodDrop(self):
        new_food = self.foodCreator.createFood()
        self.add_food(new_food)

    def create_RedMushroom(self):
        new_food = self.foodCreator.createSomeFood('mushroom_red')
        self.add_food(new_food)
    
    def create_BlueMushroom(self):
        new_food = self.foodCreator.createSomeFood('mushroom_blue')
        self.add_food(new_food)

    def create_Mushrooms(self):
        new_food = self.foodCreator.createMushrooms()
        self.add_food(new_food)

    # creates food with specified coordinates
    def create_foodDrop_coords(self, coords : Vector2):
        new_food = self.foodCreator.createFood()
        self.foodDrops.add(new_food)
        new_food.rect.center = coords

    def clear(self):
        self.bulletDrops.empty()
        self.foodDrops.empty()
        self.fallen_drops.empty()

    def set_random_coords(self, obj):
        # offset = obj.rect.width
        coords = Vector2()
        coords.x = randint(obj.rect.width, self.screen.get_width() - obj.rect.width)
        coords.y = randint(obj.rect.height, self.screen.get_height() - obj.rect.height)
        obj.rect.center = coords

    def check_and_set_random_coords(self, obj, group : MyGroup):
        # exclude self collide
        if group.has(obj):
            group.remove(obj) 

        self.set_random_coords(obj)
        count = 0
        while pygame.sprite.spritecollideany(obj, group):
            self.set_random_coords(obj)
            count += 1
            if count >= 15:
                break
        
        group.add(obj)

        # if count:
        #     print(f"collisions: {count}")

    def check_and_set_circle_coords(self, obj, group, center, radius):
        # exclude self collide
        if group.has(obj):
            group.remove(obj)

        self.set_circle_coords(obj, center, radius)
        count = 0
        while pygame.sprite.spritecollideany(obj, group):
            self.set_circle_coords(obj, center, radius)
            count += 1
            if count >= 20:
                break

        group.add(obj)

        if count:
            print(f"Food circle collisions: {count}")


class BulletDrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img_url = resource_path('img/bullet.png')
        self.image = pygame.image.load(img_url).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 9))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        # self.group = group
        # self.group.add(self)
        self.screen = pygame.display.get_surface()

    def set_random_coordinates(self, offset = 30):
        coords = Vector2()
        coords.x = randint(offset, self.screen.get_width() - offset)
        coords.y = randint(offset, self.screen.get_height() - offset)
        self.rect.center = coords

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class FallenDrop(pygame.sprite.Sprite):
    def __init__(self, drop_obj, start_pos, dest_pos):
        super().__init__()
        self.drop_obj = drop_obj # object reference
        self.drop_obj.rect.center = start_pos
        self.dest_pos = Vector2(dest_pos) # destination
        self.speed = 3

    def update(self):
        if self.drop_obj.groups():  # groups Sprite method
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
