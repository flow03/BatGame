import pygame
import random
from Spritesheet_class import SpriteSheet

class Food(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        
        size = 30
        self.image = self.get_image(size)
        
        offset = size//2 + 10
        x = random.randint(offset, screen.get_width() - offset)
        y = random.randint(offset, screen.get_height() - offset)
        self.rect = self.image.get_rect(center=(x,y))

        self.heal = random.randint(10, 20)
   
    def get_image(self, size):
        sprite_sheet = SpriteSheet('img/spritesheets/food_spritesheet_30.png')
        col = random.randint(0, 9)
        row = random.randint(0, 9)
        image = sprite_sheet.get_image(size, size, col, row)
        # new_size = 30
        # self.image = pygame.transform.scale(self.image, (new_size, new_size))
        return image
