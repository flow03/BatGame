# import pygame
import math
from pygame.math import Vector2
from Clock_class import Clock
from add.Drops_class import Food
from Dance_Girl_class import Dance_Girl

class Circle:
    def __init__(self):
        self.circle_radius = 80
        self.init()

    def init(self):
        self.is_circle = False
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

        if self.laps_completed == 2:
            self.circle_direction = -1
        elif self.laps_completed >= 4:
            self.is_circle = False

class Dance:
    def __init__(self):
        # self.dance_delay = 2200
        self.danceList = ['hips','slide','snap']
        self.d_clock = Clock(2200) # dance clock
        self.food_clock = Clock(500)
        self.dance_over = Clock(2200 * 4) # one time tick

        self.init()

    def init(self):
        self.currentDance = 0
        self.dance_over.start()
        self.d_clock.start()
        self.food_clock.start()

    def changeDance(self, girl):
        if self.d_clock.isNextFrame():
            self.currentDance += 1
            girl.idle_animation = self.danceList[self.currentDance % len(self.danceList)]

        girl.current_animation = girl.idle_animation

    def update(self, girl):
        self.changeDance(girl)
        if self.food_clock.isNextFrame():
            new_food = Food(girl.food_list)
            new_food.check_circle_coordinates(girl.rect.center, 70, 60)
            # girl.food_list.add(new_food)

    def isDanceOver(self):
        return self.dance_over.end()


class IState:
    def __init__(self, npc : Dance_Girl):
        self.npc = npc
        self.player_pos = Vector2(self.npc.player.rect.center)
        # self.circle = Circle()
        # self.dance = Dance()
        # self.dance = None
    
    def init(self):
        self.circle.init()

    def doState(self):
        return self

    def direction_by_player(self):
        # player_pos = Vector2(player_pos)
        character_pos = Vector2(self.npc.rect.center)

        direction = self.player_pos - character_pos
        if direction:   # not Zero
            direction = direction.normalize()

        return direction

class move_to_player(IState):
    def __init__(self, npc):
        super().__init__(npc)
    
    def doState(self):
        distance = Vector2(self.npc.rect.center).distance_to(self.player_pos)
        if distance > self.npc.circle.circle_radius:
            direction = self.direction_by_player(self.player_pos)
            self.npc.move_by_direction(direction)

            return self
        else:
            return move_around_player(self.npc)


class move_around_player(IState):
    def __init__(self, npc):
        super().__init__(npc)
        self.circle = Circle()
        self.npc.circle.is_circle = True
    
    def doState(self):
        if self.circle.is_circle:
            self.circle.move_around_point(self.npc.rect, self.player_pos, self.npc.speed)
            direction = self.direction_by_player(self.player_pos)
            self.npc.is_moving = True
            self.npc.update_direction(direction)
            # print("move_around_point")
            return self
        else:
            return dance(self.npc)

class dance(IState):
    def __init__(self, npc):
        super().__init__(npc)
        self.dance = Dance()
    
    def doState(self):
        # if not self.dance:
        #     self.dance = Dance()
        if not self.dance.isDanceOver():
            self.dance.update(self)
            self.is_moving = False
            # print("dance")
            return self
        else:
            # self.dance = None
            return move_away(self.npc)

class move_away(IState):
    def __init__(self, npc):
        super().__init__(npc)
        self.screen = self.npc.screen
        self.rect = self.npc.rect
        self.away_direction = self.get_min_direction()
    
    def doState(self):
        # if not self.away_direction:
        #     self.away_direction = self.get_min_direction()
        self.npc.move(self.away_direction)
        # Перевірка, чи вийшов персонаж за межі екрану
        if not self.screen.get_rect().colliderect(self.rect):
            self.npc.kill()

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
                # print(f"min_direction: {min_direction}")
                break
        # print(min_direction)
        return min_direction
