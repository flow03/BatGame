import pygame
from Spritesheet_class import SpriteSheet

class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.rect = pygame.Rect((x, y), (60, 60))
        self.speed = 3
        
        self.animation_frames = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }
        self.load_animation_frames()
        self.direction = 'down'  # Початковий напрямок руху
        self.frame_index = 0  # Початковий індекс кадру
        self.animation_speed = 0.2  # Швидкість анімації (затримка між кадрами)


    def load_animation_frames(self):
        # Завантаження всіх кадрів анімацій для кожного напрямку руху
        # for direction in self.animation_frames.keys():
        #     for i in range(8):
        #         frame = pygame.image.load(f'{direction}_{i}.png')  # Завантаження кадра з файлу
        #         self.animation_frames[direction].append(frame)
        sprite_sheet = SpriteSheet('img/hero_sprites/hero_spritesheet_black.png')
        self.animation_frames['down'] = sprite_sheet.get_anim(row = 0) # 60x60 as defaultt
        self.animation_frames['left'] = sprite_sheet.get_anim(row = 1)
        self.animation_frames['right'] = sprite_sheet.get_anim(row = 2)
        self.animation_frames['up'] = sprite_sheet.get_anim(row = 3)

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frames[self.direction]):
            self.frame_index = 0

    def draw(self, screen, colour = None):
        current_frame = self.animation_frames[self.direction][int(self.frame_index)]
        # if colour:
        #     colour_rect = self.get_colour_rect(colour)
        #     screen.blit(colour_rect, self.rect)
        screen.blit(current_frame, self.rect)
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
            self.rect = self.rect.move(0, self.speed)
        elif direction == 'up':
            self.rect = self.rect.move(0, -self.speed)
        elif direction == 'left':
            self.rect = self.rect.move(-self.speed, 0)
        elif direction == 'right':
            self.rect = self.rect.move(self.speed, 0)

    # def move(self, x, y):
    #     self.rect.update(x, y)

    # def get_frame(self):
    #     return self.animation_frames[self.direction][int(self.frame_index)]

    def reload(self):
        self.rect.update((self.start_x, self.start_y),(self.rect.width, self.rect.height))
        self.direction = 'down'

