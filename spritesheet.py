import pygame

class SpriteSheet():
    def __init__(self, path: str):
        self.sheet = pygame.image.load(path).convert_alpha()

    def get_image(self, col: int, row: int = 0, width = 60, height = 60):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((col * width), (row * height), width, height))
        image.set_colorkey((0,0,0)) # Black

        return image

    def get_anim(self, row: int, width = 60, height = 60):
        anim = []
        count = self.sheet.get_width()/width # 8
        col = 0
        while col < count:
            anim.append(self.get_image(col, row, width, height))
            col += 1

        return anim

def anim_blit(surf: pygame.Surface, animation: list, x, y):
    for frame in animation:
        surf.blit(frame, (x, y))
        x += frame.get_width()
    pass