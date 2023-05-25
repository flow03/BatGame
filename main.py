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
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("My Python game")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

screen_color = COLOR_BLACK
# screen.fill(screen_color)

isGameActive = True
while isGameActive:
    pygame.display.update()

    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameActive = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen_color = COLOR_VIOLET
                # screen.fill(COLOR_VIOLET)
            if event.key == pygame.K_s:
                screen_color = COLOR_CYAN
                # screen.fill(COLOR_CYAN)
    


