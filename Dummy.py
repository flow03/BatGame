import pygame
from pygame.math import Vector2
from HealthBar import Health
# from HealthBar import HealthBar
# from HealthBar import FancyHealthBar
from HealthBar import FancyBoundHealthBar
from Path import resource_path
from Clock_class import Clock

class Dummy(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_list):
        super().__init__()
        
        img_url = resource_path('img/training_dummy.png')
        self.image = pygame.image.load(img_url).convert_alpha()
        # self.resize_image(80)
        self.rect = self.image.get_rect(center=(x, y))

        self.bullet_list = bullet_list
        self.re_delay = Clock(600)

        self.health = Health(110)
        bar_pos = Vector2(self.rect.midtop)
        bar_pos.y -= 10
        health_bar_rect = pygame.Rect(bar_pos, (100, 6))
        self.health_bar = FancyBoundHealthBar(health_bar_rect, self.health, 1)
        self.health_bar.update_pos(bar_pos)

    def init(self):
        self.health_bar.init()

    def update(self):
        self.collide_bullet()
        
        if self.re_delay.end():
            self.health.reload()

        self.health_bar.update_health()

    def draw(self, screen, colour = None):
        screen.blit(self.image, self.rect)
        if colour:
            pygame.draw.rect(screen, colour, self.rect, 2)

        self.health_bar.draw(screen)

    def collide_bullet(self):
        # if self.bullet_list:
        #     for bullet in self.bullet_list:
        #         if self.rect.colliderect(bullet.rect):
        #             self.set_damage(bullet.damage)
        #             bullet.kill()

        if self.bullet_list:
            bullet = pygame.sprite.spritecollideany(self, self.bullet_list)
            if bullet:
                self.set_damage(bullet.damage)
                bullet.kill()

    def set_damage(self, damage):
        self.health.set_damage(damage)
        if self.health.empty():
            self.re_delay.start()

    def resize_image(self, new_h):
        original_w = self.image.get_width()
        original_h = self.image.get_height()
        new_w = int(original_w * (new_h/original_h))
        # print(f"new_h: {new_h}, new_w: {new_w}")

        self.image = pygame.transform.scale(self.image, (new_w, new_h))
