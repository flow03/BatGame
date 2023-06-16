# import pygame
# from Player_class import Player

class Jump:
    def __init__(self):
        self.is_jump = False
        self.is_jump_down = False
        self.jump_height = 120
        self.jump_speed = 6
        self.jump_start_y = None

    # Player jump
    def jump_start(self, player):
        if not self.is_jump:
                self.is_jump = True
                self.jump_start_y = player.rect.y

    def jump_end(self, player):
        if self.is_jump:
            if not self.is_jump_down:
                if (player.rect.y > self.jump_start_y - self.jump_height):
                    player.rect.y -= self.jump_speed
                else: self.is_jump_down = True
            else:
                if (player.rect.y < self.jump_start_y):
                    player.rect.y += self.jump_speed
                else:
                    self.is_jump_down = False
                    self.is_jump = False
