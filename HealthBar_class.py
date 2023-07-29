import pygame
from pygame.math import Vector2
from Clock_class import Clock

class HealthBar:
    def __init__(self, pos, width, height, border = 2):
        pos = Vector2(pos)
        self.rect = pygame.Rect(*pos, width, height)        
        self.bordered_rect = pygame.Rect(pos.x - border, pos.y - border, 
            width + border * 2, height + border * 2)

        self.max_width = width
        self.border = border
        self.set_max_health(100)
        self.health = self.max_health

        self.yellow_rect = pygame.Rect(self.rect)
        self.yellow_clock = Clock(500)
        self.green_rect = pygame.Rect(self.rect)
        self.green_clock = Clock(500)

    def init(self):
        self.rect.width = self.max_width
        self.green_rect.width = self.max_width
        self.yellow_rect.width = self.max_width

        self.anim_speed = 3
        self.decrease = False
        self.increase = False

    def draw(self, screen):
        pygame.draw.rect(screen, "Yellow", self.yellow_rect)
        pygame.draw.rect(screen, "Green", self.green_rect)
        pygame.draw.rect(screen, "Red", self.rect)
        pygame.draw.rect(screen, "Black", self.bordered_rect, self.border)

    def update_pos(self, pos):
        pos = Vector2(pos)
        self.bordered_rect.center = pos
        new_rect_pos = Vector2(self.bordered_rect.midleft)
        new_rect_pos.x += self.border
        self.rect.midleft = new_rect_pos

    def update_pos_fancy(self, pos):
        pos = Vector2(pos)
        self.bordered_rect.center = pos
        new_rect_pos = Vector2(self.bordered_rect.midleft)
        new_rect_pos.x += self.border
        self.rect.midleft = new_rect_pos

        self.green_rect.midleft = self.rect.midleft
        self.yellow_rect.midleft = self.rect.midleft


    def update_health(self, health):
        if health != self.health:
            # if health > self.max_health:
            #     health = self.max_health
            ratio = health/self.max_health

            if health < self.health:
                self.green_rect.width = round(self.max_width * ratio)
                self.rect.width = self.green_rect.width
                self.yellow_clock.start()
            elif health > self.health:
                self.green_rect.width = round(self.max_width * ratio)
                self.green_clock.start()

            self.health = round(health)

        if self.yellow_clock.end():
            self.decrease = True
        if self.decrease:
            self.yellow_decrease()

        if self.green_clock.end():
            self.increase = True
        if self.increase:
            self.red_increase()
        
        if not self.yellow_clock.nextFrame and not self.decrease:
            self.yellow_rect.width = self.green_rect.width
        if not self.green_clock.nextFrame and not self.increase:
            self.rect.width = self.green_rect.width

    def yellow_decrease(self):
        if self.yellow_rect.width > self.green_rect.width:
                self.yellow_rect.width -= self.anim_speed
        else:
            self.yellow_rect.width = self.green_rect.width
            self.decrease = False

    def red_increase(self):
        if self.rect.width < self.green_rect.width:
            self.rect.width += self.anim_speed
        else:
            self.rect.width = self.green_rect.width
            self.increase = False

    def update_health_common(self, health):
        if health != self.health:
            self.health = round(health)
            
            ratio = self.health/self.max_health
            self.rect.width = round(self.max_width * ratio)    

    def set_max_health(self, max_health):
        self.max_health = round(max_health)

class BulletBar:
    def __init__(self, pos, width, height):
        pos = Vector2(pos)
        self.rect = pygame.Rect(*pos, width, height)

        self.image = pygame.image.load('img/bullet.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.scale_image(height)
        self.bullets_image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
    
    def update(self, bullet_count):
        self.bullets_image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        position = Vector2(0, 0)
        width = self.image.get_width()
        for i in range(bullet_count):
            self.bullets_image.blit(self.image, position)
            position.x += width + 2
            if position.x > self.rect.width - width:
                break

    def draw(self, screen):
        # pygame.draw.rect(screen, "Red", self.rect, 2)
        screen.blit(self.bullets_image, self.rect)

    def scale_image(self, new_height):
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        new_width = int(original_width * (new_height / original_height))
        # print(new_width, new_height)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
