import pygame
from pygame.math import Vector2
from add.Spritesheet import SpriteSheet
from actors.Bullet import Bullet
import interface.HealthBar as HealthBar
import interface.Effects as Effects
import interface.Shields as Shields
from text.Jokes import JokeHandler

class Player:
    def __init__(self, position, game): # drops, groups.bullets
        self.animation_frames = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }
        self.load_animation_frames()
        self.start_pos = Vector2(position)
        self.speed = 4
        self.b_speed = 10   # bullet speed
        self.defence = 0
        # self.bullet_speed_bonus = 0
        self.effects = Effects.EffectQueue_draw(self)
        self.drops = game.drops
        self.joke = JokeHandler(game.jokes)
        self.events = game.events

        self.createHealth()
        
        self.init()

    def init(self):
        self.direction = 'down'  # Початковий напрямок руху
        self.current_animation = 'idle'
        self.frame_index = 0  # Початковий індекс кадру
        self.animation_speed = 0.2  # Швидкість анімації (кількість фреймів за один update)
        self.image = self.animation_frames[self.current_animation][int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.start_pos)
        self.velocity = Vector2(0)

        self.bullets_count = 32 # self.max_bullets_count
        # self.killedBats = 0
        # self.gameplay = True
        self.is_moving = False
        # self.onepunch = False
        self.add_damage = 0
        self.add_b_speed = 0
        self.add_speed = 0
        # self.harmless = False
        # self.standing = False
        self.effects.clear()
        self.joke.clear()

        self.health_bar.init() # restore
        self.bullet_bar.update(self.bullets_count)
        # self.health_bar.createBlueShield(4) # del after debug
        # self.health_bar.createGrayShield(50)
        # self.health_bar.set_damage(90)

    def createHealth(self):
        start_pos = Vector2(20, 30)

        # health_bar
        self.health = HealthBar.Health(100)
        health_bar_rect = pygame.Rect(start_pos, (258, 17)) # 254, 13
        health_bar_temp = HealthBar.FancyHealthBar(health_bar_rect, self.health, 2)
        self.health_bar = Shields.AllHealthBars(health_bar_temp)

        # bullet_bar
        start_pos.y += 17 + 5
        self.bullet_bar = HealthBar.BulletBar(start_pos, 254, 16) # 15+13+(2*2)

        # shield_bar
        # self.health_bar.createBlueShield(10)

    def add_effect(self, effect_key : str):
        self.effects.add(effect_key)

    def remove_effect(self, effect_key : str):
        self.effects.remove(effect_key)

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
            self.rect.center += round(self.velocity * (self.speed + self.add_speed))
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
                # self.health_bar.set_heal(food.heal)
                food.do(self)
                # self.health_bar.update_health()
                food.kill()

        self.health_bar.update_health()

        self.effects.update()

        if self.health.empty():
            self.events.create(self.events.EXIT)

        # if self.killedBats >= 10:
        #     self.events.create(self.events.TEN_BATS)

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

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # self.drawer.draw(self)
        # if colour:
        #     pygame.draw.rect(screen, colour, self.rect, 2)

        self.health_bar.draw(screen)
        self.bullet_bar.draw(screen)
        
        if self.effects:
            self.effects.draw(screen)  

        self.joke.draw_joke(self.rect.midtop)
            
    def get_colour_rect(self, colour):
        colour_rect = pygame.Surface(self.rect.size)
        colour_rect.fill(colour)
        colour_rect.set_alpha(100)
        return colour_rect

    def input(self):
        screen = pygame.display.get_surface()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a]) and self.rect.x > 0:
            self.move('left')
        if (keys[pygame.K_d]) and self.rect.x < (screen.get_width() - self.rect.width):
            self.move('right')
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
            self.move('up')
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y < (screen.get_height() - self.rect.height):
            self.move('down')

        # Player jump
        # if keys[pygame.K_SPACE]:
        #     jump.jump_start(player)
        # jump.jump_end(player)

    def move(self, direction):
        if not self.effects.get('stand'):
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

    def set_heal(self, heal: int):
        self.health_bar.set_heal(heal)

    def add_bullet(self, new_bullet : int):
        self.bullets_count += new_bullet
        if self.bullets_count < 0:
            self.bullets_count = 0
        # if self.bullets_count > self.max_bullets_count:
        #     self.bullets_count = self.max_bullets_count
        self.bullet_bar.update(self.bullets_count)

    # target is direction as default
    def shoot(self, bullet_group, target = None):
        if not self.effects.get('harmless'):
            if self.bullets_count > 0 or self.effects.get('onepunch'):
                new_bullet = Bullet(self.rect.center, self.b_speed)
                new_bullet.damage += self.add_damage
                new_bullet.speed += self.add_b_speed
                # print('add_b_speed: ', self.add_b_speed)

                # bullet_effect = self.effects.get('bullets')
                # if bullet_effect:
                #     new_bullet.speed += bullet_effect.bullet_speed_bonus

                # if self.onepunch:
                #     new_bullet.damage = 10000
                #     new_bullet.speed = 12
                    # print("onepunch bullet")

                if target:
                    new_bullet.velocity_by_mouse(target)
                else:
                    new_bullet.velocity_by_direction(self.direction)

                bullet_group.add(new_bullet)

                if not self.effects.get('onepunch'):
                    self.add_bullet(-1)

            # # if type(target) == str:
            # if isinstance(target, str):
            #     print("target is str")
            #     new_bullet.velocity_by_direction(target)
            # elif isinstance(target, tuple):
            #     print("target is tuple")
            #     new_bullet.velocity_by_mouse(target)
