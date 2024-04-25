import pygame
from actors.Groups import MyGroup

class Drawer():
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.displayText = False

    def draw(self, group : MyGroup):
        if not self.displayText:
            self.draw_common(group)
        else:
            self.draw_rect(group)

    def draw_common(self, group : MyGroup):
        sprites = group.sprites()
        if sprites:
            for sprite in sprites:
                sprite.draw(self.screen)

    def draw_rect(self, group : MyGroup):
        sprites = group.sprites()
        if sprites:
            colour = "Red"
            for sprite in sprites:
                sprite.draw(self.screen)
                pygame.draw.rect(self.screen, colour, sprite.rect, 2)

    def draw_alpha(self, group : MyGroup):
        sprites = group.sprites()
        if sprites:
            colour = "Red"
            for sprite in sprites:
                alpha_rect = self.create_alpha(colour, sprite.rect.size)
                self.screen.blit(alpha_rect, sprite.rect)
                sprite.draw(self.screen)
                
    def create_alpha(self, colour, size):
        alpha_rect = pygame.Surface(size)
        alpha_rect.fill(colour)
        alpha_rect.set_alpha(100)
        return alpha_rect

    