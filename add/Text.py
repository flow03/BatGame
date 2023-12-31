import pygame
from add.Path import resource_path

# Text
class Text:
    def __init__(self, screen):
        self.myfont = pygame.font.SysFont("Montserrat", 30)
        # myfont = pygame.font.Font('fonts/Thor.otf', 30)
        f_url = resource_path('fonts/MunchkinCyr.ttf')
        self.myBigerFont = pygame.font.Font(f_url, 60)
        # screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.createExitRects()
        self.y = 15
        self.y_offset = 25
        self.x_offset = 15

    def createExitRects(self):
        self.game_over = self.myBigerFont.render('GAME OVER', False, 'Black')
        self.game_over_rect = self.game_over.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))
        self.restart_text = self.myfont.render('Restart', False, 'Black')
        self.restart_text_rect = self.restart_text.get_rect(center=(self.WIDTH/2, self.game_over_rect.y + 100))
        self.exit_text = self.myfont.render('Exit', False, 'Black')
        self.exit_text_rect = self.exit_text.get_rect(center=(self.WIDTH/2, self.restart_text_rect.y + 60))

    def blitExitRects(self, screen):
        screen.blit(self.game_over, (self.WIDTH/2-self.game_over.get_width()/2, self.HEIGHT/2-self.game_over.get_height()/2))
        screen.blit(self.restart_text, self.restart_text_rect)
        screen.blit(self.exit_text, self.exit_text_rect)

    def print_fps(self, screen, FPS):
        screen.blit(self.myfont.render('FPS: ' + str(int(FPS.get_fps())), True, "Black"), (self.WIDTH - 85, 15))

    def print_debug_info(self, screen, groups, drops, player):
        self.y = 55
        self.screen = screen
        # self.print('bats on screen', len(actors['bats']))
        # self.print('food on screen', len(drops.foodDrops))
        # self.print('killed bats', player.killedBats)
        # self.print('bullets', player.bullets_count)
        # self.print('health', player.health_new.health)
        # self.print('speed', player.speed)
        # self.print('defence', player.defence)
        # self.print('loot on screen', len(drops.fallen_drops))
        self.print('bats', len(groups.bats))
        self.print('bullets', len(groups.bullets))
        self.print('actors', len(groups.actors))
        if groups.actors:
            for key in list(groups.actors.keys()):
               self.print(key +' health', groups.actors[key].health.health) 

        if player.effects.queue:
            for key in player.effects.queue.keys():
                self.print(key + " effect", player.effects.queue[key].time())

        # self.print('r_rect_width', player.health_bar.rect.width)
        # self.print('g_rect_width', player.health_bar.green_rect.width)
        # self.print('y_rect_width', player.health_bar.yellow_rect.width)


    def print_girl_info(self, screen, girl):
        # self.y = 85 + self.y_offset * 2 # 135
        self.y += self.y_offset
        self.screen = screen    # for print method

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
            

    def print(self, string : str, variable):
        self.screen.blit(self.myfont.render(string + ": " + str(variable), True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset

    def blit_loading_text(self, screen):
        loading_text = self.myBigerFont.render('LOADING...', False, 'Black')
        loading_text_rect = loading_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2)) # bottomright

        screen.blit(loading_text, loading_text_rect)
