import pygame
from add.Path import resource_path

class SpriteSheet():
    def __init__(self, path: str):
        img_url = resource_path(path)
        self.sheet = pygame.image.load(img_url).convert_alpha()

    def get_image(self, width = 60, height = 60, col: int = 0, row: int = 0):
        frame_rect = pygame.Rect((col * width), (row * height), width, height)
        frame_image = self.sheet.subsurface(frame_rect)

        return frame_image

    def get_anim(self, width = 60, height = 60, row = 0):
        anim = []
        cols = self.sheet.get_width()//width # 8
        col = 0
        while col < cols:
            anim.append(self.get_image(width, height, col, row))
            col += 1

        return anim

        # for frame_index in range(8):
        #     frame_rect = pygame.Rect(frame_index * sprite_width, 0, sprite_width, sprite_height)
        #     frame_image = sprite_sheet.subsurface(frame_rect)
        #     self.animations[animation].append(frame_image)

def anim_blit(surf: pygame.Surface, animation: list, x, y):
    for frame in animation:
        surf.blit(frame, (x, y))
        x += frame.get_width()

# def anim_blit_dict(surf: pygame.Surface, dictionary: dict, x, y):
#     for anim_list in dictionary.values():
#         anim_blit(surf, anim_list, x, y)
#         if anim_list:
#             y += anim_list[0].get_height()
