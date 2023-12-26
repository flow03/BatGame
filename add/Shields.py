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
        self.visible = False
        # self.change_colour("Blue")
    
    def set_damage(self, damage : int):
        self.cell_list[self.index].health.set_damage(1)
        if self.health.set_damage(1): # bounds check
            self.index -= 1
        
    def set_heal(self, heal : int):
        self.cell_list[self.index].health.set_heal(1)
        if self.health.set_heal(1): # bounds check
            self.index += 1 # warning

    def draw(self, screen):
        for cell in self.cell_list:
            if self.visible:
                cell.draw(screen)
            elif not cell.health.empty():
                cell.draw(screen)
            elif cell.decrease or cell.yellow_clock.nextFrame:
                cell.draw(screen)

class GrayShield(HealthBar.HealthBar):
    def __init__(self, rect : pygame.Rect, health : HealthBar.Health, border = 1):
        super().__init__(rect, health, border, "Gray")
        self.start_width = rect.width

    def update_health(self):
        super().update_health()
        if not self.health.empty():
            self.bordered_rect.width = self.rect.width + self.border * 2
        else:
            self.bordered_rect.width = 0

    def set_heal(self, heal : int):
        pass