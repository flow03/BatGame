import pygame
from pygame.math import Vector2
from interface.HealthBar import Health
import interface.HealthBar as HealthBar
import interface.Shields as Shields
from add.Path import resource_path
from add.Clock import Clock

class Dummy(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_list, health_type = None, health = 100, shield = 0):
        super().__init__()
        
        self.health_type = health_type
        img_url = resource_path('img/training_dummy.png')
        self.image = pygame.image.load(img_url).convert_alpha()
        # self.resize_image(80)
        self.rect = self.image.get_rect(center=(x, y))
        self.bullet_list = bullet_list
        self.re_delay = Clock(1000)

        self.health = Health(health)
        self.shield = None
        if shield:
            self.shield = Health(shield)

        self.healthBarCreate(self.health_type)
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
            self.health_bar = Shields.BlueShield(health_bar_rect, self.health, 1)
            self.health_bar.shifting = True
        elif health_type == "gray":
            self.health_bar = Shields.GrayShield(health_bar_rect, self.health, 1)
        elif health_type == "fancy_gray":
            health_bar = HealthBar.FancyHealthBar(health_bar_rect, self.health, 1)
            shield_bar = Shields.GrayShield(health_bar_rect, self.shield, 1)
            self.health_bar = Shields.AllHealthBars(health_bar, shield_bar)
        elif health_type == "fancy_blue":
            health_bar = HealthBar.FancyHealthBar(health_bar_rect, self.health, 1)
            shield_bar = Shields.BlueShield(health_bar_rect, self.shield, 1)
            self.health_bar = Shields.AllHealthBars(health_bar, shield_bar)
        else:
            self.health_bar = HealthBar.FancyBoundHealthBar(health_bar_rect, self.health, 1)

        self.update_bar_pos()

    def init(self):
        # self.health_bar.init()
        self.healthBarCreate(self.health_type)

    def update(self):
        self.collide_bullet()
        
        if self.re_delay.end():
            self.health.restore()
            if self.shield:
                self.shield.restore()
            self.healthBarCreate(self.health_type)

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

class DummyCreator():
    def __init__(self, groups):
        self.groups = groups
        self.is_dummies = False
        screen = pygame.display.get_surface()
        self.center = Vector2(screen.get_size())//2

    def create(self):
        if self.is_dummies:
            self.createDummies()

    def createDummies(self):
        pos = Vector2(self.center.x - 200, self.center.y)
        left_dummy = Dummy(pos, self.groups.bullets,"fancy_blue", 50, 5)
        pos = Vector2(self.center.x + 200, self.center.y)
        right_dummy = Dummy(pos, self.groups.bullets, "fancy_gray", 50, 30)
        pos = Vector2(self.center.x - 200, self.center.y - 200)
        topleft_dummy = Dummy(pos, self.groups.bullets,"blue", 3)
        pos = Vector2(self.center.x + 200, self.center.y - 200)
        topright_dummy = Dummy(pos, self.groups.bullets, "gray", 50)
        pos = Vector2(self.center.x, self.center.y + 200)
        down_dummy = Dummy(pos, self.groups.bullets, "cell", 15)

        self.groups.dummies.add_actor("left_dummy", left_dummy)
        self.groups.dummies.add_actor("right_dummy", right_dummy)
        self.groups.dummies.add_actor("topleft_dummy", topleft_dummy)
        self.groups.dummies.add_actor("topright_dummy", topright_dummy)
        self.groups.dummies.add_actor("down_dummy", down_dummy)

    def deleteDummies(self):
        self.groups.dummies.clear()

    def switchDummies(self):
        if self.is_dummies:
            self.deleteDummies()
            self.is_dummies = False
        else:
            self.createDummies()
            self.is_dummies = True
