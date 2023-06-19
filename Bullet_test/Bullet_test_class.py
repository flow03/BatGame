import pygame
import math

# Клас, що представляє кулю
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos: float, target_pos: float):
        super().__init__()
        self.image = pygame.Surface((32, 12))
        # self.image.fill(WHITE)
        bullet_image = pygame.image.load('img/bullet.png').convert_alpha()
        self.image.blit(bullet_image, (0, 0), (0, 10, 32, 12))
        self.image.set_colorkey('Black')
        # self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.velocity = (float, float)
        self.speed = 8
        
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

        self.print(dx, dy, magnitude)
        

    def update(self, screen, circle_group):
        # Оновлення позиції кулі
        self.rect.x += self.velocity[0] * self.speed
        self.rect.y += self.velocity[1] * self.speed
        # self.rect = self.rect.move(self.velocity[0] * 5, self.velocity[1] * 5)
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
        return (self.rect.x, self.rect.y)

    def print(self, dx, dy, magnitude):
        print(f'dx {dx}')
        print(f'dy {dy}')
        print(f'magnitude {magnitude}')
        print(f'velocity {self.velocity}')