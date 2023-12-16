import pygame
from pygame.math import Vector2
import HealthBar

class AllHealthBars:
    def __init__(self, healthbar : HealthBar, shieldbar):
        self.healthbar = healthbar
        self.shieldbar = shieldbar
    
    # healthbar pos
    def update_pos(self, pos):
        self.healthbar.update_pos(pos)

        shield_pos = Vector2(self.healthbar.self.bordered_rect.topleft)
        shield_pos.y -= 10

        self.shieldbar.update_pos_left(shield_pos)
    
    def update_health(self):
        self.healthbar.update_health()
        self.shieldbar.update_health()
        

class BlueShield(HealthBar.CellHealthBar):
    def __init__(self, rect : pygame.Rect, health : HealthBar.Health, border = 1):
        super().__init__(rect, health, border, "Blue")
        
        # for cell in self.cell_list:
        #     cell.change_colour("Blue")
