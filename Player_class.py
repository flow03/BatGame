import pygame
from pygame.math import Vector2
from Spritesheet_class import SpriteSheet
from HealthBar import FancyHealthBar
from HealthBar import FancyBoundHealthBar
from HealthBar import BulletBar
from HealthBar import Health
from Bullet_class import Bullet
import Effects

class Player:
    def __init__(self, x, y):
        self.animation_frames = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }
        self.load_animation_frames()
        self.start_pos = Vector2(x, y)
        self.speed = 3
        self.effects = Effects.EffectQueue(self)

        self.health_new = Health(100)
        # self.max_health = 100
        # self.max_bullets_count = 32
        # self.health_bar = FancyHealthBar((20, 15), 254, 13) # max_health is 100 as default
        self.health_bar = FancyBoundHealthBar(pygame.Rect((20, 15), (254, 13)), self.health_new, 1)
        self.bullet_bar = BulletBar((20, 32), 254, 16) # 15+13+(2*2)

        self.init()

    def init(self):
        self.direction = 'down'  # Початковий напрямок руху
        self.current_animation = 'idle'
        self.frame_index = 0  # Початковий індекс кадру
        self.animation_speed = 0.2  # Швидкість анімації (затримка між кадрами)
        self.image = self.animation_frames[self.current_animation][int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.start_pos)

        self.bullets_count = 32 # self.max_bullets_count
        self.killedBats = 0
        self.gameplay = True
        self.is_moving = False
        self.effects.clear()

        self.health_bar.init()
        self.bullet_bar.update(self.bullets_count)

    def poisoned(self):
        self.effects.add("poison")

    def speed_up(self):
        self.effects.add("speed")

    def load_animation_frames(self):
        # Завантаження всіх кадрів анімацій для кожного напрямку руху
        sprite_sheet = SpriteSheet('img/spritesheets/hero_spritesheet.png')
        self.animation_frames['down'] = sprite_sheet.get_anim(row = 0) # 60x60 as default
        self.animation_frames['left'] = sprite_sheet.get_anim(row = 1)
        self.animation_frames['right'] = sprite_sheet.get_anim(row = 2)
        self.animation_frames['up'] = sprite_sheet.get_anim(row = 3)
        idle_sheet = SpriteSheet('img/spritesheets/hero_idle.png')
        self.animation_frames['idle'] = idle_sheet.get_anim()

    def update(self, bulletDrops, foodDrops):
        if bulletDrops:
            sprite = pygame.sprite.spritecollideany(self, bulletDrops)
            if sprite:
                self.add_bullet(2)
                sprite.kill()
            # pygame.sprite.spritecollide(player, bulletDrops, True)

        if foodDrops:
            food = pygame.sprite.spritecollideany(self, foodDrops)
            if food:
                self.health_new.set_heal(food.heal)
                # self.health_bar.update_health()
                food.kill()

        self.health_bar.update_health()
        # self.bullet_bar.update(self.bullets_count)

        self.effects.update()
        # for effect in self.effects:
        #     effect.update()
        #     if effect.off():
        #         # self.effects.pop()
        #         self.effects.remove(effect)

        if self.health_new.empty():
            self.gameplay = False

        if not self.is_moving:
            self.current_animation = "idle"

        self.update_animations()
        
        self.is_moving = False

    def update_animations(self):
        # оновлення кадрів анімації
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frames[self.current_animation]):
            self.frame_index = 0
        self.image = self.animation_frames[self.current_animation][int(self.frame_index)]

    def draw(self, screen, colour = None):
        screen.blit(self.image, self.rect)
        if colour:
            pygame.draw.rect(screen, colour, self.rect, 2)

        self.health_bar.draw(screen)
        self.bullet_bar.draw(screen)
            
    def get_colour_rect(self, colour):
        colour_rect = pygame.Surface(self.rect.size)
        colour_rect.fill(colour)
        colour_rect.set_alpha(100)
        return colour_rect

    def move(self, direction):
        self.direction = direction
        self.current_animation = self.direction

        if direction == 'down':
            self.rect.centery += self.speed
        elif direction == 'up':
            self.rect.centery += -self.speed
        elif direction == 'left':
            self.rect.centerx += -self.speed
        elif direction == 'right':
            self.rect.centerx += self.speed

        self.is_moving = True

    def set_damage(self, damage: int):
        self.health_new.set_damage(damage)
            # self.gameplay = False

    def add_bullet(self, new_bullet : int):
        self.bullets_count += new_bullet
        if self.bullets_count < 0:
            self.bullets_count = 0
        # if self.bullets_count > self.max_bullets_count:
        #     self.bullets_count = self.max_bullets_count
        self.bullet_bar.update(self.bullets_count)

    # target is direction as default
    def shoot(self, bullet_group, target = None):
        if self.bullets_count > 0:
            new_bullet = Bullet(self.rect.center)
            if target:
                new_bullet.velocity_by_mouse(target)
            else:
                new_bullet.velocity_by_direction(self.direction)
            bullet_group.add(new_bullet)
            self.add_bullet(-1)

            # # if type(target) == str:
            # if isinstance(target, str):
            #     print("target is str")
            #     new_bullet.velocity_by_direction(target)
            # elif isinstance(target, tuple):
            #     print("target is tuple")
            #     new_bullet.velocity_by_mouse(target)
