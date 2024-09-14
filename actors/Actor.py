import pygame
from pygame.math import Vector2
import interface.HealthBar as HealthBar
import interface.Shields as Shields
import interface.Effects as Effects

class Actor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.screen = pygame.display.get_surface()
        self.image = None # pygame.Surface()
        self.rect = None #self.image.get_rect()
        self.direction = Vector2()

        # self.default_speed = 0
        self.speed = 0
        self.damage = 0
        self.defence = 0
        self.bullets = 0

        self.health = None # HealthBar.Health(100)
        self.health_bar = None # self.createHealthBar() # self.health and self.rect needed
        # self.update_bar_pos()

    def update(self):
        # self.rect.center += round(self.direction * self.speed)
        if self.health_bar:
            self.update_bar_pos()
            self.health_bar.update_health()

    def createHealthBar(self):
        position = Vector2(self.rect.midtop)
        position.y -= 10
        health_bar_rect = pygame.Rect(position, (self.rect.width, 7))
        health_bar_temp = HealthBar.FancyBoundHealthBar(health_bar_rect, self.health, 1)
        health_bar = Shields.AllHealthBars(health_bar_temp)

        return health_bar

    def update_bar_pos(self):
        new_pos = Vector2(self.rect.midtop)
        new_pos.y -= 10
        self.health_bar.update_pos(new_pos)

    def defence_damage(self, damage):
        if self.defence < 100: # 100 percent
            damage = (1 - self.defence/100) * damage # 0/100 = 0
            damage = ((100 - self.defence)/100) * damage # 0/100 = 0
            # print(f"defence_damage: {damage}")
        return round(damage)

    def get_health(self):
        return self.health.health

    def set_damage(self, damage: int):
        damage = self.defence_damage(damage)
        self.health_bar.set_damage(damage)

    def set_heal(self, heal: int):
        self.health_bar.set_heal(heal)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.health_bar:
            self.health_bar.draw(screen)

    def add_bullet(self, new_bullet : int):
        self.bullets += new_bullet
        if self.bullets < 0:
            self.bullets = 0

    def direction_by_point(self, target_pos):
        target_pos = Vector2(target_pos)
        character_pos = Vector2(self.rect.center)

        direction = target_pos - character_pos
        if direction:   # not Zero
            direction = direction.normalize()

        return direction

# TODO ефекти мають бути в окремому класі, не в Actor
# об'єкт якого створюватиметься всередині потрібних класів
class ActorEffects(Actor):
    def __init__(self):
        super().__init__()
        
        self.effects = Effects.EffectQueue_draw(self)

        self.add_speed = 0
        self.add_damage = 0
        self.add_b_speed = 0

    def add_effect(self, effect_key : str):
        self.effects.add(effect_key)

    def remove_effect(self, effect_key : str):
        self.effects.remove(effect_key)

    def update(self):
        super().update()
        self.effects.update()

    def draw(self, screen):
        super().draw(screen)
        if self.effects:
            self.effects.draw(self.screen)
