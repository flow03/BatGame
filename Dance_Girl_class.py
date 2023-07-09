import pygame
from pygame.math import Vector2
import math
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
        # self.is_alive = True
        self.is_circle = False

        self.dance_delay = 2200
        self.nextFrame = self.clock() + self.dance_delay
        self.danceList = ['hips','slide','snap']
        self.currentDance = 0
        self.circle_radius = 80
        # self.circle_timer = 0
        self.laps_completed = 0
        self.angle = 0
        self.completed_lap = False


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
        if not self.is_moving:
            if self.isNextDance(self.dance_delay):
                self.currentDance += 1
                self.idle_animation = self.danceList[self.currentDance % len(self.danceList)]

            self.current_animation = self.idle_animation

    def add_moving_anims(self):
        self.resize_animations(60)

        self.animations['skip_left'] = self.animations.pop('skip')
        self.animations['skip_right'] = self.flip_list(self.animations['skip_left'])

        self.animations['balancing_left'] = self.animations.pop('balancing')
        self.animations['balancing_right'] = self.flip_list(self.animations['balancing_left'])

        self.move_left_anim = 'skip_left'
        self.move_right_anim = 'skip_right'


    def load_animations_from_sheet(self):
        sprite_sheet = SpriteSheet('img/Dancing_Girl/black_rgb_super.png')
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

    def update(self, player):
        player_pos = Vector2(player.rect.center)
        character_pos = Vector2(self.rect.center)

        distance = character_pos.distance_to(player_pos)
        direction = (player_pos - character_pos).normalize()

        if not self.is_circle and distance > self.circle_radius:
            self.move_to_point(direction)
        else:
            self.is_circle = True

        # Рух по колу з центром в player.rect.center
        if self.is_circle:
            self.move_around_point(player_pos)

        self.update_direction(direction)

        # оновлення кадрів анімації
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.current_animation]):
            self.frame_index = 0

        self.image = self.animations[self.current_animation][int(self.frame_index)]

        # змінюємо танець    
        self.changeDance()
        # перевіряємо, чи персонаж закінчив рух
        # if not self.is_moving and (self.current_animation.startswith('skip') or self.current_animation.startswith('balancing')):
        #     self.current_animation = self.idle_animation
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
            self.rect.move_ip(-self.speed, 0)
            self.current_animation = self.move_left_anim
        elif direction == 'right':
            self.rect.move_ip(self.speed, 0)
            self.current_animation = self.move_right_anim

        self.is_moving = True

    def reload(self):
        self.rect.update((self.start_x, self.start_y),(self.rect.width, self.rect.height))
        self.current_animation = self.idle_animation
        self.frame_index = 0
        self.angle = 0
        self.laps_completed = 0

        self.is_moving = False
        self.is_circle = False

    # def destroy(self):
    #     self.is_alive = False

    # def revive(self):
    #     self.is_alive = True

    def move_to_point(self, direction):
        
        self.rect.centerx += direction.x * self.speed
        self.rect.centery += direction.y * self.speed
        self.is_moving = True
        

    def update_direction(self, direction):
        if direction.x < 0:
            self.current_animation = self.move_left_anim
        elif direction.x > 0:
            self.current_animation = self.move_right_anim

    def move_around_point(self, player_pos):
        character_pos = Vector2(self.rect.center)
        # self.circle_timer += self.animation_speed
        self.angle = math.atan2(character_pos.y - player_pos.y, character_pos.x - player_pos.x)
        # self.angle += self.animation_speed * 0.15
        self.angle += (self.speed - 0.5) / self.circle_radius
        self.rect.centerx = player_pos.x + int(math.cos(self.angle) * self.circle_radius)
        self.rect.centery = player_pos.y + int(math.sin(self.angle) * self.circle_radius)
        # self.current_animation = self.idle_animation
        self.is_moving = True

        if not self.completed_lap and abs(self.angle) < 0.1:
            self.laps_completed += 1
            self.completed_lap = True
        elif self.completed_lap and abs(self.angle) >= 0.1:
            self.completed_lap = False
