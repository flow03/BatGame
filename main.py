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
icon = pygame.image.load('img/flower.png').convert_alpha()
pygame.display.set_icon(icon)

# bg = pygame.image.load('img/bg/bg_PS7HtBx.jpg')
bg = pygame.image.load('img/bg/Work-2.jpg').convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
screen.blit(bg, (0, 0))
# pygame.display.update()

def get_sprites(folder: str, count: int):
    sprites = []
    i = 0
    while i < count:
        sprites.append(pygame.image.load(
            'img/sprite/' + folder + '/' + folder + str(i) + '.png').convert_alpha())
        i += 1
    return sprites


move_right = get_sprites('p_move_right', 8)
move_left = get_sprites('p_move_left', 8)
move_up = get_sprites('p_move_up', 8)
move_down = get_sprites('p_move_down', 8)

myfont = pygame.font.SysFont("Montserrat", 30)
# myfont = pygame.font.Font('fonts/Thor.otf', 30)
# myfont = pygame.font.Font('fonts/MunchkinCyr.ttf', 40)
# text_surface = myfont.render('Experimental text', False, 'Black')

# animation
p_count = 0
bg_x = 0

# Player
player = pygame.image.load('img/sprite/p_move_down/p_move_down0.png').convert_alpha()
player_speed = 15
player_x = 150
player_y = 300
direction = move_right

# Bat
bat = pygame.image.load('img/bat/bat2.png').convert_alpha()
# bat_x = WIDTH + bat.get_width()
# bat_y = player_y
bat_list = []

# Jump
is_jump = False
# is_jump_up = False
is_jump_down = False
jump_height = 120
jump_speed = 20
player_start_y = player_y

bat_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bat_timer, 2500)

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
    screen.blit(player, (player_x, player_y))
    screen.blit(myfont.render(str(int(FPS.get_fps())), True, COLOR_BLACK), (WIDTH - 50, 20))

    if bat_list:
        for el_rect in bat_list:
            screen.blit(bat, el_rect)
            el_rect.x -= 10

            if player_rect.colliderect(el_rect):
                screen.blit(myfont.render('You lose', True, COLOR_RED), (0, 20))
    

    player_rect = player.get_rect(topleft=(player_x, player_y))
    # bat_rect = bat.get_rect(topleft=(bat_x, bat_y))


    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
        player_x -= player_speed
        direction = move_left
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < (WIDTH - player.get_width()):
        player_x += player_speed
        direction = move_right
    elif (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
        player_y -= player_speed
        direction = move_up
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < (HEIGHT - player.get_height()):
        player_y += player_speed
        direction = move_down
        
    if not is_jump and keys[pygame.K_SPACE]:
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


    player = direction[p_count]
    if p_count < 7:
        p_count += 1
    else:
        p_count = 1

    
    
    
    # pygame.display.update(player.get_rect(topleft=(100, 300)))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameActive = False
            pygame.quit()
        if event.type == bat_timer:
            bat_list.append(bat.get_rect(topleft=(WIDTH + bat.get_width(), player_y)))

        # elif event.type == pygame.KEYDOWN:
        #     pass
