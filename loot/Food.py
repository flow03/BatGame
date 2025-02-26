import pygame
from random import randint, choice
# import math
# from pygame.math import Vector2
from add.Spritesheet import SpriteSheet, anim_blit

class FoodCreator():
    def __init__(self):
        # self.foodGroup = foodGroup
        self.images = {
            'other' : [],
            'meat' : [],
            'fish' : [],
            'crab' : [],
            'mushroom' : [],
            'mushroom_red' : [],
            'mushroom_blue' : [],
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
                if row == 4 and (col == 2 or col == 4 or col == 8):
                    self.images['mushroom_blue'].append(image)
                elif row == 4 and (col == 3 or col == 7):
                    self.images['mushroom_red'].append(image)
                elif row == 4:
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

    def get_rand_image(self, size = 30):
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

        y += 30
        return y

    def blit_other_new(self):
        screen = pygame.display.get_surface()
        other = self.images['other']
        max_count = (screen.get_width() - 20) // 30
        y = 70
        for i in range(len(other)):
            anim_blit(screen, other[i], 20, y)
            if i == max_count - 1:
                y += 30
                max_count *= 2
        y += 30
        return y

    def blit_dict(self):
        screen = pygame.display.get_surface()
        # anim_blit_dict(screen, self.images, 20, 70)
        y = self.blit_other_new()
        for key, images in self.images.items():
            if images and key != "other":
                anim_blit(screen, images, 20, y)

    def createFood_common(self):
        image = choice(self.images['other'])
        return Food(image)
        # new_food.check_random_coordinates()
        # self.foodGroup.add(new_food)

    # def createFood_test(self): # test
    #     # image = choice(self.images['mushroom']) 
    #     return self.createMushrooms()
        
    def createFood(self):
        key = choice(list(self.images.keys()))    # rand key
        return self.createSomeFood(key)

    def createSomeFood(self, key):
        if self.images.get(key, None) and self.images[key]: # not empty
            image = choice(self.images[key])
            if key == 'fish':
                return Fish(image)
            elif key == 'mushroom': # key.startswith('mushroom'): # str method
                return Mushroom(image)
            elif key == 'mushroom_red':
                return RedMushroom(image)
            elif key == 'mushroom_blue':
                return BlueMushroom(image)
            elif key == 'meat':
                return Meat(image)
            elif key == 'flour':
                return Flour(image)
            elif key == 'crab':
                return Crab(image)
            elif key == 'egg':
                return Egg(image)
            elif key == 'cake':
                return Cake(image)
            else:
                return Food(image)
        else:
            return None
        
    def createMushrooms(self):
        kind = randint(0, 2)
        if kind == 1:
            return self.createSomeFood('mushroom_red')
        elif kind == 2:
            return self.createSomeFood('mushroom_blue')
        else:
            return self.createSomeFood('mushroom')

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

class Meat(Food):
    def __init__(self, image):
        super().__init__(image)
        self.heal = 40

class Fish(Food):
    def __init__(self, image):
        super().__init__(image)
        self.heal = self.min_heal

    def do(self, actor):
        # actor.set_heal(self.min_heal)
        super().do(actor)
        actor.effects.add_effect('speed')

# 3, 7 - poison
# 2, 8 - non poison
class Mushroom(Food):
    def __init__(self, image):
        super().__init__(image)
        self.heal = self.min_heal

class RedMushroom(Mushroom):
    def __init__(self, image):
        super().__init__(image)

    def do(self, actor):
        actor.effects.add_effect('poison')
        # pass

class BlueMushroom(Mushroom):
    def __init__(self, image):
        super().__init__(image)

    def do(self, actor):
        super().do(actor) # heal
        actor.effects.remove_effect('poison')

class Flour(Food):
    def __init__(self, image):
        super().__init__(image)
        self.stand = randint(0, 1)

    def do(self, actor):
        super().do(actor)
        if self.stand:
            actor.effects.add_effect('stand')

class Crab(Food):
    def __init__(self, image):
        super().__init__(image)
        self.heal = self.min_heal
        self.shield = randint(20, 50)

    def do(self, actor):
        super().do(actor)
        actor.health_bar.createGrayShield(self.shield)

class Egg(Food):
    def __init__(self, image):
        super().__init__(image)
        self.heal = self.min_heal

    def do(self, actor):
        super().do(actor)
        actor.effects.add_effect("bullets")

class Cake(Food):
    def __init__(self, image):
        super().__init__(image)
        self.heal = self.min_heal

    def do(self, actor):
        super().do(actor)
        actor.add_bullet(32)
         