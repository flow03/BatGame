import pygame

class MyGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        
        # self.alpha_rect = pygame.Surface((100, 100)) #self.get_size()
        # print(self.alpha_rect.get_width(), " ", self.alpha_rect.get_height())
        # self.alpha_rect.set_alpha(100)

    def draw(self, surface, colour = None, alpha = False):
        sprites = self.sprites()
        # print(len(sprites))
        if sprites:
            if colour and alpha:
                # alpha_rect = self.create_alpha(colour)

                for sprite in sprites:
                    alpha_rect = self.create_alpha(colour, sprite.rect.size)
                    surface.blit(alpha_rect, sprite.rect)
                    # surface.blit(alpha_rect, sprite.rect, (0, 0, *sprite.rect.size))
                    # pygame.draw.rect(surface, (255, 0, 0, 100), sprite.rect)
                    surface.blit(sprite.image, sprite.rect)
            elif colour:
                for sprite in self.sprites():
                    surface.blit(sprite.image, sprite.rect)
                    pygame.draw.rect(surface, colour, sprite.rect, 2)
            else:
                for sprite in self.sprites():
                    surface.blit(sprite.image, sprite.rect)

    # def get_size(self):
    #     size = None
    #     sprites = self.sprites()
    #     if sprites:
    #         print("sprites not empty")
    #         size = (sprites[0].rect.width, sprites[0].rect.height)
    #     else:
    #         print("sprites empty")
    #         size = (0,0)
            
    #     # print(size)
    #     return size

    def create_alpha(self, colour, size = (100, 100)):
        alpha_rect = pygame.Surface(size)
        alpha_rect.fill(colour)
        alpha_rect.set_alpha(100)
        return alpha_rect