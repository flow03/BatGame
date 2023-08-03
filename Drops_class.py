import pygame
import random
import math
from pygame.math import Vector2
from Spritesheet_class import SpriteSheet

class BulletDrop(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load('img/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 9))
        self.image = pygame.transform.rotate(self.image, 90)
       
        offset = 25
        x = random.randint(offset, screen.get_width() - offset)
        y = random.randint(offset, screen.get_height() - offset)

        self.rect = self.image.get_rect(center=(x,y))
        # self.rect.center = position
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
            

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.size = 30
        self.image = self.get_image(self.size)
        
        # coords = self.set_random_coordinates(screen)
        # coords = self.set_circle_coordinates(
        #     (screen.get_width()//2, screen.get_height()//2), 100, 70)
        # self.rect = self.image.get_rect(center=coords)

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
        self.rect = self.image.get_rect(center=coords)
        # return coords

    def set_random_coordinates(self, screen):
        offset = self.size//2 + 10
        coords = Vector2()
        coords.x = random.randint(offset, screen.get_width() - offset)
        coords.y = random.randint(offset, screen.get_height() - offset)
        self.rect = self.image.get_rect(center=coords)
        # return (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


