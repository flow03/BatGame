import pygame
import math
import random
from pygame.math import Vector2
from Spritesheet_class import SpriteSheet

class Circle:
    def __init__(self):
        self.is_circle = False
        self.circle_radius = 80
        # self.circle_timer = 0
        self.angle = 0
        self.start_angle = 0
        self.laps_completed = 0
        self.completed_lap = False
        self.circle_start = True
        self.circle_direction = 1

    def move_around_point(self, rect, point, speed):
        character_pos = Vector2(rect.center)
        self.angle = math.atan2(character_pos.y - point.y, character_pos.x - point.x)
        if self.circle_start:
            self.start_angle = abs(self.angle)
            # self.laps_completed -= 1
            self.circle_start = False
        self.angle += (speed - 0.5) / self.circle_radius * self.circle_direction # 3 is speed
        rect.centerx = point.x + int(math.cos(self.angle) * self.circle_radius)
        rect.centery = point.y + int(math.sin(self.angle) * self.circle_radius)

        if not self.completed_lap and abs(self.angle) < self.start_angle:
            self.laps_completed += 1
            self.completed_lap = True
        elif self.completed_lap and abs(self.angle) >= self.start_angle:
            self.completed_lap = False

        if self.laps_completed == 3:
            self.circle_direction = -1
        # elif self.laps_completed >= 4:
        #     self.is_circle = False
            

    def reload(self):
        self.is_circle = False
        self.angle = 0
        self.start_angle = 0
        self.laps_completed = 0
        self.completed_lap = False
        self.circle_start = True

class Clock:
    def __init__(self, delay):
        self.nextFrame = self.clock() + delay
        self.dance_over = self.clock() + delay * 5
    
    def clock(self):
        return pygame.time.get_ticks()

    def isNextDance(self, delay):
        if (self.clock() > self.nextFrame):
            self.nextFrame += delay
            return True
        else:
            return False

    def isDanceOver(self):
        return self.clock() > self.dance_over

class Dance:
    def __init__(self):
        self.dance_delay = 2200
        self.danceList = ['hips','slide','snap']
        self.currentDance = 0

        self.dance_clock = Clock(self.dance_delay)

    def changeDance(self, player):
        if self.dance_clock.isNextDance(self.dance_delay):
            self.currentDance += 1
            player.idle_animation = self.danceList[self.currentDance % len(self.danceList)]

        player.current_animation = player.idle_animation

