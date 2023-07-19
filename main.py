import pygame
# import random
# import spritesheet
from Player_class import Player
from Jump_class import Jump
from Bullet_class import Bullet
from BulletDrop_class import BulletDrop
from MyGroup_class import MyGroup
import Bat_class
from Text_class import Text
from Dance_Girl_class import Dance_Girl

FPS = pygame.time.Clock()
pygame.init()

# COLOR_WHITE = (255, 255, 255)
# COLOR_BLACK = (0, 0, 0)
# COLOR_CYAN = (0, 255, 255)
# COLOR_VIOLET = (128, 0, 128)
# COLOR_GREEN = (0, 255, 0)
# COLOR_BLUE = (0, 0, 160)
# COLOR_RED = (255, 0, 0)

WIDTH = 1200
HEIGHT = 600

# screen = pygame.display.set_mode((600, 300), flags=pygame.NOFRAME)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Game")
icon = pygame.image.load('img/fangs.png').convert_alpha()
pygame.display.set_icon(icon)

# Text
text = Text(screen)

# bg = pygame.image.load('img/bg/bg_PS7HtBx.jpg')
bg = pygame.image.load('img/bg/Work-2.jpg').convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
screen.blit(bg, (0, 0))
text.blit_loading_text(screen)
pygame.display.update()

# def clock():
#     # current_time = pygame.time.get_ticks()
#     return pygame.time.get_ticks()

# animation background
# frame = 0
# anim_delay = 100
# nextFrame = clock() + anim_delay
# bg_x = 0

# def isNextFrame():
#     if clock() > nextFrame:
#         nextFrame += 80
#         return True
#     else:
#         return False

# Player
player = Player(WIDTH//2, HEIGHT//2) # 150, 300

# Margosh
# Margosh = Dance_Girl(screen)
Margosh = MyGroup()

# Jump
jump = Jump()

# Bat
# bat_images = get_sprites('img/bat/bat', 11)
bat_list = MyGroup()
# killedBats = 0
BAT_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(BAT_TIMER, 1500)
BULLET_DROP_TIMER = pygame.USEREVENT + 2
pygame.time.set_timer(BULLET_DROP_TIMER, 2500)

# Color rect
# green_rect = pygame.Surface((player.rect.width, player.rect.height))
# green_rect.fill('Green')
# green_rect.set_alpha(100)

# red_rect = pygame.Surface((64, 64))
# red_rect.fill('Red')
# red_rect.set_alpha(100)


# Bullet
bullets = MyGroup() #pygame.sprite.Group()
# bullets_count = 5
bulletDrops = MyGroup()

# Update and draw
def update_objects():
    bat_list.update(player)
    player.update(bulletDrops)
    bullets.update(screen, bat_list, player)
    Margosh.update(player)

def draw_objects(isBoundRects):
    if not isBoundRects:
        colourGreen = None
        colourRed = None
    else:
        colourGreen = "Green"
        colourRed = "Red"

    bulletDrops.draw(screen, colourGreen)
    bat_list.draw(screen, colourRed)
    player.draw(screen, colourGreen)
    bullets.draw(screen, colourGreen)
    Margosh.draw(screen, colourGreen)


# Sound
# bg_sound = pygame.mixer.Sound('sounds/Black Sabbath - Paranoid.mp3')
# bg_sound.play()

# Bool triggers
isBoundRects = True
# gameplay = True
run = True

def initialize():
    # gameplay = True
    player.init()
    Margosh.empty()
    bat_list.empty()
    bullets.empty()
    bulletDrops.empty()
    # bullets_count = 5
    # killedBats = 0
    jump.is_jump = False
    # nextFrame = clock() + anim_delay

# Main loop
while run:
    FPS.tick(60)

    screen.blit(bg, (0, 0)) # bg_x

    if player.gameplay:
        
        # gameplay = False
        
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a]) and player.rect.x > 0:
            player.move('left')
        if (keys[pygame.K_d]) and player.rect.x < (WIDTH - player.rect.width):
            player.move('right')
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.rect.y > 0:
            player.move('up')
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.rect.y < (HEIGHT - player.rect.height):
            player.move('down')
        # if (keys[pygame.K_LEFT]):
        #     Margosh.move('left')
        # if (keys[pygame.K_RIGHT]):
        #     Margosh.move('right')
        
        # Player jump
        if keys[pygame.K_SPACE]:
            jump.jump_start(player)
        jump.jump_end(player)

        update_objects()
        draw_objects(isBoundRects)

        
        if isBoundRects:
            text.print_fps(screen, FPS)
            text.print_debug_info(screen, bat_list, player)
            if Margosh:
                # sprite = Margosh.sprites()[0]
                text.print_girl_info(screen, Margosh.sprites()[-1]) # the last one

        # COLLISIONS
        # All in classes

    else:
        # screen.fill("Black")
        text.blitExitRects(screen)

        mouse = pygame.mouse.get_pos()
        if text.restart_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            initialize()
        elif text.exit_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            run = False

    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            # pygame.quit()
        if event.type == BAT_TIMER:
            new_bat = Bat_class.Bat(WIDTH, HEIGHT)
            bat_list.add(new_bat)
            pass
        if event.type == BULLET_DROP_TIMER:
            bulletDrops.add(BulletDrop(screen))
        if player.gameplay and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e or event.key == pygame.K_q:
                if player.bullets_count > 0:
                    bullets.add(Bullet(player.rect.center, player.direction))
                    player.bullets_count -=1
            # pygame.time.delay(80)
            if event.key == pygame.K_TAB:
                if not isBoundRects:
                    isBoundRects = True
                else:
                    isBoundRects = False
            if event.key == pygame.K_m:
                if not Margosh:
                    Margosh.add(Dance_Girl(screen))
        # працює незалежно від player.gameplay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                initialize()

pygame.quit()

