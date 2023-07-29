import pygame

class MyGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        
        # self.alpha_rect = pygame.Surface((100, 100)) #self.get_size()
        # print(self.alpha_rect.get_width(), " ", self.alpha_rect.get_height())
        # self.alpha_rect.set_alpha(100)

    def draw(self, screen, colour = None, alpha = False):
        sprites = self.sprites()
        # print(len(sprites))
        if sprites:
            for sprite in sprites:
                if colour and alpha:
                    alpha_rect = self.create_alpha(colour, sprite.rect.size)
                    screen.blit(alpha_rect, sprite.rect)
                    
                # screen.blit(sprite.image, sprite.rect)
                sprite.draw(screen)

                if colour and not alpha:
                    pygame.draw.rect(screen, colour, sprite.rect, 2)

    def create_alpha(self, colour, size):
        alpha_rect = pygame.Surface(size)
        alpha_rect.fill(colour)
        alpha_rect.set_alpha(100)
        return alpha_rect