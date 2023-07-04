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
        self.load_animations_from_sheet()
        self.idle_animation = 'snap'
        self.current_animation = self.idle_animation  # поточна анімація
        self.frame_index = 0  # поточний індекс кадру
        self.animation_speed = 0.18 # 0.2

        self.image = self.animations[self.current_animation][self.frame_index]
        
        self.start_x = x
        self.start_y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

        self.is_moving = False
        self.is_alive = True

        self.dance_delay = 2200
        self.nextFrame = self.clock() + self.dance_delay
        self.danceList = ['hips','slide','snap']
        self.currentDance = 0


    def load_animations(self):
        for animation_name in self.animations.keys():
            sprite_sheet = SpriteSheet(f'img/Dancing_Girl/{animation_name}.png')
            self.animations[animation_name] = sprite_sheet.get_anim(39, 53)

        self.add_moving_anims()

    def clock(self):
        return pygame.time.get_ticks()

    def isNextDance(self, delay):
        if (self.clock() > self.nextFrame):
            self.nextFrame += delay
            return True
        else:
            return False
    
    def changeDance(self):
        if self.isNextDance(self.dance_delay):
            self.currentDance +=1
            self.idle_animation = self.danceList[self.currentDance % len(self.danceList)]
            if not self.is_moving:
                self.current_animation = self.idle_animation

    def add_moving_anims(self):
        self.resize_animations(60)

        self.animations['skip_left'] = self.animations.pop('skip')
        self.animations['skip_right'] = self.flip_list(self.animations['skip_left'])

        self.animations['balancing_left'] = self.animations.pop('balancing')
        self.animations['balancing_right'] = self.flip_list(self.animations['balancing_left'])


    def load_animations_from_sheet(self):
        sprite_sheet = SpriteSheet('img/Dancing_Girl/black_rgb_super_2.png')
        i = 0
        for key in self.animations.keys():
            self.animations[key] = sprite_sheet.get_anim(39, 53, row = i)
            i += 1

        self.add_moving_anims()

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

        # змінюємо танець    
        self.changeDance()
        # перевіряємо, чи персонаж закінчив рух
        if not self.is_moving and (self.current_animation.startswith('skip') or self.current_animation.startswith('balancing')):
            self.current_animation = self.idle_animation
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
