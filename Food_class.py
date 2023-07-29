import pygame
import random
import math
from pygame.math import Vector2
from Spritesheet_class import SpriteSheet

class Food(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        
        size = 30
        self.image = self.get_image(size)
        
        coords = self.get_random_coordinates(screen, size)
        # coords = self.get_circle_coordinates(
        #     (screen.get_width()//2, screen.get_height()//2), 100, 70)
        self.rect = self.image.get_rect(center=coords)

        self.heal = random.randint(10, 20)
   
    def get_image(self, size):
        sprite_sheet = SpriteSheet('img/spritesheets/food_spritesheet_30.png')
        col = random.randint(0, 9)
        row = random.randint(0, 9)
        image = sprite_sheet.get_image(size, size, col, row)
        # new_size = 30
        # self.image = pygame.transform.scale(self.image, (new_size, new_size))
        return image

    def get_circle_coordinates(self, center, radius, offset = 0):
        center = Vector2(center)
        coords = Vector2()
        angle = random.uniform(0, 2 * math.pi)
        # distance = math.sqrt(random.uniform(0, 1)) * radius
        distance = random.uniform(0, 1) * (radius - offset) + offset
        coords.x = center.x + distance * math.cos(angle)
        coords.y = center.y + distance * math.sin(angle)
        coords = round(coords)
        # print(coords)
        return coords

    def get_random_coordinates(self, screen, size):
        offset = size//2 + 10
        x = random.randint(offset, screen.get_width() - offset)
        y = random.randint(offset, screen.get_height() - offset)
        return (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)