import pygame

# Text
class Text:
    def __init__(self, screen):
        self.myfont = pygame.font.SysFont("Montserrat", 30)
        # myfont = pygame.font.Font('fonts/Thor.otf', 30)
        self.myBigerFont = pygame.font.Font('fonts/MunchkinCyr.ttf', 60)
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

    def print_debug_info(self, screen, FPS, bat_list, killedBats, bullets_count):
        screen.blit(self.myfont.render('FPS: ' + str(int(FPS.get_fps())), True, "Black"), (self.WIDTH - 85, 15))
        self.y = 15
        screen.blit(self.myfont.render('bats on screen: ' + str(len(bat_list)), True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset
        screen.blit(self.myfont.render('killed bats: ' + str(killedBats), True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset
        screen.blit(self.myfont.render('bullets: ' + str(bullets_count), True, "Black"), (self.x_offset, self.y))

    def print_girl_info(self, screen, girl):
        self.y = 65 + self.y_offset * 2
        self.screen = screen    # for print method

        self.screen.blit(self.myfont.render("Girl", True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset

        self.print('state', girl.state)
        self.print('current', girl.current_animation)
        if girl.state == "move_around_player":
            self.print('angle', girl.circle.angle)
            self.print('start_angle', girl.circle.start_angle)
            self.print('laps_completed', girl.circle.laps_completed)
        if girl.state == "dance":
            # self.y += self.y_offset
            self.print('idle', girl.idle_animation)
            self.print('clock', girl.dance.dance_clock.clock())
            self.print('dance_over', girl.dance.dance_clock.dance_over)
            self.print('nextFrame', girl.dance.dance_clock.nextFrame)
            self.print('currentDance', girl.dance.currentDance)

    def print(self, string : str, variable):
        self.screen.blit(self.myfont.render(string + ": " + str(variable), True, "Black"), (self.x_offset, self.y))
        self.y += self.y_offset

    def blit_loading_text(self, screen):
        loading_text = self.myBigerFont.render('LOADING...', False, 'Black')
        loading_text_rect = loading_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2)) # bottomright

        screen.blit(loading_text, loading_text_rect)
