import pygame
import random
# import spritesheet
from Player_class import Player
from Jump_class import Jump
import Bat_class

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

# def get_sprites(filepath: str, count: int):
#     sprites = []
#     i = 0
#     while i < count:
#         sprites.append(pygame.image.load(
#             filepath + str(i) + '.png').convert_alpha())
#         i += 1
#     return sprites

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

# Player
player = Player(150, 300)

# Jump
jump = Jump()

# Bat
# bat_images = get_sprites('img/bat/bat', 11)
bat_list = pygame.sprite.Group()
# bat_speed = 4
bat_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bat_timer, 1500)

# Color rect
green_rect = pygame.Surface((player.rect.width, player.rect.height))
green_rect.fill('Green')
green_rect.set_alpha(100)

# red_rect = pygame.Surface((64, 64))
# red_rect.fill('Red')
# red_rect.set_alpha(100)


# Bullet
bullet = pygame.image.load('img/bullet.png').convert_alpha()
bullet = pygame.transform.scale(bullet, (25, 25))
bullets = []
bullets_count = 5

# Sound
# bg_sound = pygame.mixer.Sound('sounds/Black Sabbath - Paranoid.mp3')
# bg_sound.play()

gameplay = True
run = True
while run:
    FPS.tick(60)

    screen.blit(bg, (bg_x, 0)) # bg_x

    if gameplay:
        
        # gameplay = False
        bat_list.update()
        bat_list.draw(screen)

        for bat in bat_list:
            if bat.rect.colliderect(player.rect):
                gameplay = False
            # screen.blit(red_rect, bat.rect)
            pygame.draw.rect(screen, 'Red', bat.rect, 2)

        
        screen.blit(myfont.render('FPS: ' + str(int(FPS.get_fps())), True, COLOR_BLACK), (WIDTH - 85, 15))
        screen.blit(myfont.render('bats: ' + str(len(bat_list)), True, COLOR_BLACK), (15, 15))

        
        # player.draw(screen)
        
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.rect.x > 0:
            player.move('left')
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.rect.x < (WIDTH - player.rect.width):
            player.move('right')
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.rect.y > 0:
            player.move('up')
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.rect.y < (HEIGHT - player.rect.height):
            player.move('down')
        
        # Player jump
        if keys[pygame.K_SPACE]:
            jump.jump_start(player)

        jump.jump_end(player)

        player.update()
        screen.blit(green_rect, player.rect)
        player.draw(screen)

        # bat_list.sprites()[0].red_rect


        if bullets:
            for (i, bullet_rect) in enumerate(bullets):
                screen.blit(bullet, bullet_rect)
                bullet_rect.x += 4
                if bullet_rect.x > WIDTH:
                    bullets.pop(i)

                if bat_list:
                    for bat in bat_list:
                        if bat.rect.colliderect(bullet_rect):
                            bat_list.remove(bat)
                            bullets.pop(i)

    else:
        # screen.fill("Black")
        screen.blit(game_over, (WIDTH/2-game_over.get_width()/2, HEIGHT/2-game_over.get_height()/2))
        screen.blit(restart_text, restart_text_rect)
        screen.blit(exit_text, exit_text_rect)

        mouse = pygame.mouse.get_pos()
        if restart_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player.reload()
            bat_list.empty()
            bullets.clear()
            bullets_count = 5
            nextFrame = clock() + anim_delay
        elif exit_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            run = False
            # pygame.quit()
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            # pygame.quit()
        if event.type == bat_timer:
            new_bat = Bat_class.Bat(WIDTH, HEIGHT)
            bat_list.add(new_bat)
            # pass
        if gameplay and event.type == pygame.KEYDOWN:
            if  event.key == pygame.K_e or event.key == pygame.K_q:
                # if bullets_count > 0:
                bullets.append(bullet.get_rect(center=(player.rect.midright)))
                # bullets_count -=1
            # pygame.time.delay(80)

        # elif event.type == pygame.KEYDOWN:
        #     pass

pygame.quit()
