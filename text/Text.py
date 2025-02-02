import pygame
# import pygame.font
# import pygame.draw
# import pygame.Rect
from pygame.display import get_surface
# from pygame.math import Vector2
from add.Path import resource_path, load_json
# from random import choice
from os.path import join
from sys import argv
# from text.Iterator import ButtonsHandler
# from text.Menu import Exit

class DebugInfo:
    def __init__(self, game, text):
        self.game = game
        self.text = text
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

        self.r_y = self.HEIGHT - self.y_offset # reversed y
        
    def display(self):
        # if self.game.displayText:
        # self.y = 85
        self.print_debug_info()
        self.print_effects()
        # if Girl:
        #     text.print_girl_info(screen, Girl.sprites()[-1]) # the last one
        self.print_girl_info()

        # self.print_fps(self.game.FPS)
        # self.print_killed_bats()
        self.print_help()

    def print_fps(self):
        self.screen.blit(self.myfont.render('FPS: ' + str(int(self.game.FPS.get_fps())), True, "Black"), (self.WIDTH - 85, 15))

    def print_killed_bats(self):
        text = self.myfont.render(self.text['killed_bats'] + ': ' + str(self.game.killedBats), True, "Black")
        self.screen.blit(text, (self.WIDTH - text.get_width() - 10, 40))

    def print_debug_info(self):
        # self.y = 85
        player = self.game.player
        self.y = player.bullet_bar.get_bottom() + 5
        # groups = self.game.groups
        # drops = self.game.drops
        self.print(self.text['bats_on_screen'], len(self.game.groups.bats))
        # self.print('bullets on screen', len(drops.bulletDrops))
        # self.print('loot on screen', len(drops.fallen_drops))
        # self.print(self.text['killed_bats'], self.game.killedBats)
        # self.print('bullets', player.bullets_count)
        self.print(self.text['health'], player.health.health)
        # self.print(self.text['speed'], player.speed)
        self.print_plus(self.text['speed'], player.speed, player.add_speed)
        self.print_plus(self.text['bullet_speed'], player.b_speed, player.add_b_speed)
        self.print(self.text['defence'], player.defence)
        # jokes_text = self.game.jokes.get_text()
        self.print(self.text['jokes'], self.game.jokes.get_text())

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
                    boost_text = str(effects.queue[key].boost) + 'x ' # with space
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
        self.print_r_text(self.text['girl'])
        self.print_r_text(self.text['dummies'])
        self.print_r_text(self.text['joke'])

        self.print_r_text()
        self.print_r_text(self.text['events'])
        # self.print_r_text(self.text['restart'])
        self.print_r_text(self.text['help'])
        self.print_r_text()

    def print(self, text : str, variable):
        self.screen.blit(self.myfont.render(text + ": " + str(variable), True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset

    def print_plus(self, text : str, variable_1, variable_2):
        text = text + ": " + str(variable_1) + " + " + str(variable_2)
        self.screen.blit(self.myfont.render(text, True, "Black"), (self.x_offset, self.y))
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

class DebugDisplay:
    def __init__(self, game, info : DebugInfo):
        self.game = game
        self.info = info
        self.displayText = False
        self.displayFPS = True
        self.display_killed_bats = True

    def switch_text(self):
        if not self.displayText:
            self.displayText = True
        else:
            self.displayText = False

    def set_button(self, button : str):
        name, state = button.split('_')
        # print('name, state', name, state)
        if name == "displayKilled":
            if state == 'on':
                self.display_killed_bats = True
            elif state == 'off':
                self.display_killed_bats = False
        elif name == "displayFPS":
            if state == 'on':
                self.displayFPS = True
            elif state == 'off':
                self.displayFPS = False

    def display(self):
        if self.displayText:  
            self.info.display()
            
        if self.displayFPS:
            self.info.print_fps()
        if self.display_killed_bats:
            self.info.print_killed_bats()

        if self.displayText:
            self.game.groups.drawer.alpha("Red")
            self.game.drops.drawer.alpha("Green")
        else:
            self.game.groups.drawer.common()
            self.game.drops.drawer.common()

# Text
class Text:
    def __init__(self):
        # self.text = {}

        if "-en" in argv: # sys
            text_path = resource_path(join('text', 'lang_en.json'))
        else:
            text_path = resource_path(join('text', 'lang_uk.json'))

        self.text = dict(load_json(text_path))
        # self.exit = Exit(self.text)

        # if "-s" in argv: # sys
        # over_s = load_json(resource_path(join('text', 'over_s.json')))
        # self.text.update(over_s)
    
    def load(self, lang : str): # 'lang_uk' або 'lang_en'
        filename = lang + '.json'

        text_path = resource_path(join('text', filename))
        self.text = dict(load_json(text_path))
        # print(lang, "loaded")
        # print(self.text)

    def __getitem__(self, key):
        return self.text[key]

    def __setitem__(self, key, text):
        self.text[key] = text

    # для оператора in
    def __contains__(self, key):
        return key in self.text
    
    # def __delitem__(self, key):
    #     del self.text[key]

    # def __bool__(self):
    #     return bool(self.text)
    
    # def __len__(self):
    #     return len(self.text)
