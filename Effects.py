import pygame
# from HealthBar import Health
from HealthBar import HealthBar
from Clock_class import Clock

class PoisonEffect:
    def __init__(self, health_bar : HealthBar):
        self.healthBar = health_bar
        self.healthBar.change_colour("forestgreen")
        self.timer = Clock(900)
        self.timer.start()
        self.poison_damage = 2

    def update(self):
        if self.timer.isNextFrame():
            self.healthBar.health.set_damage(self.poison_damage)    

    def __del__(self):
        self.healthBar.change_colour("red")
