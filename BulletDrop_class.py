import pygame

class BulletDrop(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('img/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 9))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=position)
        # self.rect.center = position
    

    # def update(self, screen):
    #     # Оновлення позиції кулі
    #     self.rect.x += self.velocity[0] * self.speed
    #     self.rect.y += self.velocity[1] * self.speed
        # self.rect = self.rect.move(self.velocity[0] * 5, self.velocity[1] * 5)

        # Перевірка, чи вийшла куля за межі екрану
        # if not screen.get_rect().colliderect(self.rect):
        #     self.kill()

