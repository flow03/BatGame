import pygame
from pygame.math import Vector2
import visuals.HealthBar as HealthBar
import visuals.Shields as Shields

class Actor(pygame.sprite.Sprite):
    def __init__():
        super().__init__()
        pass

    def createHealthBar(self, max_health):
        self.health = HealthBar.Health(max_health)

        health_bar_rect = pygame.Rect(self.rect.midtop, (self.rect.width, 7))
        health_bar_temp = HealthBar.FancyBoundHealthBar(health_bar_rect, self.health, 1)
        self.health_bar = Shields.AllHealthBars(health_bar_temp)

        # self.createShield()
        self.update_bar_pos()

    def update_bar_pos(self):
        new_pos = Vector2(self.rect.midtop)
        new_pos.y -= 10
        self.health_bar.update_pos(new_pos)