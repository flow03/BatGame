import pygame
from pygame.math import Vector2
import HealthBar

class AllHealthBars:
    def __init__(self, healthbar : HealthBar, shieldbar = None):
        self.healthbar = healthbar
        self.shieldbar = shieldbar
        self.align = 'center' # or 'left'
        # self.update_pos(self.healthbar.get_pos())

    def init(self):
        self.healthbar.init()
        if self.shieldbar:
            self.shieldbar.init()

    # healthbar pos as parameter
    def update_pos(self, health_pos):
        # if self.healthbar.get_pos() != Vector2(pos):
        self.healthbar.update_pos(health_pos)
        
        if self.shieldbar:
            shift = 10
            # print('align: ', self.align)
            if self.align == 'center':
                shield_pos = Vector2(self.healthbar.rect.center)
                shield_pos.y -= shift
                self.shieldbar.update_pos(shield_pos)
            elif self.align == 'left':
                shield_pos = Vector2(self.healthbar.rect.midleft)
                shield_pos.y -= shift
                self.shieldbar.update_pos_left(shield_pos)
    
    def update_health(self):
        self.healthbar.update_health()
        if self.shieldbar: # and not self.shieldbar.health.empty()
            self.shieldbar.update_health()

    def draw(self, screen):
        self.healthbar.draw(screen)
        if self.shieldbar:
            self.shieldbar.draw(screen)

    def set_damage(self, damage : int):
        if self.shieldbar: # and not self.shieldbar.empty()
            overdamage = self.shieldbar.set_damage(damage)
            if self.shieldbar.health.empty():
                self.shieldbar = None
            if overdamage:
                # print("overdamage is ", overdamage)
                self.healthbar.set_damage(overdamage)
        else:
            self.healthbar.set_damage(damage)

    def set_heal(self, heal : int):
        self.healthbar.set_heal(heal)

class BlueShield(HealthBar.CellHealthBar):
    def __init__(self, rect : pygame.Rect, health : HealthBar.Health, border = 1):
        super().__init__(rect, health, border, "Blue")
        self.visible_empty = False
        self.shifting = False
        self.decreased_cell = None
        # self.start_width = rect.width
        
        # self.change_colour("Blue")

    def set_damage(self, damage : int):
        self.decreased_cell = self.current_cell()
        return self.health.set_damage(1)
        
    def set_heal(self, heal : int):
        return self.health.set_heal(1)

    def draw(self, screen):
        for cell in self.cell_list:
            if self.visible_empty:
                cell.draw(screen)
            elif not cell.health.empty():
                cell.draw(screen)
            elif cell.is_decrease():
                cell.draw(screen)

    def update_health(self):
        super().update_health()
        if self.shifting and not self.visible_empty:
            if self.decreased_cell:
                if not self.decreased_cell.is_decrease():
                    self.decreased_cell = None
                    self.fit_rect(self.cell_visible_width()) # update_pos inside

    # def update_rect_pos(self, rect : pygame.Rect, y_shift):
    #     print('align: ', self.align)
    #     if self.align == 'center':
    #         shield_pos = Vector2(rect.center)
    #         shield_pos.y -= y_shift
    #         super().update_pos(shield_pos)
    #     elif self.align == 'left':
    #         shield_pos = Vector2(rect.midleft)
    #         shield_pos.y -= y_shift
    #         super().update_pos_left(shield_pos)

class GrayShield(HealthBar.HealthBar):
    def __init__(self, rect : pygame.Rect, health : HealthBar.Health, border = 1):
        super().__init__(rect, health, border, "Gray")
        # self.start_width = rect.width

    def update_health(self):
        super().update_health()
        if not self.health.empty():
            self.rect.width = self.rect_health.width + self.border * 2
        else:
            self.rect.width = 0

    def set_damage(self, damage : int):
        overdamage = self.health.set_damage(damage)
        return overdamage

    def set_heal(self, heal : int):
        pass

    # def update_rect_pos(self, rect : pygame.Rect, y_shift):
    #     shield_pos = Vector2(rect.midleft)
    #     shield_pos.y -= y_shift

    #     super().update_pos_left(shield_pos) # left
