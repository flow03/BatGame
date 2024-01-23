import pygame
from random import randint, uniform
import math
from pygame.math import Vector2
from add.Spritesheet import SpriteSheet
            
class Food(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()
        
        size = 30
        self.image = self.get_image(size)
        self.rect = self.image.get_rect()
        self.heal = randint(10, 20)
        self.group = group
        self.group.add(self)
        self.screen = pygame.display.get_surface()

    def get_image(self, size):
        sprite_sheet = SpriteSheet('img/spritesheets/food_spritesheet_30.png')
        col = randint(0, 9)
        row = randint(0, 9)
        image = sprite_sheet.get_image(size, size, col, row)
        # new_size = 30
        # self.image = pygame.transform.scale(self.image, (new_size, new_size))
        return image

    def set_circle_coordinates(self, center, radius, c_offset = 0):
        center = Vector2(center)
        coords = Vector2()
        angle = uniform(0, 2 * math.pi)
        # distance = math.sqrt(random.uniform(0, 1)) * radius
        distance = uniform(0, 1) * (radius - c_offset) + c_offset
        coords.x = center.x + distance * math.cos(angle)
        coords.y = center.y + distance * math.sin(angle)
        coords = round(coords)
        # print(coords)
        self.rect.center = coords

    def set_random_coordinates(self):
        offset = 30 # self.image.get_width()//2 + 10
        offset = self.rect.width
        # print("Food self.rect.width: ", self.rect.width)
        coords = Vector2()
        coords.x = randint(offset, self.screen.get_width() - offset)
        coords.y = randint(offset, self.screen.get_height() - offset)
        self.rect.center = coords
        # return (x, y)

    def check_random_coordinates(self):
        # exclude self collide
        if self.group.has(self):
            self.group.remove(self) 

        self.set_random_coordinates()
        count = 0
        while pygame.sprite.spritecollideany(self, self.group):
            self.set_random_coordinates()
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

class FoodCreator():
    def __init__(self):
        # self.others = []
        # self.meat = []
        # self.fish = []
        # self.crabs = []
        # self.mashrooms = []
        # self.cakes = []
        self.images = {
            'other' : [],
            'meat' : [],
            'fish' : [],
            'crab' : [],
            'mashroom' : [],
            'cake' : [],
        }
    
    def add_images(self, size):
        sprite_sheet = SpriteSheet('img/spritesheets/food_spritesheet_30.png')
        col = randint(0, 9)
        row = randint(0, 9)
        image = sprite_sheet.get_image(size, size, col, row)
        # new_size = 30
        # self.image = pygame.transform.scale(self.image, (new_size, new_size))
        return image
    
    def createFood(self):
        self.createMeat()
        self.createFish()
        self.createCrab()
        self.createMashroom()
        self.createCake()

    def createMeat(self):
        image = random(self.images['meat'])
        return Meat(group, image)

class Meat(Food):
    def __init__(self, group, image):
        super().__init__(group)

    def do(self):
        # meat stuff
        pass
