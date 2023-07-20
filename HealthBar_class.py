import pygame
from pygame.math import Vector2
from Clock_class import Clock

class HealthBar:
    def __init__(self, pos, width, height, border = 2):
        pos = Vector2(pos)
        self.rect = pygame.Rect(*pos, width, height)        
        self.bordered_rect = pygame.Rect(pos.x - border, pos.y - border, 
            width + border * 2, height + border * 2)

        self.max_width = width
        self.border = border
        self.set_max_health(100)
        self.health = self.max_health

        self.yellow_rect = pygame.Rect(self.rect)
        self.yellow_clock = None

    def draw(self, screen):
        pygame.draw.rect(screen, "Yellow", self.yellow_rect)
        pygame.draw.rect(screen, "Red", self.rect)
        pygame.draw.rect(screen, "Black", self.bordered_rect, self.border)

    def update_pos(self, pos):
        pos = Vector2(pos)
        self.rect.center = pos
        self.bordered_rect.center = pos

    def update_health(self, health):
        if health != self.health:
            # if health > self.max_health:
            #     health = self.max_health
            ratio = health/self.max_health
            self.rect.width = round(self.max_width * ratio)

            if health < self.health:
                self.clock_start()
            elif not self.yellow_clock:
                self.yellow_rect.width = self.rect.width

            self.health = round(health)

        self.clock_end()

    def set_max_health(self, max_health):
        self.max_health = round(max_health)

    def clock_start(self):
        self.yellow_clock = Clock(500)

    def clock_end(self):
        if self.yellow_clock:
            # print(self.yellow_clock.clock())
            if self.yellow_clock.isNextFrame():
                self.yellow_rect.width = self.rect.width
                self.yellow_clock = None

