import pygame
# import pygame.font
# import pygame.draw
# import pygame.Rect
from pygame.display import get_surface
from pygame.math import Vector2
from add.Path import resource_path, load_json
from random import choice
from os.path import join

# Text
class Text:
    def __init__(self, game):
        self.game = game
        self.myfont = pygame.font.SysFont("Montserrat", 30) # Arial Narrow, Montserrat
        # self.whitefont = pygame.font.SysFont("Montserrat", 31)
        # self.myBiggerFont = self.get_BiggerFont()
        self.screen = get_surface()
        # self.center = Vector2(self.screen.get_rect().center)
        self.WIDTH = self.screen.get_width()
        self.HEIGHT = self.screen.get_height()
        self.y = 0
        self.y_right = 0
        self.y_offset = 25
        self.x_offset = 20

        text_path = resource_path(join('text', 'lang_en.json'))
        self.text = load_json(text_path)
        self.exit = Exit(self.text)

    def display(self):
        # if self.game.displayText:
        self.y = 85
        self.print_debug_info()
        self.print_effects()
        # if Girl:
        #     text.print_girl_info(screen, Girl.sprites()[-1]) # the last one
        self.print_girl_info()

        self.print_fps(self.game.FPS)
        self.print_help()

    def print_fps(self, FPS):
        self.screen.blit(self.myfont.render('FPS: ' + str(int(FPS.get_fps())), True, "Black"), (self.WIDTH - 85, 15))

    def print_debug_info(self):
        # self.y = 85
        groups = self.game.groups
        # drops = self.game.drops
        player = self.game.player
        # self.print('food on screen', len(drops.foodDrops))
        # self.print('bullets on screen', len(drops.bulletDrops))
        # self.print('loot on screen', len(drops.fallen_drops))
        self.print(self.text['killed_bats'], player.killedBats)
        # self.print('bullets', player.bullets_count)
        self.print(self.text['health'], player.health.health)
        self.print(self.text['speed'], player.speed)
        self.print(self.text['add_speed'], player.add_speed)
        self.print(self.text['defence'], player.defence)

        # self.print('bats', len(groups.bats))
        # self.print('bullets', len(groups.bullets))
        # self.print('actors', len(groups.actors))
        # if groups.actors:
        #     for key in list(groups.actors.keys()):
        #        self.print(key + ' health', groups.actors.get_health(key)) 
        
        # self.print('r_rect_width', player.health_bar.rect.width)
        # self.print('g_rect_width', player.health_bar.green_rect.width)
        # self.print('y_rect_width', player.health_bar.yellow_rect.width)

        self.print_empty()

    def print_effects(self):
        effects = self.game.player.effects
        if effects.queue:
            for key in effects.queue.keys():
                if effects.queue[key].boost <= 1:
                    self.print(key + ' effect', effects.queue[key].time())
                else:
                    boost_text = str(effects.queue[key].boost) + 'x '
                    self.print(boost_text + key + ' effect', effects.queue[key].time())

            self.print_empty()

    def print_girl_info(self):
        girl = self.game.groups.actors.get("girl")
        if girl:
            # self.y = 85 + self.y_offset * 2 # 135
            # self.y += self.y_offset

            self.screen.blit(self.myfont.render("Girl", True, "Black"), (self.x_offset, self.y))
            self.y += self.y_offset

            self.print('state', girl.state.name)
            self.print('current', girl.current_animation)
            # self.print('girl health', girl.health.health)
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

    def print_help(self):
        self.y_right = 85
        self.print_r_text(self.text['moving'])
        self.print_r_text(self.text['fire'])
        self.print_r_text(self.text['effects'])
        self.print_r_text(self.text['speed_key'])
        self.print_r_text(self.text['b_speed_key'])
        self.print_r_text(self.text['food'])
        self.print_r_text(self.text['bat'])
        self.print_r_text(self.text['mushrooms'])
        self.print_r_text(self.text['dummies'])
        self.print_r_text(self.text['girl'])

        self.print_r_text()
        self.print_r_text(self.text['events'])
        self.print_r_text(self.text['restart'])
        self.print_r_text(self.text['help'])
        self.print_r_text()

    def print(self, text : str, variable):
        self.screen.blit(self.myfont.render(text + ": " + str(variable), True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset
    
    def print_empty(self):
        self.y += self.y_offset

    def print_r_text(self, text : str = None):
        x_r_offset = 920
        if text:
            # self.screen.blit(self.whitefont.render(text, True, "White"), (self.x_offset, self.y))
            self.screen.blit(self.myfont.render(text, True, "Black"), (x_r_offset, self.y_right))
            # print(f'"key" : "{text}",')
        self.y_right += self.y_offset
    
    def blit_loading_text(self, screen):
        loading_text = self.myBiggerFont.render('LOADING...', False, 'Black')
        loading_text_rect = loading_text.get_rect(center=self.center) # bottomright

        screen.blit(loading_text, loading_text_rect)

class Exit:
    def __init__(self, text):
        self.myfont = pygame.font.SysFont("Montserrat", 30) # Arial Narrow, Montserrat
        self.fonts = ["Romashulka.ttf", "moonlight.ttf", "graf.ttf" ]
        self.myBiggerFont = self.get_BiggerFont()
        self.screen = get_surface()
        self.center = Vector2(self.screen.get_rect().center)

        self.text = text
        # print(self.text.keys())

        self.createExitButtons()

    def get_BiggerFont(self):
        if not self.fonts:
            self.fonts = ["Romashulka.ttf", "moonlight.ttf", "graf.ttf" ]

        font_name = choice(self.fonts)
        self.fonts.remove(font_name)
        font_url = resource_path(join('fonts', font_name))
        
        return pygame.font.Font(font_url, 60)

    def change_BiggerFont(self):
        self.myBiggerFont = self.get_BiggerFont()
        self.createExitButtons()

    def createExitButtons(self):
        # print("createExitRects call")
        # self.myBiggerFont = self.get_BiggerFont()
        # ----------------------------------------------------------
        position = Vector2(self.center.x, self.center.y - 85)
        # print('new:', position) # (600, 215)
        self.game_over = Button(self.text['over_1'], self.myBiggerFont, position)
        position.y = self.game_over.get_bottom() + 30
        self.game_over_2 = Button(self.text['over_2'], self.myBiggerFont, position)
        position.y = self.game_over_2.get_bottom() + 50
        self.restart_text = Button(self.text['restart_button'], self.myfont, position)
        position.y = self.restart_text.get_bottom() + 30
        self.exit_text = Button(self.text['exit_button'], self.myfont, position)

    def blitExitButtons(self):
        self.game_over.draw(self.screen)
        self.game_over_2.draw(self.screen)
        self.restart_text.draw(self.screen)
        self.exit_text.draw(self.screen)

class Button:
    def __init__(self, text : str, font : pygame.font.Font, center=None, midbottom=None):
        self.line = font.render(text, False, 'Black')
        self.rect = self.line.get_rect()
        if center:
            self.rect.center = center
            # print("center", center)
        elif midbottom:
            self.rect.midbottom = midbottom
            # print("midbottom", midbottom)

    def get_center(self):
        return self.rect.center

    def get_bottom(self):
        return self.rect.bottom

    def collide(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen):
        screen.blit(self.line, self.rect)
        # pygame.draw.rect(screen, "Red", self.rect, 2)

    def update_pos(self, midbottom):
        self.rect.midbottom = midbottom

class WhiteButton(Button):
    def __init__(self, *args):
        super().__init__(*args)
        self.white_rect = pygame.Rect(self.rect)
        border = 5
        self.white_rect.width += border * 2
        self.white_rect.height += border * 2
        self.white_rect.center = self.rect.center
        # self.rect_health = pygame.Rect(self.rect.x + border, self.rect.y + border, 
            # self.rect.width - border * 2, self.rect.height - border * 2)

    def update_pos(self, midbottom):
        self.rect.midbottom = midbottom
        self.white_rect.center = self.rect.center

    def draw(self, screen):
        pygame.draw.rect(screen, "White", self.white_rect, border_radius=100)
        pygame.draw.rect(screen, "Black", self.white_rect, width=1, border_radius=100)
        # pygame.draw.rect(screen, "Red", self.rect, 2)
        screen.blit(self.line, self.rect)
