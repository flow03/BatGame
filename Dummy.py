import pygame
from pygame.math import Vector2
from HealthBar import Health
import HealthBar
import add.Shields
from add.Path import resource_path
from add.Clock import Clock

class Dummy(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_list, health = 100, health_type = None):
        super().__init__()
        
        img_url = resource_path('img/training_dummy.png')
        self.image = pygame.image.load(img_url).convert_alpha()
        # self.resize_image(80)
        self.rect = self.image.get_rect(center=(x, y))
        self.bullet_list = bullet_list
        self.re_delay = Clock(1000)

        self.health = Health(health)
        self.healthBarCreate(health_type)
        # print("dummy ", self.health_bar.bordered_rect.width, self.health_bar.bordered_rect.height)

    def update_bar_pos(self):
        new_pos = Vector2(self.rect.midtop)
        new_pos.y -= 10
        self.health_bar.update_pos(new_pos)

    def healthBarCreate(self, health_type = None):
        health_bar_rect = pygame.Rect((0, 0), (100, 8)) # (0, 0) position

        if health_type == "cell":
            self.health_bar = HealthBar.CellHealthBar(health_bar_rect, self.health, 1)
        elif health_type == "blue":
            self.health_bar = add.Shields.BlueShield(health_bar_rect, self.health, 1)
        elif health_type == "gray":
            self.health_bar = add.Shields.GrayShield(health_bar_rect, self.health, 1)
        elif health_type == "fancy_gray":
            health_bar = HealthBar.FancyHealthBar(health_bar_rect, self.health, 1)
            shield_bar = add.Shields.GrayShield(health_bar_rect, Health(30), 1)
            self.health_bar = add.Shields.AllHealthBars(health_bar, shield_bar)
        elif health_type == "fancy_blue":
            health_bar = HealthBar.FancyHealthBar(health_bar_rect, self.health, 1)
            shield_bar = add.Shields.BlueShield(health_bar_rect, Health(5), 1)
            self.health_bar = add.Shields.AllHealthBars(health_bar, shield_bar)
        else:
            self.health_bar = HealthBar.FancyBoundHealthBar(health_bar_rect, self.health, 1)

        self.update_bar_pos()

    def init(self):
        self.health_bar.init()

    def update(self):
        self.collide_bullet()
        
        if self.re_delay.end():
            self.health.restore()

        self.health_bar.update_health()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.health_bar.draw(screen)

    def collide_bullet(self):
        if self.bullet_list:
            bullet = pygame.sprite.spritecollideany(self, self.bullet_list)
            if bullet:
                self.set_damage(bullet.damage)
                bullet.kill()

        # if self.bullet_list:
        #     for bullet in self.bullet_list:
        #         if self.rect.colliderect(bullet.rect):
        #             self.set_damage(bullet.damage)
        #             bullet.kill()

    def set_damage(self, damage):
        self.health_bar.set_damage(damage)
        if self.health.empty():
            self.re_delay.start()

    def set_heal(self, heal : int):
        self.health_bar.set_heal(heal)

    def resize_image(self, new_h):
        original_w = self.image.get_width()
        original_h = self.image.get_height()
        new_w = int(original_w * (new_h/original_h))
        # print(f"new_h: {new_h}, new_w: {new_w}")

        self.image = pygame.transform.scale(self.image, (new_w, new_h))
