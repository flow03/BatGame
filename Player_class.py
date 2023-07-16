import pygame
from Spritesheet_class import SpriteSheet

class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        # self.rect = pygame.Rect((x, y), (60, 60))
        self.speed = 3
        self.bullets_count = 5
        self.killedBats = 0
        self.gameplay = True
        
        self.animation_frames = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }
        self.load_animation_frames()
        self.direction = 'down'  # Початковий напрямок руху
        # self.current_animation = self.direction
        self.frame_index = 0  # Початковий індекс кадру
        self.animation_speed = 0.2  # Швидкість анімації (затримка між кадрами)
        self.image = self.animation_frames[self.direction][int(self.frame_index)]
        self.rect = self.image.get_rect(center=(x,y))


    def load_animation_frames(self):
        # Завантаження всіх кадрів анімацій для кожного напрямку руху
        # for direction in self.animation_frames.keys():
        #     for i in range(8):
        #         frame = pygame.image.load(f'{direction}_{i}.png')  # Завантаження кадра з файлу
        #         self.animation_frames[direction].append(frame)
        sprite_sheet = SpriteSheet('img/hero_sprites/hero_spritesheet_black.png')
        self.animation_frames['down'] = sprite_sheet.get_anim(row = 0) # 60x60 as default
        self.animation_frames['left'] = sprite_sheet.get_anim(row = 1)
        self.animation_frames['right'] = sprite_sheet.get_anim(row = 2)
        self.animation_frames['up'] = sprite_sheet.get_anim(row = 3)

    def update(self, bulletDrops):
        if bulletDrops:
            sprite = pygame.sprite.spritecollideany(self, bulletDrops)
            if sprite:
                self.bullets_count += 1
                sprite.kill()

             
            # pygame.sprite.spritecollide(player, bulletDrops, True)

        # оновлення кадрів анімації
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frames[self.direction]):
            self.frame_index = 0
        self.image = self.animation_frames[self.direction][int(self.frame_index)]

    def draw(self, screen, colour = None):
        screen.blit(self.image, self.rect)
        if colour:
            pygame.draw.rect(screen, colour, self.rect, 2)
            
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

    def reload(self):
        self.rect.center = (self.start_x, self.start_y)
        self.direction = 'down'
        self.bullets_count = 5
        self.killedBats = 0
        self.gameplay = True

