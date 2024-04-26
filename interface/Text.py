import pygame
from pygame.math import Vector2
from add.Path import resource_path
from random import choice

# Text
class Text:
    def __init__(self, game):
        self.game = game
        self.myfont = pygame.font.SysFont("Montserrat", 30) # Arial Narrow, Montserrat
        self.myBiggerFont = self.get_BiggerFont()
        self.screen = pygame.display.get_surface()
        self.center = Vector2(self.screen.get_rect().center)
        self.WIDTH = self.screen.get_width()
        self.HEIGHT = self.screen.get_height()
        self.createExitRects()
        self.y = 15
        self.y_offset = 25
        self.x_offset = 15

    def display(self):
        if self.game.displayText:
            self.print_fps(self.game.FPS)
            self.print_debug_info()
            # if Girl:
            #     text.print_girl_info(screen, Girl.sprites()[-1]) # the last one
            girl = self.game.groups.actors.get("girl")
            if girl:
                self.print_girl_info(girl)

    def collide_restart(self, mouse):
        return self.restart_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]

    def collide_exit(self, mouse):
        return self.exit_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]

    def get_BiggerFont(self):
        fonts = ["Romashulka.ttf", "moonlight.ttf", "graf.ttf" ]
        font_name = choice(fonts)
        font_url = resource_path("fonts\\" + font_name)

        return pygame.font.Font(font_url, 60)

    def change_BiggerFont(self):
        self.myBiggerFont = self.get_BiggerFont()
        self.createExitRects()

    def createExitRects(self):
        # print("createExitRects call")
        self.myBiggerFont = self.get_BiggerFont()
        self.game_over = self.myBiggerFont.render('GAME OVER', False, 'Black')
        self.game_over_rect = self.game_over.get_rect()
        self.game_over_2 = self.myBiggerFont.render('RESTART?', False, 'Black')
        self.game_over_rect_2 = self.game_over_2.get_rect()
        # self.game_over.
        pos_y = self.center.y - (self.game_over_rect.height + self.game_over_rect_2.height)/2
        position = Vector2(self.center.x, pos_y)
        self.game_over_rect.center = position

        position.y = self.game_over_rect.bottom + 30
        self.game_over_rect_2.center = position

        position.y = self.game_over_rect_2.bottom + 50
        self.restart_text = self.myfont.render('Again', False, 'Black')
        self.restart_text_rect = self.restart_text.get_rect(center=position)

        position.y = self.restart_text_rect.bottom + 30
        self.exit_text = self.myfont.render('Another time', False, 'Black')
        self.exit_text_rect = self.exit_text.get_rect(center=position)

    def blitExitRects(self, screen):
        screen.blit(self.game_over, self.game_over_rect)
        screen.blit(self.game_over_2, self.game_over_rect_2)
        screen.blit(self.restart_text, self.restart_text_rect)
        screen.blit(self.exit_text, self.exit_text_rect)

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
        # self.print('health', player.health_new.health)
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
        loading_text_rect = loading_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2)) # bottomright

        screen.blit(loading_text, loading_text_rect)
