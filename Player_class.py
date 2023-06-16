import pygame
import spritesheet
# from Jump_class import Jump

class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.rect = pygame.Rect((x, y), (60, 60))
        self.speed = 3
        self.direction = 'down'  # Початковий напрямок руху
        self.frame_index = 0  # Початковий індекс кадру
        self.animation_speed = 0.2  # Швидкість анімації (затримка між кадрами)
        self.animation_frames = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }
        self.sheet = spritesheet.SpriteSheet('img/sprite/hero_sprites.png')
        self.load_animation_frames()

    def load_animation_frames(self):
        # Завантажте всі кадри анімацій для кожного напрямку руху
        # for direction in self.animation_frames.keys():
        #     for i in range(8):
        #         frame = pygame.image.load(f'{direction}_{i}.png')  # Завантаження кадра з файлу
        #         self.animation_frames[direction].append(frame)
        self.animation_frames['down'] = self.sheet.get_anim(0)
        self.animation_frames['left'] = self.sheet.get_anim(1)
        self.animation_frames['right'] = self.sheet.get_anim(2)
        self.animation_frames['up'] = self.sheet.get_anim(3)

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frames[self.direction]):
            self.frame_index = 0

    def draw(self, screen):
        current_frame = self.animation_frames[self.direction][int(self.frame_index)]
        screen.blit(current_frame, self.rect)

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

    # def jump(self):
    #     self.jump_object = Jump()
    #     self.jump_object.active(self)
