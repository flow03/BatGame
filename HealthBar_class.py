import pygame
from pygame.math import Vector2

class HealthBar:
    def __init__(self, pos, width, height, border = 2):
        pos = Vector2(pos)
        self.rect = pygame.Rect(*pos, width, height)        
        self.bordered_rect = pygame.Rect(pos.x - border, pos.y - border, 
            width + border * 2, height + border * 2)
        # self.yellow_rect = pygame.Rect(self.rect)
        

        self.max_width = width
        self.border = border
        self.set_max_health(100)
        self.health = self.max_health

    def draw(self, screen):
        # pygame.draw.rect(screen, "Yellow", self.yellow_rect)
        pygame.draw.rect(screen, "Red", self.rect)
        pygame.draw.rect(screen, "Black", self.bordered_rect, self.border)

    def update_pos(self, pos):
        pos = Vector2(pos)
        self.rect.center = pos
        self.bordered_rect.center = pos

    def update_health(self, health):
        if health != self.health:
            self.health = round(health)
            # if self.health > self.max_health:
            #     self.health = self.max_health
            
            ratio = self.health/self.max_health
            self.rect.width = round(self.max_width * ratio)

    def set_max_health(self, max_health):
        self.max_health = round(max_health)

