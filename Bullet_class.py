import pygame
import math

# Клас, що представляє кулю
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos: float, direction):
        super().__init__()
        self.image = pygame.image.load('img/bullet_new.png').convert_alpha()
        self.scale_image(25)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.speed = 5
        self.angle = 0
        self.velocity = (float, float)
        self.velocity_for_direction(direction)
        
    def scale_image(self, new_width):
        # new_width = 25
        original_width = self.image.get_width()
        original_height = self.image.get_height()
        new_height = int(original_height * (new_width / original_width))
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def velocity_for_direction(self, direction):
        # Зміна напрямку та кута повороту кулі
        if direction == "up":
            self.velocity = (0, -1)
            self.angle = 90 #0
        elif direction == "down":
            self.velocity = (0, 1)
            self.angle = 270 #180
        elif direction == "left":
            self.velocity = (-1, 0)
            self.angle = 180 #90
        elif direction == "right":
            self.velocity = (1, 0)
            self.angle = 0 #270

        self.rotate()

    def velocity_for_mouse(self, start_pos: float, target_pos: float):
        # Визначення вектора руху кулі для миші
        dx = dy = float
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        self.velocity = (dx / magnitude, dy / magnitude)

        # Визначення кута повороту зображення, згідно нового вектора руху
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image, angle)

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, screen):
        # Оновлення позиції кулі
        self.rect.x += self.velocity[0] * self.speed
        self.rect.y += self.velocity[1] * self.speed
        # self.rect = self.rect.move(self.velocity[0] * 5, self.velocity[1] * 5)

        # Перевірка, чи вийшла куля за межі екрану
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

    # def get_pos(self):
    #     return (self.rect.x, self.rect.y)
