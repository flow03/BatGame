import pygame
from pygame.math import Vector2
from add.Path import resource_path
from random import choice
from os.path import join

# Text
class Text:
    def __init__(self, game):
        self.game = game
        self.myfont = pygame.font.SysFont("Montserrat", 30) # Arial Narrow, Montserrat
        # self.myBiggerFont = self.get_BiggerFont()
        self.screen = pygame.display.get_surface()
        # self.center = Vector2(self.screen.get_rect().center)
        self.WIDTH = self.screen.get_width()
        self.HEIGHT = self.screen.get_height()
        self.y = 15
        self.y_offset = 25
        self.x_offset = 15

        self.exit = Exit()

    def display(self):
        # if self.game.displayText:
        self.print_fps(self.game.FPS)
        self.print_debug_info()
        # if Girl:
        #     text.print_girl_info(screen, Girl.sprites()[-1]) # the last one
        girl = self.game.groups.actors.get("girl")
        if girl:
            self.print_girl_info(girl)

    def print_fps(self, FPS):
        self.screen.blit(self.myfont.render('FPS: ' + str(int(FPS.get_fps())), True, "Black"), (self.WIDTH - 85, 15))

    def print_debug_info(self):
        self.y = 85
        groups = self.game.groups
        # drops = self.game.drops
        player = self.game.player
        # self.print('food on screen', len(drops.foodDrops))
        # self.print('bullets on screen', len(drops.bulletDrops))
        # self.print('loot on screen', len(drops.fallen_drops))
        self.print('killed bats', player.killedBats)
        # self.print('bullets', player.bullets_count)
        self.print('health', player.health.health)
        self.print('speed', player.speed)
        self.print('add_speed', player.add_speed)
        self.print('defence', player.defence)

        # self.print('bats', len(groups.bats))
        # self.print('bullets', len(groups.bullets))
        # self.print('actors', len(groups.actors))
        if groups.actors:
            for key in list(groups.actors.keys()):
               self.print(key + ' health', groups.actors.get_health(key)) 

        if player.effects.queue:
            for key in player.effects.queue.keys():
                if player.effects.queue[key].boost <= 1:
                    self.print(key + ' effect', player.effects.queue[key].time())
                else:
                    self.print(str(player.effects.queue[key].boost) + 'x ' + key + ' effect', player.effects.queue[key].time())

        # self.print('r_rect_width', player.health_bar.rect.width)
        # self.print('g_rect_width', player.health_bar.green_rect.width)
        # self.print('y_rect_width', player.health_bar.yellow_rect.width)

    def print_girl_info(self, girl):
        # self.y = 85 + self.y_offset * 2 # 135
        self.y += self.y_offset

        self.screen.blit(self.myfont.render("Girl", True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset

        self.print('state', girl.state.name)
        self.print('current', girl.current_animation)
        # if girl.state == "move_around_player":
        #     self.print('angle', girl.circle.angle)
        #     self.print('start_angle', girl.circle.start_angle)
        #     self.print('laps_completed', girl.circle.laps_completed)
        # if girl.state == "dance" and girl.dance:
        #     # self.y += self.y_offset
        #     self.print('idle', girl.idle_animation)
        #     self.print('currentDance', girl.dance.currentDance)
        #     self.print('dance_clock', girl.dance.d_clock.clock())
        #     self.print('nextDance', girl.dance.d_clock.nextFrame)
        #     self.print('dance_over', girl.dance.dance_over.nextFrame)

            # self.print('food_clock', girl.dance.food_clock.clock())
            # self.print('nextFood', girl.dance.food_clock.nextFrame)
        ...    

    def print(self, string : str, variable):
        self.screen.blit(self.myfont.render(string + ": " + str(variable), True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset

    def blit_loading_text(self, screen):
        loading_text = self.myBiggerFont.render('LOADING...', False, 'Black')
        loading_text_rect = loading_text.get_rect(center=self.center) # bottomright

        screen.blit(loading_text, loading_text_rect)

class Button:
    def __init__(self, text, font : pygame.font.Font, pos):
        self.text = font.render(text, False, 'Black')
        self.rect = self.text.get_rect(center=pos)

    def get_center(self):
        return self.rect.center

    def get_bottom(self):
        return self.rect.bottom

    def collide(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen):
        screen.blit(self.text, self.rect)

class Exit:
    def __init__(self):
        self.myfont = pygame.font.SysFont("Montserrat", 30) # Arial Narrow, Montserrat
        self.myBiggerFont = self.get_BiggerFont()
        self.screen = pygame.display.get_surface()
        self.center = Vector2(self.screen.get_rect().center)

        str_url = resource_path(join('fonts','lang_s.txt'))
        self.strings = self.get_text(str_url)

        self.createExitButtons()

    def get_text(self, filename):
        strings = {}
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            strings['over'] = lines[0].strip()
            strings['over_add'] = lines[1].strip()
            strings['restart'] = lines[2].strip()
            strings['exit'] = lines[3].strip()
        # print(strings)
        return strings

    def get_BiggerFont(self):
        fonts = ["Romashulka.ttf", "moonlight.ttf", "graf.ttf" ]
        font_name = choice(fonts)
        font_url = resource_path("fonts\\" + font_name)

        return pygame.font.Font(font_url, 60)

    def change_BiggerFont(self):
        self.myBiggerFont = self.get_BiggerFont()
        self.createExitButtons()

    def createExitButtons(self):
        # print("createExitRects call")
        self.myBiggerFont = self.get_BiggerFont()
        # ----------------------------------------------------------
        position = Vector2(self.center.x, self.center.y - 85)
        # print('new:', position) # (600, 215)
        self.game_over = Button(self.strings['over'], self.myBiggerFont, position)
        position.y = self.game_over.get_bottom() + 30
        self.game_over_2 = Button(self.strings['over_add'], self.myBiggerFont, position)
        position.y = self.game_over_2.get_bottom() + 50
        self.restart_text = Button(self.strings['restart'], self.myfont, position)
        position.y = self.restart_text.get_bottom() + 30
        self.exit_text = Button(self.strings['exit'], self.myfont, position)

    def blitExitButtons(self):
        self.game_over.draw(self.screen)
        self.game_over_2.draw(self.screen)
        self.restart_text.draw(self.screen)
        self.exit_text.draw(self.screen)
