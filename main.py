import pygame

FPS = pygame.time.Clock()
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

# player = pygame.image.load('img/sprite/p_move_down/p_move_down0.png')
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
move_left = get_sprites('p_move_left', 8)

myfont = pygame.font.SysFont("Montserrat", 30)
# myfont = pygame.font.Font('fonts/Thor.otf', 30)
# myfont = pygame.font.Font('fonts/MunchkinCyr.ttf', 40)
# text_surface = myfont.render('Experimental text', False, 'Black')

p_count = 0
bg_x = 0

# player = move_right[p_count]
player_speed = 15
player_x = 150
player_y = 300
direction = move_right

is_jump = False
# is_jump_up = False
is_jump_down = False
jump_height = 100
jump_speed = 20
player_start_y = player_y
# jump_count = 7
# jump_height = jump_count


# bg_sound = pygame.mixer.Sound('sounds/Psychosocial x Sexy and I Know It (256).mp3')
# bg_sound.play()

isGameActive = True
while isGameActive:
    FPS.tick(10)

    screen.blit(bg, (bg_x, 0))
    # screen.blit(bg, (bg_x + WIDTH, 0))
    # bg_x -= 5
    # if bg_x <= -WIDTH:
    #     bg_x = 0

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
        player_x -= player_speed
        direction = move_left
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < (WIDTH - player.get_width()):
        player_x += player_speed
        direction = move_right
        
    if not is_jump and (keys[pygame.K_SPACE] or keys[pygame.K_w]):
            is_jump = True
            player_start_y = player_y

    if is_jump:
        if not is_jump_down:
            if (player_y > player_start_y - jump_height):
                player_y -= jump_speed
            else: is_jump_down = True
        else:
            if (player_y < player_start_y):
                player_y += jump_speed
            else:
                is_jump_down = False
                is_jump = False

    # jump_power = (jump_count ** 2) / 2
    # if is_jump:
    #     if jump_count >= -jump_height:
    #         jump_power = (jump_count ** 2) / 2
    #         if jump_count > 0:
    #             player_y -= jump_power
    #         else:
    #             player_y += jump_power
    #         jump_count -= 1
    #     else:
    #         is_jump = False
    #         jump_count = jump_height

    # screen.blit(myfont.render("jump_count " + str(jump_count), True, COLOR_BLACK), (50, 20))
    # screen.blit(myfont.render("player_y " + str(player_y), True, COLOR_BLACK), (50, 50))
    # screen.blit(myfont.render("jump_power " + str(jump_power), True, COLOR_BLACK), (50, 80))
    screen.blit(myfont.render(str(int(FPS.get_fps())), True, COLOR_BLACK), (WIDTH - 50, 20))


    player = direction[p_count]
    if p_count < 7:
        p_count += 1
    else:
        p_count = 1

    screen.blit(player, (player_x, player_y))
    # pygame.display.update(player.get_rect(topleft=(100, 300)))
    

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameActive = False
            pygame.quit()
        # elif event.type == pygame.KEYDOWN:
        #     pass