class Dance_Girl:
    def __init__(self, screen):
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
        self.image = self.animations[self.current_animation][int(self.frame_index)]
        
        # self.start_x = x
        # self.start_y = y
        self.screen = screen
        self.rect = self.image.get_rect()
        self.set_rand_pos(self.screen)
        self.speed = 3
        self.is_moving = False

        self.dance = None
        self.circle = Circle()

        self.state = "move_to_player"
        self.away_direction = None


    def load_animations(self):
        for animation_name in self.animations.keys():
            sprite_sheet = SpriteSheet(f'img/Dancing_Girl/{animation_name}.png')
            self.animations[animation_name] = sprite_sheet.get_anim(39, 53)

        self.add_moving_anims()

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
        # new_y = 65 # new_x = 44
        new_x = int(original_x * (new_y/original_y))

        for animation in self.animations.values():
            for i in range(len(animation)):
                animation[i] = pygame.transform.scale(animation[i], (new_x, new_y))

    def update(self, player):
        player_pos = Vector2(player.rect.center)
        character_pos = Vector2(self.rect.center)

        direction = (player_pos - character_pos).normalize()

        # Рух до гравця з-за меж екрану
        if self.state == "move_to_player":
            distance = character_pos.distance_to(player_pos)
            if distance > self.circle.circle_radius:
                self.move_to_point(direction)
                self.is_moving = True
                print("move_to_point")
            else:
                # self.circle.is_circle = True
                self.state = "move_around_player"
        # Рух по колу з центром в player.rect.center
        elif self.state == "move_around_player":
            # if self.circle.is_circle:
            if self.circle.laps_completed < 5:
                self.circle.move_around_point(self.rect, player_pos, self.speed)
                self.is_moving = True
                print("move_around_point")
            else:
                self.state = "dance"
        # Змінюємо танець
        elif self.state == "dance":
            if not self.dance:
                self.dance = Dance()
            if not self.dance.dance_clock.isDanceOver():
                if not self.is_moving:
                    self.dance.changeDance(self)
                    self.is_moving = False
                    print("dance")
            else:
                self.state = "move_away"
        elif self.state == "move_away":
            if not self.away_direction:
                self.away_direction = self.get_min_direction()
            self.move(self.away_direction)
            print("move_away")

        # Оновлюємо напрямок анімації руху
        self.update_direction(direction)

        # змінюємо танець
        # if not self.is_moving:
        #     self.dance.changeDance(self)

        # self.update_animations()

        # перевіряємо, чи персонаж закінчив рух
        # if not self.is_moving and (self.current_animation.startswith('skip') or self.current_animation.startswith('balancing')):
        #     self.current_animation = self.idle_animation
        self.is_moving = False  # скидаємо прапор руху після оновлення кадру
    
    def update_animations(self):
        # оновлення кадрів анімації
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.current_animation]):
            self.frame_index = 0
        self.image = self.animations[self.current_animation][int(self.frame_index)]    

    def draw(self, screen, colour = None):
        # current_frame = self.animation_frames[self.direction][int(self.frame_index)]

        self.update_animations()

        screen.blit(self.image, self.rect)
        if colour:
            pygame.draw.rect(screen, colour, self.rect, 2)

    def move(self, direction):
        if direction == 'down':
            self.rect.move_ip(0, self.speed)
        elif direction == 'up':
            self.rect.move_ip(0, -self.speed)
        elif direction == 'left':
            self.rect.move_ip(-self.speed, 0)
            self.current_animation = self.move_left_anim
        elif direction == 'right':
            self.rect.move_ip(self.speed, 0)
            self.current_animation = self.move_right_anim

        self.is_moving = True

    def reload(self):
        # self.rect.update((self.start_x, self.start_y),(self.rect.width, self.rect.height))
        self.set_rand_pos(self.screen)
        self.current_animation = self.idle_animation
        self.frame_index = 0
        self.is_moving = False
        self.circle.reload()
        self.state = "move_to_player"
        if self.dance:
            self.dance = None
        self.away_direction = None
        
    # def changeDance(self):
    #     if not self.is_moving:
    #         if self.dance.dance_clock.isNextDance(self.dance.dance_delay):
    #             self.dance.currentDance += 1
    #             self.idle_animation = self.dance.danceList[self.dance.currentDance % len(self.dance.danceList)]

    #         self.current_animation = self.idle_animation

    def move_to_point(self, direction):
        self.rect.centerx += direction.x * self.speed
        self.rect.centery += direction.y * self.speed


    def update_direction(self, direction):
        if self.is_moving:
            if direction.x < 0:
                self.current_animation = self.move_left_anim
            elif direction.x > 0:
                self.current_animation = self.move_right_anim

    def set_rand_pos(self, screen):
        new_x = random.randint(0, screen.get_width())
        new_y = random.randint(0, screen.get_height())
        # print(f'new_x: {new_x}')
        # print(f'new_y: {new_y}')
        out_x = [0 - (self.rect.width//2+1), screen.get_width() + (self.rect.width//2+1)]
        out_y = [0 - (self.rect.height//2+1), screen.get_height() + (self.rect.width//2+1)]
        selected_var = random.choice(['x', 'y'])
        if selected_var == 'x':
            # Випадково вибираємо елемент зі списку x_list і присвоюємо його змінній new_x
            new_x = random.choice(out_x)
        else:
            # Випадково вибираємо елемент зі списку y_list і присвоюємо його змінній new_y
            new_y = random.choice(out_y)

        self.rect.centerx = new_x
        self.rect.centery = new_y

        # print(f'out_x: {out_x}')
        # print(f'out_y: {out_y}')
        # print(f'x: {new_x}')
        # print(f'y: {new_y}')
        # print(f'rect.width: {self.rect.width}')
        # print(f'rect.height: {self.rect.height}')

    # Визначає напрям до найближчої межі екрану
    def get_min_direction(self):
        distances = {
            "left"  : self.rect.centerx,                               # Відстань до лівої межі
            "up"    : self.rect.centery,                               # Відстань до верхньої межі
            "right" : self.screen.get_width() - self.rect.centerx,     # Відстань до правої межі
            "down"  : self.screen.get_height() - self.rect.centery     # Відстань до нижньої межі
        }

        min_distance = min(distances.values())
        min_direction = None

        for key, value in distances.items():
            if value == min_distance:
                min_direction = key
                print(f"min_direction: {min_direction}")
                break
        
        return min_direction