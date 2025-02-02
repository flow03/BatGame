import pygame
# from actors.Groups import MyGroup, Actors

class Drawer():
    def __init__(self):
        # self.screen = pygame.display.get_surface()
        # self.displayText = False
        self.drawer = Draw() # common as default

    def draw_group(self, group):
        self.drawer.draw_group(group)

    def draw(self, sprite):
        self.drawer.draw_sprite(sprite)

    def common(self):
        self.drawer = Draw()

    def rect(self):
        self.drawer = DrawRect()

    def alpha(self, color): # "Red"
        self.drawer = DrawAlpha()
        self.drawer.color = color

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

class DrawRect(Draw):
    def __init__(self):
        super().__init__()
        self.color = "Red"
    
    def draw_sprite(self, sprite : pygame.sprite.Sprite):
        sprite.draw(self.screen)
        pygame.draw.rect(self.screen, self.color, sprite.rect, 2)

class DrawAlpha(Draw):
    def __init__(self):
        super().__init__()
        self.color = "Red"
    
    def draw_sprite(self, sprite : pygame.sprite.Sprite):
        alpha_rect = self.create_alpha(self.color, sprite.rect.size)
        self.screen.blit(alpha_rect, sprite.rect)
        sprite.draw(self.screen)

    def create_alpha(self, color, size):
        alpha_rect = pygame.Surface(size)
        alpha_rect.fill(color)
        alpha_rect.set_alpha(100)
        return alpha_rect
 