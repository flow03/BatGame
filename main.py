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
myBigerFont = pygame.font.Font('fonts/MunchkinCyr.ttf', 60)
game_over = myBigerFont.render('GAME OVER', False, 'White')
restart_text = myfont.render('Restart', False, 'White')
restart_text_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2+60))

# animation
p_count = 0
bg_x = 0

# Player
player = pygame.image.load('img/sprite/p_move_down/p_move_down0.png').convert_alpha()
player_speed = 15
player_x_start = 150
player_y_start = 300
player_x = player_x_start
player_y = player_y_start
direction = move_right

# Bat
bat = pygame.image.load('img/bat/bat2.png').convert_alpha()
# bat_x = WIDTH + bat.get_width()
# bat_y = player_y
bat_list = []

# Color rect
# up_green_rect = pygame.image.load('img/sprite/up_green_rect.png').convert_alpha()
# side_green_rect = pygame.image.load('img/sprite/side_green_rect.png').convert_alpha()
# down_green_rect = pygame.image.load('img/sprite/down_green_rect.png').convert_alpha()
# green_rect = down_green_rect
green_rect = pygame.Surface((player.get_width(), player.get_height()))
green_rect.fill('Green')
green_rect.set_alpha(100)

red_rect = pygame.image.load('img/red_rect.png').convert_alpha()
red_rect = pygame.transform.scale(red_rect, (bat.get_width(), bat.get_height()))

# Jump
is_jump = False
# is_jump_up = False
is_jump_down = False
jump_height = 120
jump_speed = 20
player_start_y = player_y

bat_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bat_timer, 2000)

# bg_sound = pygame.mixer.Sound('sounds/Psychosocial x Sexy and I Know It (256).mp3')
# bg_sound.play()

gameplay = True
run = True
while run:
    FPS.tick(10)

    screen.blit(bg, (bg_x, 0))
    # screen.blit(bg, (bg_x + WIDTH, 0))
    # bg_x -= 5
    # if bg_x <= -WIDTH:
    #     bg_x = 0

    if gameplay:
        if bat_list:
            for bat_rect in bat_list:
                screen.blit(bat, bat_rect)
                screen.blit(red_rect, bat_rect)
                bat_rect.x -= 10

                if bat_rect.right < 0:
                    bat_list.pop(bat_list.index(bat_rect))

                if player_rect.colliderect(bat_rect):
                    # screen.blit(myfont.render('You lose', True, COLOR_RED), (0, 20))
                    gameplay = False
        
        screen.blit(myfont.render(str(int(FPS.get_fps())), True, COLOR_BLACK), (WIDTH - 50, 20))
        screen.blit(myfont.render('bats: ' + str(len(bat_list)), True, COLOR_BLACK), (20, 20))

        player_rect = player.get_rect(topleft=(player_x, player_y))
        # green_rect = pygame.transform.scale(green_rect, (player.get_width(), player.get_height()))
        green_rect = pygame.transform.scale(green_rect, (player_rect.width, player_rect.height))
        screen.blit(green_rect, player_rect)
        screen.blit(player, player_rect)
        

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
            direction = move_left
            # green_rect = side_green_rect
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < (WIDTH - player.get_width()):
            player_x += player_speed
            direction = move_right
            # green_rect = side_green_rect
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
            player_y -= player_speed
            direction = move_up
            # green_rect = up_green_rect
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < (HEIGHT - player.get_height()):
            player_y += player_speed
            direction = move_down
            # green_rect = down_green_rect
            
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
    else:
        screen.fill("Black")
        screen.blit(game_over, (WIDTH/2-game_over.get_width()/2, HEIGHT/2-game_over.get_height()/2))
        screen.blit(restart_text, restart_text_rect)

        mouse = pygame.mouse.get_pos()
        if restart_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = player_x_start
            player_y = player_y_start
            bat_list.clear()
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == bat_timer:
            bat_list.append(bat.get_rect(topleft=(WIDTH + bat.get_width(), player_y)))

        # elif event.type == pygame.KEYDOWN:
        #     pass
