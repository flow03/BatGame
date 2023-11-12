import pygame
import random
import math
from pygame.math import Vector2
from add.Spritesheet_class import SpriteSheet
from MyGroup_class import MyGroup
from Path import resource_path

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

    def set_random_coordinates(self, screen, offset = 30):
        coords = Vector2()
        coords.x = random.randint(offset, screen.get_width() - offset)
        coords.y = random.randint(offset, screen.get_height() - offset)
        self.rect.center = coords

    def draw(self, screen):
        screen.blit(self.image, self.rect)
            
class Food(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()
        
        size = 30
        self.image = self.get_image(size)
        self.rect = self.image.get_rect()
        self.heal = random.randint(10, 20)
        self.group = group
        self.group.add(self)

    def get_image(self, size):
        sprite_sheet = SpriteSheet('img/spritesheets/food_spritesheet_30.png')
        col = random.randint(0, 9)
        row = random.randint(0, 9)
        image = sprite_sheet.get_image(size, size, col, row)
        # new_size = 30
        # self.image = pygame.transform.scale(self.image, (new_size, new_size))
        return image

    def set_circle_coordinates(self, center, radius, c_offset = 0):
        center = Vector2(center)
        coords = Vector2()
        angle = random.uniform(0, 2 * math.pi)
        # distance = math.sqrt(random.uniform(0, 1)) * radius
        distance = random.uniform(0, 1) * (radius - c_offset) + c_offset
        coords.x = center.x + distance * math.cos(angle)
        coords.y = center.y + distance * math.sin(angle)
        coords = round(coords)
        # print(coords)
        self.rect.center = coords

    def set_random_coordinates(self, screen):
        offset = 30 # self.image.get_width()//2 + 10
        offset = self.rect.width
        # print("Food self.rect.width: ", self.rect.width)
        coords = Vector2()
        coords.x = random.randint(offset, screen.get_width() - offset)
        coords.y = random.randint(offset, screen.get_height() - offset)
        self.rect.center = coords
        # return (x, y)

    def check_random_coordinates(self, screen):
        # exclude self collide
        if self.group.has(self):
            self.group.remove(self) 

        self.set_random_coordinates(screen)
        count = 0
        while pygame.sprite.spritecollideany(self, self.group):
            self.set_random_coordinates(screen)
            count += 1
            if count >= 15:
                break
        
        self.group.add(self)

        # if count:
        #     print(f"Food coord_collisions: {count}")

    def check_circle_coordinates(self, center, radius, c_offset = 0):
        # exclude self collide
        if self.group.has(self):
            self.group.remove(self) 

        self.set_circle_coordinates(center, radius, c_offset)
        count = 0
        while pygame.sprite.spritecollideany(self, self.group):
            self.set_circle_coordinates(center, radius, c_offset)
            count += 1
            if count >= 20:
                break

        self.group.add(self)

        # if count:
        #     print(f"Food circle collisions: {count}")

    def draw(self, screen): # MyGroup required screen param
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
    def __init__(self, screen):
        self.bulletDrops = MyGroup()
        self.foodDrops = MyGroup()
        self.fallen_drops = MyGroup()

        self.screen = screen
        # self.fallen_count = 0

    def createFallenDrop(self, start_pos):
        rand_drop = random.randint(0, 1)
        new_drop = None

        if rand_drop:
            new_drop = Food(self.foodDrops)
        else:
            new_drop = BulletDrop(self.bulletDrops)

        start_pos = Vector2(start_pos)
        dest_pos = Vector2()
        dest_pos.x = start_pos.x
        dest_pos.y = random.randint(start_pos.y, self.screen.get_height() - new_drop.rect.width//2)
        
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
        new_bullet_drop.set_random_coordinates(self.screen)
        # self.bulletDrops.add(new_bullet_drop)

    def create_foodDrop(self):
        new_food = Food(self.foodDrops)
        new_food.check_random_coordinates(self.screen)  # collide before add
        # self.foodDrops.add(new_food)

    def empty(self):
        self.bulletDrops.empty()
        self.foodDrops.empty()
        self.fallen_drops.empty()
