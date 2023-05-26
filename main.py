import pygame

clock = pygame.time.Clock()
pygame.init()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_VIOLET = (128, 0, 128)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 160)
COLOR_RED = (255, 0, 0)

WIDTH = 800
HEIGHT = 400
# screen = pygame.display.set_mode((600, 300), flags=pygame.NOFRAME)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Game")
icon = pygame.image.load('img/flower.png')
pygame.display.set_icon(icon)

# bg = pygame.image.load('img/bg/bg_PS7HtBx.jpg')
bg = pygame.image.load('img/bg/Work-2.jpg')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
screen.blit(bg, (0, 0))
pygame.display.update()

player = pygame.image.load('img/sprite/p_move_down/p_move_down0.png')
# .convert_alpha()



def get_sprites(folder: str, count: int):
    sprites = []
    i = 0
    while i < count:
        sprites.append(pygame.image.load(
            'img/sprite/' + folder + '/' + folder + str(i) + '.png'))
        i += 1
    return sprites


# move_down = get_sprites('p_move_down', 8)
move_right = get_sprites('p_move_right', 8)

# myfont = pygame.font.SysFont("Montserrat", 60)
# myfont = pygame.font.Font('fonts/Thor.otf', 30)
# myfont = pygame.font.Font('fonts/MunchkinCyr.ttf', 40)
# text_surface = myfont.render('Experimental text', False, 'Black')

p_count = 0
bg_x = 0

bg_sound = pygame.mixer.Sound('sounds/Psychosocial x Sexy and I Know It (256).mp3')
bg_sound.play()

isGameActive = True
while isGameActive:
    clock.tick(10)

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + WIDTH, 0))
    bg_x -= 10
    if bg_x <= -WIDTH:
        bg_x = 0

    player = move_right[p_count]
    if p_count < 7:
        p_count += 1
    else:
        p_count = 1

    screen.blit(player, (100, 300))
    # pygame.display.update(player.get_rect(topleft=(100, 300)))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameActive = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            pass
