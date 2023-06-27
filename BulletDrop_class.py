import pygame
import random

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
    

    # def update(self, screen):
        # Перевірка, чи вийшла куля за межі екрану
        # if not screen.get_rect().colliderect(self.rect):
        #     self.kill()

