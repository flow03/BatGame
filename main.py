import pygame
import random
import spritesheet

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

def get_sprites(filepath: str, count: int):
    sprites = []
    i = 0
    while i < count:
        sprites.append(pygame.image.load(
            filepath + str(i) + '.png').convert_alpha())
        i += 1
    return sprites

def create_bat():
    # enemy_size = (60, 30)
    # enemy = pygame.transform.scale(pygame.image.load('images/enemy.png').convert_alpha(), enemy_size)
    # enemy.fill(COLOR_RED)
    bat = bat_images[random.randint(0, 10)]
    bat_speed = random.randint(3, 6)
    # avoids off screen position
    bat_y = random.randint(0+bat.get_height(), HEIGHT-bat.get_height())
    bat_rect = bat.get_rect(midleft=(WIDTH, bat_y))
    # enemy_move = [random.randint(-8, -4), 0]
    return [bat, bat_rect, bat_speed] # return create tuple as default

# Text
myfont = pygame.font.SysFont("Montserrat", 30)
# myfont = pygame.font.Font('fonts/Thor.otf', 30)
myBigerFont = pygame.font.Font('fonts/MunchkinCyr.ttf', 60)
game_over = myBigerFont.render('GAME OVER', False, 'Black')
restart_text = myfont.render('Restart', False, 'Black')
restart_text_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2+60))
exit_text = myfont.render('Exit', False, 'Black')
exit_text_rect = exit_text.get_rect(center=(WIDTH/2, 350))

def clock():
    # current_time = pygame.time.get_ticks()
    return pygame.time.get_ticks()

# animation background
frame = 0
anim_delay = 100
nextFrame = clock() + anim_delay
bg_x = 0

# def isNextFrame():
#     if clock() > nextFrame:
#         nextFrame += 80
#         return True
#     else:
#         return False

#Test spritesheet
sprite_sheet = spritesheet.SpriteSheet('img/sprite/3dbfca7.png')
test_move_down = sprite_sheet.get_anim(0)
test_move_left = sprite_sheet.get_anim(1)
# move_up = sprite_sheet.get_anim(3)
# frame0 = sprite_sheet.get_image(0)
# frame1 = sprite_sheet.get_image(1)
# frame7 = sprite_sheet.get_image(7)

# Player

# move_right = get_sprites('p_move_right', 8)
# move_left = get_sprites('p_move_left', 8)
# move_up = get_sprites('p_move_up', 8)
# move_down = get_sprites('p_move_down', 8)
move_right = sprite_sheet.get_anim(2)
move_left = sprite_sheet.get_anim(1)
move_up = sprite_sheet.get_anim(3)
move_down = sprite_sheet.get_anim(0)

player = pygame.image.load('img/sprite/p_move_down/p_move_down0.png').convert_alpha()
player_speed = 3
player_x_start = 150
player_y_start = 300
player_x = player_x_start
player_y = player_y_start
direction = move_down

# Bat
# bat = pygame.image.load('img/bat/bat2.png').convert_alpha()
bat_images = get_sprites('img/bat/bat', 11)
# bat = bat_images[random.randint(0, 9)]
# bat_x = WIDTH + bat.get_width()
# bat_y = player_y
bat_list = []
# bat_speed = 4
bat_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bat_timer, 1500)

# Color rect
# up_green_rect = pygame.image.load('img/sprite/up_green_rect.png').convert_alpha()
# side_green_rect = pygame.image.load('img/sprite/side_green_rect.png').convert_alpha()
# down_green_rect = pygame.image.load('img/sprite/down_green_rect.png').convert_alpha()
# green_rect = down_green_rect
green_rect = pygame.Surface((player.get_width(), player.get_height()))
green_rect.fill('Green')
green_rect.set_alpha(100)

# red_rect = pygame.image.load('img/red_rect.png').convert_alpha()
# red_rect = pygame.transform.scale(red_rect, (bat.get_width(), bat.get_height()))
red_rect = pygame.Surface((bat_images[0].get_width(), bat_images[0].get_height()))
red_rect.fill('Red')
red_rect.set_alpha(100)

# Jump
is_jump = False
# is_jump_up = False
is_jump_down = False
jump_height = 120
jump_speed = 6
player_start_y = player_y



# Sound
# bg_sound = pygame.mixer.Sound('sounds/Psychosocial x Sexy and I Know It (256).mp3')
# bg_sound.play()

gameplay = True
run = True
while run:
    FPS.tick(60)

    # screen.blit(bg, (bg_x, 0)) # bg_x
    screen.fill("Green")
    # screen.blit(bg, (bg_x + WIDTH, 0))
    # bg_x -= 5
    # if bg_x <= -WIDTH:
    #     bg_x = 0

    # test frames
    spritesheet.anim_blit(screen, move_down, 0, 40)
    spritesheet.anim_blit(screen, move_left, 0, 100)
    spritesheet.anim_blit(screen, move_right, 0, 160)
    spritesheet.anim_blit(screen, move_up, 0, 220)
    # screen.blit(frame0, (0 * frame0.get_width(), 30))
    # screen.blit(frame1, (1 * frame1.get_width(), 30))
    # screen.blit(frame7, (2 * frame7.get_width(), 30))

    if gameplay:
        if bat_list:
            # where bat[1] is bat_rect, 
            # bat[0] is bat Surface
            # bat[2] is bat_speed
            for bat in bat_list:
                screen.blit(red_rect, bat[1])
                screen.blit(bat[0], bat[1])
                bat[1].x -= bat[2]
                # bat[1].move([-bat[2], 0])

                if bat[1].right < 0:
                    bat_list.pop(bat_list.index(bat))

                if player_rect.colliderect(bat[1]):
                    # screen.blit(myfont.render('You lose', True, COLOR_RED), (0, 20))
                    gameplay = False
        
        screen.blit(myfont.render('FPS: ' + str(int(FPS.get_fps())), True, COLOR_BLACK), (WIDTH - 80, 20))
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
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < (WIDTH - player.get_width()):
            player_x += player_speed
            direction = move_right
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
            player_y -= player_speed
            direction = move_up
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < (HEIGHT - player.get_height()):
            player_y += player_speed
            direction = move_down
        
        # Player jump
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

        # Player animation
        player = direction[frame]
        if clock() > nextFrame:
            if frame < 7:
                frame += 1
            else:
                frame = 0
            # frame = (frame+1)%8
            nextFrame += anim_delay
    else:
        # screen.fill("Black")
        screen.blit(game_over, (WIDTH/2-game_over.get_width()/2, HEIGHT/2-game_over.get_height()/2))
        screen.blit(restart_text, restart_text_rect)
        screen.blit(exit_text, exit_text_rect)

        mouse = pygame.mouse.get_pos()
        if restart_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = player_x_start
            player_y = player_y_start
            bat_list.clear()
            nextFrame = clock() + anim_delay
            is_jump = False
        elif exit_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            run = False
            # pygame.quit()
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            # pygame.quit()
        if event.type == bat_timer:
            # bat_list.append(bat.get_rect(topleft=(WIDTH + bat.get_width(), player_y)))
            # bat_list.append(create_bat())
            pass

        # elif event.type == pygame.KEYDOWN:
        #     pass

pygame.quit()
