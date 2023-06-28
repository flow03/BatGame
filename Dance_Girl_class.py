import pygame
from Spritesheet_class import SpriteSheet

class Dance_Girl:
    def __init__(self, x, y):
        self.animations = {
            'balancing': [],
            'hips': [],
            'skip': [],
            'slide': [],
            'snap': []
        }
        self.load_animations()
        self.current_animation = 'slide'  # поточна анімація
        self.frame_index = 0  # поточний індекс кадру
        self.animation_speed = 0.18 # 0.2

        self.image = self.animations[self.current_animation][self.frame_index]
        
        self.start_x = x
        self.start_y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

        self.is_moving = False
        self.is_alive = True

    def load_animations(self):
        for animation_name in self.animations.keys():
            sprite_sheet = SpriteSheet(f'img/Dancing_Girl/{animation_name}.png')
            self.animations[animation_name] = sprite_sheet.get_anim(39, 53)

        self.resize_animations(63)

        self.animations['skip_left'] = self.animations.pop('skip')
        self.animations['skip_right'] = self.flip_list(self.animations['skip_left'])
    
    def flip_list(self, list):
        flipped_list = []
        for frame in list:
            flipped_frame = pygame.transform.flip(frame, True, False)
            flipped_list.append(flipped_frame)

        return flipped_list

    def resize_animations(self, new_y):
        original_x = 39
        original_y = 52
        # new_y = 65
        new_x = int(original_x * (new_y/original_y))
        print(new_x)

        for animation in self.animations.values():
            for i in range(len(animation)):
                animation[i] = pygame.transform.scale(animation[i], (new_x, new_y))

    def update(self):
        if self.is_alive:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animations[self.current_animation]):
                self.frame_index = 0

            self.image = self.animations[self.current_animation][int(self.frame_index)]

        # перевіряємо, чи персонаж закінчив рух
        if not self.is_moving and self.current_animation.startswith('skip'):
            self.current_animation = 'slide'
        
        self.is_moving = False  # скидаємо прапор руху після оновлення кадру

    def draw(self, screen, colour = None):
        # current_frame = self.animation_frames[self.direction][int(self.frame_index)]
        screen.blit(self.image, self.rect)
        if colour:
            pygame.draw.rect(screen, colour, self.rect, 2)

    def move(self, direction):
        
        # if direction == 'down':
        #     self.rect = self.rect.move(0, self.speed)
        # elif direction == 'up':
            # self.rect = self.rect.move(0, -self.speed)
        if direction == 'left':
            self.rect = self.rect.move(-self.speed, 0)
            self.current_animation = 'skip_left'
        elif direction == 'right':
            self.rect = self.rect.move(self.speed, 0)
            self.current_animation = 'skip_right'

        self.is_moving = True

    def reload(self):
        self.rect.update((self.start_x, self.start_y),(self.rect.width, self.rect.height))
        self.current_animation = 'slide'

    # def destroy(self):
    #     self.is_alive = False

    # def revive(self):
    #     self.is_alive = True
