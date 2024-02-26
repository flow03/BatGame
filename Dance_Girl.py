import pygame
# import math
import random
from pygame.math import Vector2
from add.Spritesheet import SpriteSheet
# from Clock_class import Clock
# from add.MyGroup import MyGroup
from Drops import Drops
from visuals.HealthBar import Health
import add.State

class Dance_Girl(pygame.sprite.Sprite):
    def __init__(self, player, actors, drops : Drops):
        super().__init__()
        self.animations = {
            'balancing': [],
            'hips': [],
            'skip': [],
            'slide': [],
            'snap': []
        }
        self.load_animations_from_sheet()
        self.screen = pygame.display.get_surface()
        self.speed = 3
        self.health = Health(12)

        self.player = player
        self.actors = actors
        self.drops = drops
        
        self.init()

    def init(self):
        # animations
        self.idle_animation = 'snap'
        self.current_animation = self.idle_animation  # поточна анімація
        self.frame_index = 0  # поточний індекс кадру
        self.animation_speed = 0.18 # 0.2
        self.image = self.animations[self.current_animation][int(self.frame_index)]
        self.rect = self.image.get_rect()
        self.set_rand_pos() # rect
        
        self.live = True
        self.is_moving = False
        self.state = add.State.move_to_player(self)
        self.health.restore()

        # self.circle.init()
        # self.state.init()
        # self.dance.init()

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

        self.change_moving_anims('skip')

    def change_moving_anims(self, anim):
        if anim == 'skip' or anim == 'balancing':
            self.move_left_anim = anim + '_left'
            self.move_right_anim = anim + '_right'

    def load_animations_from_sheet(self):
        sprite_sheet = SpriteSheet('img/spritesheets/Dancing_Girl_spritesheet.png')
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

    def resize_animations(self, new_h):
        original_w = 39
        original_h = 52
        # new_y = 65 # new_x = 44
        new_w = int(original_w * (new_h/original_h))

        for animation in self.animations.values():
            for i in range(len(animation)):
                animation[i] = pygame.transform.scale(animation[i], (new_w, new_h))

    def update(self):
        self.state = self.state.doState()

        # Оновлюємо напрямок анімації руху
        # self.update_direction(direction)

        # змінюємо танець
        # if not self.is_moving:
        #     self.dance.changeDance(self)

        self.update_animations() # in draw method

        # перевіряємо, чи персонаж закінчив рух
        # if not self.is_moving and (self.current_animation.startswith('skip') or self.current_animation.startswith('balancing')):
        #     self.current_animation = self.idle_animation
        self.is_moving = False  # скидаємо прапор руху після оновлення кадру

        if not self.live:
            # for gc
            self.actors.remove("girl")
            # del self.actors["girl"]
            # self.__del__()
    
    def update_animations(self):
        # оновлення кадрів анімації
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.current_animation]):
            self.frame_index = 0
        self.image = self.animations[self.current_animation][int(self.frame_index)]    

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, direction : str):
        if direction == 'down':
            # self.rect.move_ip(0, self.speed)
            direction_vec = Vector2(0, 1)
        elif direction == 'up':
            # self.rect.move_ip(0, -self.speed)
            direction_vec = Vector2(0, -1)
        elif direction == 'left':
            # self.rect.move_ip(-self.speed, 0)
            # self.current_animation = self.move_left_anim
            direction_vec = Vector2(-1, 0)
        elif direction == 'right':
            # self.rect.move_ip(self.speed, 0)
            # self.current_animation = self.move_right_anim
            direction_vec = Vector2(1, 0)

        self.move_by_vector(direction_vec)

    def move_by_vector(self, direction : Vector2):
        self.rect.center += direction * self.speed
        self.is_moving = True
        # Оновлюємо напрямок анімації руху
        self.update_anim(direction)

    # єдина фунція, яка залежить від self.is_moving
    def update_anim(self, direction : Vector2):
        if self.is_moving:
            # move left
            if direction.x < 0:
                self.current_animation = self.move_left_anim
            # move right
            elif direction.x > 0:
                self.current_animation = self.move_right_anim
            elif direction.x == 0:
                # move up
                if direction.y < 0:
                    self.current_animation = self.move_left_anim
                # move down
                elif direction.y > 0:
                    self.current_animation = self.move_right_anim

    def set_rand_pos(self):
        new_x = random.randint(0, self.screen.get_width())
        new_y = random.randint(0, self.screen.get_height())
        # print(f'new_x: {new_x}')
        # print(f'new_y: {new_y}')
        out_x = [0 - (self.rect.width//2+1), self.screen.get_width() + (self.rect.width//2+1)]
        out_y = [0 - (self.rect.height//2+1), self.screen.get_height() + (self.rect.width//2+1)]
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
        