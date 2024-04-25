import pygame
from actors.Groups import MyGroup

class Drawer():
    def __init__(self):
        # self.screen = pygame.display.get_surface()
        # self.displayText = False
        self.draw = Draw()

    def draw(self, obj):
        if isinstance(obj, pygame.sprite.Group) or isinstance(obj, MyGroup):
            self.draw.draw_group(obj)
        elif isinstance(obj, pygame.sprite.Sprite):
            self.draw.draw_sprite(obj)

    def common(self):
        self.draw = Draw()

    def rect(self):
        self.draw = DrawRect()

    def alpha(self):
        self.draw = DrawAlpha()

class Draw():
    def __init__(self):
        self.screen = pygame.display.get_surface()
    
    def draw_sprite(self, sprite : pygame.sprite.Sprite):
        sprite.draw(self.screen)

    def draw_group(self, group : pygame.sprite.Group):
        sprites = group.sprites()
        if sprites:
            for sprite in sprites:
                self.draw_sprite(sprite)

class DrawRect():
    def __init__(self):
        super().__init__()
        self.colour = "Red"
    
    def draw_sprite(self, sprite : pygame.sprite.Sprite):
        sprite.draw(self.screen)
        pygame.draw.rect(self.screen, self.colour, sprite.rect, 2)

class DrawAlpha():
    def __init__(self):
        super().__init__()
        self.colour = "Red"
    
    def draw_sprite(self, sprite : pygame.sprite.Sprite):
        alpha_rect = self.create_alpha(self.colour, sprite.rect.size)
        self.screen.blit(alpha_rect, sprite.rect)
        sprite.draw(self.screen)
                
    def create_alpha(self, colour, size):
        alpha_rect = pygame.Surface(size)
        alpha_rect.fill(colour)
        alpha_rect.set_alpha(100)
        return alpha_rect
 