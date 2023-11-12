import pygame
import math
from pygame.math import Vector2
from add.Path import resource_path

# Клас, що представляє кулю
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, start_pos):
        super().__init__()
        img_url = resource_path('img/bullet.png')
        self.image = pygame.image.load(img_url).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 9))
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 7
        self.damage = 25
        self.screen = screen
        # self.angle = 0
        # self.velocity_for_direction(direction)

        self.position = Vector2(start_pos) # position stored in the Vector2 class
        self.velocity = None

        # self.set_direction(start_pos, target_pos)
        
    def velocity_by_direction(self, direction):
        # Зміна напрямку та кута повороту кулі
        if direction == "up":
            self.velocity = Vector2(0, -1)
        elif direction == "down":
            self.velocity = Vector2(0, 1)
        elif direction == "left":
            self.velocity = Vector2(-1, 0)
        elif direction == "right":
            self.velocity = Vector2(1, 0)

        # angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x))
        # print(angle)
        self.rotate(*self.velocity)

        # self.image = pygame.transform.rotate(self.image, self.angle)
        # self.rect = self.image.get_rect(center=self.rect.center)

    # Визначення вектора руху кулі 
    def velocity_by_mouse(self, target_pos : Vector2):
        
        # start_pos = self.position
        target_pos = Vector2(target_pos)

        # self.distance = start_pos.distance_to(target_pos) # for debug
        # print(f"distance: {self.distance}")
        self.velocity = target_pos - self.position
        if self.velocity:
            self.velocity = self.velocity.normalize()

        self.rotate(self.velocity.x, self.velocity.y)

    def rotate(self, dx, dy):
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        # Оновлення позиції кулі
        if self.velocity:
            self.position += self.velocity * self.speed
            self.rect.center = round(self.position)

        # pygame.sprite.groupcollide(bullets, bat_list, True, True)
        # Параметр True вказує, що об'єкти, які зіткнулися,
        # мають бути автоматично видалені зі своїх відповідних груп.

        # Перевірка, чи вийшла куля за межі екрану
        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()

        # return isHit

    def draw(self, screen):
        screen.blit(self.image, self.rect)
