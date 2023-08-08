import pygame
import random
import math
from pygame.math import Vector2
from Spritesheet_class import SpriteSheet
from Path import resource_path

class BulletDrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img_url = resource_path('img/bullet.png')
        self.image = pygame.image.load(img_url).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 9))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
    
    def set_random_coordinates(self, screen, offset = 30):
        coords = Vector2()
        coords.x = random.randint(offset, screen.get_width() - offset)
        coords.y = random.randint(offset, screen.get_height() - offset)
        self.rect.center = coords

    def draw(self, screen):
        screen.blit(self.image, self.rect)
            

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        size = 30
        self.image = self.get_image(size)
        self.rect = self.image.get_rect()
        self.heal = random.randint(10, 20)

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
        coords = Vector2()
        coords.x = random.randint(offset, screen.get_width() - offset)
        coords.y = random.randint(offset, screen.get_height() - offset)
        self.rect.center = coords
        # return (x, y)

    def check_random_coordinates(self, food_list, screen):
        self.set_random_coordinates(screen)
        count = 0
        while pygame.sprite.spritecollideany(self, food_list):
            self.set_random_coordinates(screen)
            count += 1
            if count >= 15:
                break

        # if count:
        #     print(f"coord_collisions: {count}")

    def check_circle_coordinates(self, food_list, center, radius, c_offset = 0):
        self.set_circle_coordinates(center, radius, c_offset)
        count = 0
        while pygame.sprite.spritecollideany(self, food_list):
            self.set_circle_coordinates(center, radius, c_offset)
            count += 1
            if count >= 20:
                break

        # if count:
        #     print(f"circle_coord_collisions: {count}")

    def draw(self, screen): # MyGroup required screen param
        screen.blit(self.image, self.rect)

class Drop(pygame.sprite.Sprite):
    def __init__(self, drop_obj, obj_group, start_pos, dest_pos):
        super().__init__()
        self.drop_obj = drop_obj # object reference
        self.obj_group = obj_group # object group reference
        self.drop_obj.rect.center = start_pos
        # self.position = Vector2(start_pos)
        self.dest_pos = Vector2(dest_pos) # destination
        self.speed = 3

    def update(self):
        if self.obj_group.has(self.drop_obj):
        # if self.drop_obj in self.obj_group:
            direction = self.dest_pos - self.drop_obj.rect.center

            if direction.length() <= self.speed:
                self.drop_obj.rect.center = self.dest_pos
                self.kill()
            else:
                direction.normalize_ip()
                self.drop_obj.rect.center += direction * self.speed
        else:
            self.kill()
