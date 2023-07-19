import pygame
from pygame.math import Vector2
from Spritesheet_class import SpriteSheet

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
        self.max_health = 100

        self.init()

    def init(self):
        self.direction = 'down'  # Початковий напрямок руху
        # self.current_animation = self.direction
        self.frame_index = 0  # Початковий індекс кадру
        self.animation_speed = 0.2  # Швидкість анімації (затримка між кадрами)
        self.image = self.animation_frames[self.direction][int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.start_pos)

        self.health = self.max_health
        self.bullets_count = 5
        self.killedBats = 0
        self.gameplay = True

    def load_animation_frames(self):
        # Завантаження всіх кадрів анімацій для кожного напрямку руху
        # for direction in self.animation_frames.keys():
        #     for i in range(8):
        #         frame = pygame.image.load(f'{direction}_{i}.png')  # Завантаження кадра з файлу
        #         self.animation_frames[direction].append(frame)
        sprite_sheet = SpriteSheet('img/spritesheets/hero_spritesheet.png')
        self.animation_frames['down'] = sprite_sheet.get_anim(row = 0) # 60x60 as default
        self.animation_frames['left'] = sprite_sheet.get_anim(row = 1)
        self.animation_frames['right'] = sprite_sheet.get_anim(row = 2)
        self.animation_frames['up'] = sprite_sheet.get_anim(row = 3)

    def update(self, bulletDrops, foodDrops):
        if bulletDrops:
            sprite = pygame.sprite.spritecollideany(self, bulletDrops)
            if sprite:
                self.bullets_count += 1
                sprite.kill()
            # pygame.sprite.spritecollide(player, bulletDrops, True)

        if foodDrops:
            food = pygame.sprite.spritecollideany(self, foodDrops)
            if food:
                self.set_heal(food.heal)
                food.kill()

        # оновлення кадрів анімації
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frames[self.direction]):
            self.frame_index = 0
        self.image = self.animation_frames[self.direction][int(self.frame_index)]

    def draw(self, screen, colour = None):
        screen.blit(self.image, self.rect)
        if colour:
            pygame.draw.rect(screen, colour, self.rect, 2)

        self.draw_health(screen, Vector2(20, 15))

    def draw_health(self, screen, pos : Vector2):
        ratio = self.health/self.max_health
        width = 250
        height = 13
        border = 2
        pygame.draw.rect(screen, "Red", (*pos, round(width * ratio), height)) # pos unpacking
        bordered_rect = pygame.Rect(pos.x - border, pos.y - border, 
            width + border * 2, height + border * 2)

        pygame.draw.rect(screen, "Black", bordered_rect, border)
            
    def get_colour_rect(self, colour):
        colour_rect = pygame.Surface(self.rect.size)
        colour_rect.fill(colour)
        colour_rect.set_alpha(100)
        return colour_rect

    def move(self, direction):
        self.direction = direction

        if direction == 'down':
            self.rect.centery += self.speed
        elif direction == 'up':
            self.rect.centery += -self.speed
        elif direction == 'left':
            self.rect.centerx += -self.speed
        elif direction == 'right':
            self.rect.centerx += self.speed

    # def move(self, x, y):
    #     self.rect.update(x, y)

    # def get_frame(self):
    #     return self.animation_frames[self.direction][int(self.frame_index)]

    def set_damage(self, damage: int):
        self.health -= int(damage)
        if self.health <= 0:
            self.gameplay = False

    def set_heal(self, heal: int):
        self.health += int(heal)
        if self.health > self.max_health:
            self.health = self.max_health
