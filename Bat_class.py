import pygame
import random

class Bat(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super().__init__()

        self.image = self.load_random_frame()
        bat_y = random.randint(0 + self.image.get_height(), 
        HEIGHT - self.image.get_height())
        self.rect = self.image.get_rect(midleft=(WIDTH, bat_y))
        self.speed = random.randint(3, 6)

  
    def load_random_frame(self):
        i = random.randint(0, 10)
        frame = pygame.image.load(f'img/bat/bat{i}.png')
        
        return frame

    def update(self, player):
        self.rect = self.rect.move(-self.speed, 0)

        if self.rect.colliderect(player.rect):
            player.gameplay = False

        if self.rect.right < 0:
            self.kill()

        # if self.rect.colliderect(player.rect):
        #     return False
        # else: 
        #     return True

    # Group ignores this method
    # def draw(self, screen):
    #     screen.blit(self.red_rect, self.rect)
    #     screen.blit(self.image, self.rect)
