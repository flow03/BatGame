import pygame

pygame.init()

# tuple creating
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_VIOLET = (128, 0, 128)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 160)
COLOR_RED = (255, 0, 0)

# screen = pygame.display.set_mode((600, 300), flags=pygame.NOFRAME)
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("My Python game")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

player = pygame.image.load('img/hero.png').convert_alpha()

square = pygame.Surface((50, 100))
square.fill("Blue")

# screen_color = COLOR_BLACK
screen.fill(COLOR_WHITE)

# myfont = pygame.font.SysFont("Montserrat", 60)
# myfont = pygame.font.Font('fonts/Thor.otf', 30)
myfont = pygame.font.Font('fonts/MunchkinCyr.ttf', 40)
text_surface = myfont.render('Experimental text', False, 'Black')

isGameActive = True
while isGameActive:

    pygame.draw.circle(square, 'Red', (20, 15), 10)
    screen.blit(square, (50, 0))
    screen.blit(text_surface, (100, 100))
    screen.blit(player, (100, 150))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameActive = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            pass
