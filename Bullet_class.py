import pygame
import math

# Клас, що представляє кулю
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos: float, target_pos: float):
        super().__init__()
        # self.image = pygame.Surface((10, 10))
        # self.image.fill(WHITE)
        self.image = pygame.image.load('img/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.velocity = (float, float)
        
        # Визначення вектора руху кулі
        dx = dy = float
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        # self.velocity = (dx / magnitude, dy / magnitude)

        if magnitude > 0:
            self.velocity = (dx / magnitude, dy / magnitude)
            angle = math.degrees(math.atan2(-dy, dx))
            self.image = pygame.transform.rotate(self.image, angle)
        

    def update(self, screen):
        # Оновлення позиції кулі
        self.rect.x += self.velocity[0] * 5
        self.rect.y += self.velocity[1] * 5

        # Перевірка, чи вийшла куля за межі екрану
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

    def get_pos(self):
        return (self.rect.x, self.rect.y)
