import pygame
from random import randint, choice
import math
from pygame.math import Vector2
from add.Spritesheet import SpriteSheet, anim_blit, anim_blit_dict
            
class Food(pygame.sprite.Sprite):
    def __init__(self, image : pygame.Surface):
        super().__init__()
        self.image = image
        # size = 30
        # self.image = self.get_rand_image(size)
        self.rect = self.image.get_rect()
        self.min_heal = 5
        self.heal = randint(10, 25)
        self.screen = pygame.display.get_surface()

    def do(self, sprite : pygame.sprite.Sprite):
        sprite.set_heal(self.heal)
    
    def draw(self, screen): # MyGroup required screen param
        screen.blit(self.image, self.rect)

class FoodCreator():
    def __init__(self):
        # self.foodGroup = foodGroup
        self.images = {
            'other' : [],
            'meat' : [],
            'fish' : [],
            'crab' : [],
            'mushroom' : [],
            # 'mushroom_red' : [],
            # 'mushroom_blue' : [],
            'flour' : [],
            'cake' : [],
            'egg' : []
        }

        self.add_images()
    
    def add_images(self, size = 30):
        sprite_sheet = SpriteSheet('img/spritesheets/food_spritesheet_30.png')
        for row in range(10):
            for col in range(10):
                image = sprite_sheet.get_image(size, size, col, row)
                if row == 4:
                    self.images['mushroom'].append(image)
                elif row == 5 and (col == 1 or col == 2 or col == 4 or col == 6 or col == 9):
                    self.images['meat'].append(image)
                elif row == 5 and col == 5:
                    self.images['egg'].append(image)
                elif row == 6 and (col >= 2 and col <= 4):
                    self.images['crab'].append(image)
                elif row == 6:
                    self.images['fish'].append(image)
                elif row == 7 and (col == 2 or col == 3):
                    self.images['cake'].append(image)
                elif row == 7 and (col == 7 or col == 8):
                    self.images['crab'].append(image)
                elif row == 7:
                    self.images['flour'].append(image)
                elif row == 8 and col == 1:
                    self.images['mushroom'].append(image)
                elif row == 8 and col == 2:
                    self.images['cake'].append(image)
                elif row == 8 and (col == 4 or col == 6):
                    self.images['egg'].append(image)
                elif row == 8 and (col == 5 or col == 8):
                    self.images['flour'].append(image)
                elif row == 8 and col == 9:
                    self.images['meat'].append(image)
                elif row == 9 and (col == 0 or col == 8):
                    self.images['meat'].append(image)
                elif row == 9 and (col == 1 or col == 2 or col == 4):
                    self.images['flour'].append(image)
                elif row == 9 and (col == 3 or col == 6):
                    self.images['cake'].append(image)
                elif row == 9 and (col == 7):
                    self.images['fish'].append(image)
                else:
                    self.images['other'].append(image)

    def get_rand_image(self, size):
        sprite_sheet = SpriteSheet('img/spritesheets/food_spritesheet_30.png')
        col = randint(0, 9)
        row = randint(0, 9)
        image = sprite_sheet.get_image(size, size, col, row)
        # new_size = 30
        # self.image = pygame.transform.scale(self.image, (new_size, new_size))
        return image

    def blit_other(self):
        screen = pygame.display.get_surface()
        other = self.images['other']
        # frame_width = self.images['other'][0].get_width()
        max_count = (screen.get_width() - 20) // 30 # frame_width & frame_height
        # print('len(other) ', len(other))
        # print('max_count ', max_count)
        y = 70
        start_index = 0
        end_index = max_count
        while start_index < len(other):
            anim_blit(screen, other[start_index:end_index], 20, y) # slices
            start_index = end_index
            end_index += max_count
            y += 30 #frame_height

    def draw(self, screen):
        # screen = pygame.display.get_surface()
        anim_blit_dict(screen, self.images, 20, 70)
        # self.blit_other()

    def createFood(self):
        image = self.get_rand_image(30)
        return Food(image)
        # new_food.check_random_coordinates()
        # self.foodGroup.add(new_food)
        
    def createFood_new(self):
        rand_drop = randint(0, 1)
        new_drop = None
        # self.createOther()
        # self.createMeat()
        if rand_drop:
            new_drop = self.createFish()
        # self.createCrab()
        else:
            new_drop = self.createMushroom()
        # self.createCake()
        return new_drop

    def createMeat(self):
        image = choice(self.images['meat'])
        return Meat(image)

    def createFish(self):
        image = choice(self.images['fish'])
        return Fish(image)

    def createMushroom(self):
        image = choice(self.images['mushroom'])
        return Mushroom(image)

class Meat(Food):
    def __init__(self, image):
        super().__init__(image)
        self.heal = self.min_heal

    def do(self, actor):
        # meat stuff
        pass

class Fish(Food):
    def __init__(self, image):
        super().__init__(image)
        # self.heal = self.min_heal

    def do(self, actor):
        actor.set_heal(self.min_heal)
        actor.add_effect('speed')

class Mushroom(Food):
    def __init__(self, image):
        super().__init__(image)
        # self.heal = self.min_heal

    def do(self, actor):
        actor.add_effect('poison')
