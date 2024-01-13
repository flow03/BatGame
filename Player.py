import pygame
from pygame.math import Vector2
from add.Spritesheet import SpriteSheet
import HealthBar
from Bullet import Bullet
import Effects
import add.Shields as Shields

class Player:
    def __init__(self, x, y, drops):
        self.animation_frames = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }
        self.load_animation_frames()
        self.start_pos = Vector2(x, y)
        self.speed = 4
        self.defence = 0
        self.effects = Effects.EffectQueue_draw(self)
        self.drops = drops

        self.createHealth()
        

        self.init()

    def init(self):
        self.direction = 'down'  # Початковий напрямок руху
        self.current_animation = 'idle'
        self.frame_index = 0  # Початковий індекс кадру
        self.animation_speed = 0.2  # Швидкість анімації (кількість фреймів за один update)
        self.image = self.animation_frames[self.current_animation][int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.start_pos)
        self.velocity = Vector2(0,0)

        self.bullets_count = 32 # self.max_bullets_count
        self.killedBats = 0
        self.gameplay = True
        self.is_moving = False
        self.onepunch = False
        self.effects.clear()

        self.health_bar.init()
        self.bullet_bar.update(self.bullets_count)

    def createHealth(self):
        start_pos = Vector2(20, 30)

        # health_bar
        self.health = HealthBar.Health(100)
        health_bar_rect = pygame.Rect(start_pos, (258, 17)) # 254, 13
        health_bar_temp = HealthBar.HealthBar(health_bar_rect, self.health, 2)
        self.health_bar = Shields.AllHealthBars(health_bar_temp)

        # bullet_bar
        start_pos.y += 17 + 5
        self.bullet_bar = HealthBar.BulletBar(start_pos, 254, 16) # 15+13+(2*2)

        # shield_bar
        shield_height = 8
        shield_width = health_bar_rect.width/2 # /5 * 5
        start_pos = Vector2(health_bar_rect.topleft)
        start_pos.x += 2
        start_pos.y -= 5 + shield_height
        shield = HealthBar.Health(5)
        shield_bar_rect = pygame.Rect(start_pos, (shield_width, shield_height))
        shield_bar_temp = Shields.BlueShield(shield_bar_rect, shield, 1)
        shield_bar_temp.align = 'left'
        self.health_bar.shieldbar = shield_bar_temp

    def add_effect(self, effect_key : str):
        self.effects.add(effect_key)

    # def speed_up(self):
    #     self.effects.add("speed")

    def load_animation_frames(self):
        # Завантаження всіх кадрів анімацій для кожного напрямку руху
        sprite_sheet = SpriteSheet('img/spritesheets/hero_spritesheet.png')
        self.animation_frames['down'] = sprite_sheet.get_anim(row = 0) # 60x60 as default
        self.animation_frames['left'] = sprite_sheet.get_anim(row = 1)
        self.animation_frames['right'] = sprite_sheet.get_anim(row = 2)
        self.animation_frames['up'] = sprite_sheet.get_anim(row = 3)
        idle_sheet = SpriteSheet('img/spritesheets/hero_idle.png')
        self.animation_frames['idle'] = idle_sheet.get_anim()

    def update(self):
        # moving
        if self.is_moving and self.velocity:
            self.rect.center += self.velocity * self.speed
            self.velocity = Vector2(0,0)
            # print()

        if self.drops.bulletDrops:
            sprite = pygame.sprite.spritecollideany(self, self.drops.bulletDrops)
            if sprite:
                self.add_bullet(2)
                sprite.kill()
            # pygame.sprite.spritecollide(player, bulletDrops, True)

        if self.drops.foodDrops:
            food = pygame.sprite.spritecollideany(self, self.drops.foodDrops)
            if food:
                self.health.set_heal(food.heal)
                # self.health_bar.update_health()
                food.kill()

        self.health_bar.update_health()

        self.effects.update()

        if self.health.empty():
            self.gameplay = False

        self.update_animations()
        
    # оновлення кадрів анімації
    def update_animations(self):
        if not self.is_moving:
            self.current_animation = "idle"

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frames[self.current_animation]):
            self.frame_index = 0
        self.image = self.animation_frames[self.current_animation][int(self.frame_index)]

        self.is_moving = False

    def draw(self, screen, colour = None):
        screen.blit(self.image, self.rect)
        if colour:
            pygame.draw.rect(screen, colour, self.rect, 2)

        self.health_bar.draw(screen)
        self.bullet_bar.draw(screen)
        
        if self.effects:
            self.effects.draw(screen)    
            
    def get_colour_rect(self, colour):
        colour_rect = pygame.Surface(self.rect.size)
        colour_rect.fill(colour)
        colour_rect.set_alpha(100)
        return colour_rect

    # def move(self, direction):
    #     self.direction = direction
    #     self.current_animation = self.direction

    #     if direction == 'down':
    #         self.rect.centery += self.speed
    #     elif direction == 'up':
    #         self.rect.centery += -self.speed
    #     elif direction == 'left':
    #         self.rect.centerx += -self.speed
    #     elif direction == 'right':
    #         self.rect.centerx += self.speed

    #     self.is_moving = True

    def move(self, direction):
        self.direction = direction
        self.current_animation = self.direction

        if direction == 'down':
            self.velocity.y = 1
        elif direction == 'up':
            self.velocity.y = -1
        elif direction == 'right':
            self.velocity.x = 1
        elif direction == 'left':
            self.velocity.x = -1

        # normalize diagonal moving (not Null)
        if self.velocity.x and self.velocity.y:
            self.velocity.normalize_ip()

        # move
        # self.rect.center += direction_vec * self.speed
        self.is_moving = True

        # print("direction: ", self.direction)
        # print("velocity: ",self.velocity)

    def defence_damage(self, damage):
        if self.defence < 100: # 100 percent
            damage = (1 - self.defence/100) * damage # 0/100 = 0
            damage = ((100 - self.defence)/100) * damage # 0/100 = 0
            # print(f"defence_damage: {damage}")
        return round(damage)

    def set_damage(self, damage: int):
        damage = self.defence_damage(damage)
        self.health_bar.set_damage(damage)

    def add_bullet(self, new_bullet : int):
        self.bullets_count += new_bullet
        if self.bullets_count < 0:
            self.bullets_count = 0
        # if self.bullets_count > self.max_bullets_count:
        #     self.bullets_count = self.max_bullets_count
        self.bullet_bar.update(self.bullets_count)

    # target is direction as default
    def shoot(self, screen, bullet_group, target = None):
        if self.bullets_count > 0 or self.onepunch:
            new_bullet = Bullet(screen, self.rect.center)
            if self.onepunch:
                new_bullet.damage = 10000
                new_bullet.speed = 11
                # print("onepunch bullet")

            if target:
                new_bullet.velocity_by_mouse(target)
            else:
                new_bullet.velocity_by_direction(self.direction)

            bullet_group.add(new_bullet)

            if not self.onepunch:
                self.add_bullet(-1)

            # # if type(target) == str:
            # if isinstance(target, str):
            #     print("target is str")
            #     new_bullet.velocity_by_direction(target)
            # elif isinstance(target, tuple):
            #     print("target is tuple")
            #     new_bullet.velocity_by_mouse(target)
