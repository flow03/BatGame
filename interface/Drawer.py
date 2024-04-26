import pygame
# from actors.Groups import MyGroup, Actors

class Drawer():
    def __init__(self):
        # self.screen = pygame.display.get_surface()
        # self.displayText = False
        self.drawer = Draw()

    def draw(self, obj):
        if isinstance(obj, pygame.sprite.Group):
            self.drawer.draw_group(obj)
        elif isinstance(obj, pygame.sprite.Sprite):
            self.drawer.draw_sprite(obj)

    def common(self):
        self.drawer = Draw()

    def rect(self):
        self.drawer = DrawRect()

    def alpha(self):
        self.drawer = DrawAlpha()

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
 