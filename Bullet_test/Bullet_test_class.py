import pygame
import math
from pygame.math import Vector2

# Клас, що представляє кулю
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos: float, target_pos: float):
        super().__init__()
        self.image = pygame.image.load('img/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 9))
        self.rect = self.image.get_rect(center=start_pos)
        # self.rect.center = start_pos
        self.speed = 6
        self.position = Vector2(start_pos) # position stored in the Vector2 class

        self.set_direction(start_pos, target_pos)

    # Визначення вектора руху кулі 2
    def set_direction(self, start_pos, target_pos):
        
        start_pos = Vector2(start_pos)
        target_pos = Vector2(target_pos)

        self.distance = start_pos.distance_to(target_pos) # for debug
        # print(f"distance: {self.distance}")
        self.direction = target_pos - start_pos
        if self.direction:
            self.direction = self.direction.normalize()

        self.rotate(self.direction.x, self.direction.y)

    # Визначення вектора руху кулі 1
    def set_velocity(self, start_pos, target_pos):
        # self.velocity = (float, float)
       
        dx = dy = float
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        # self.velocity = (dx / magnitude, dy / magnitude)

        # if magnitude > 0:
        self.velocity = Vector2(dx / magnitude, dy / magnitude)

        self.rotate(dx, dy)

        # self.print(dx, dy, magnitude)

    def rotate(self, dx, dy):
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, screen, circle_group):
        # Оновлення позиції кулі
        self.position += self.direction * self.speed

        # self.rect.center = self.position
        self.rect.center = round(self.position)
        # self.rect.centerx = round(self.position.x)
        # self.rect.centery = round(self.position.y)

        # self.rect.centerx += self.direction.x * self.speed
        # self.rect.centery += self.direction.y * self.speed

        # Перевірка колізій з червоними цятками
        if circle_group:
            self.check_collision(circle_group)
        # Перевірка, чи вийшла куля за межі екрану
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

    def check_collision(self, circle_group):
        collided_objects = pygame.sprite.spritecollide(
            self, circle_group, False, pygame.sprite.collide_circle)
        # collided_objects.remove(self.rect)
        if collided_objects:
            for obj in collided_objects:
                obj.change_colour()

    def get_pos(self):
        return self.rect.center

    def print(self, dx, dy, magnitude):
        print(f'dx {dx}')
        print(f'dy {dy}')
        print(f'magnitude {magnitude}')
        print(f'velocity {self.velocity}')