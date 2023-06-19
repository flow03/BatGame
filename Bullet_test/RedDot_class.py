import pygame

class RedDot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 5
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, 'red', (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        

    def change_colour(self, colour = 'green'):
        # self.image.fill(colour)
        pygame.draw.circle(self.image, colour, (self.radius, self.radius), self.radius)

    # def check_collision(self, )
    # collided_objects = pygame.sprite.spritecollide(
    #     red_dot, circle_group, False, pygame.sprite.collide_circle)
    # if collided_objects:
    #     print("Collision detected!")