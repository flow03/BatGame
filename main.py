import pygame
# import random
# import spritesheet
from Player_class import Player
# from Jump_class import Jump
# from Bullet_class import Bullet
# from Drops_class import BulletDrop
# from Drops_class import Food
import Drops_class
from MyGroup_class import MyGroup
from Bat_class import Bat
from Bat_class import BatSpecial
from Text_class import Text
from Dance_Girl_class import Dance_Girl
from Path import resource_path
from UserEvents import UserEvents
from Dummy import Dummy
import Actors

FPS = pygame.time.Clock()
pygame.init()

WIDTH = 1200
HEIGHT = 600

# screen = pygame.display.set_mode((600, 300), flags=pygame.NOFRAME)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bat Game")
icon = pygame.image.load(resource_path('img/fangs.ico')).convert_alpha()
pygame.display.set_icon(icon)

# Text
text = Text(screen)

# bg = pygame.image.load('img/bg/bg_PS7HtBx.jpg')
bg = pygame.image.load(resource_path('img/bg/Work-2.jpg')).convert()
# bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
# screen.blit(bg, (0, 0))

bg_width, bg_height = bg.get_size()
scale_factor = max(WIDTH / bg_width, HEIGHT / bg_height)
scaled_bg_width = int(bg_width * scale_factor)
scaled_bg_height = int(bg_height * scale_factor)
bg = pygame.transform.scale(bg, (scaled_bg_width, scaled_bg_height))
bg_x = (WIDTH - scaled_bg_width) // 2
bg_y = (HEIGHT - scaled_bg_height) // 2
screen.blit(bg, (bg_x, bg_y))

# print(f"original: {bg_width, bg_height}")
# print(f"scale_factor: {scale_factor}")
# print(f"scaled: {scaled_bg_width, scaled_bg_height}")
# print(f"position: {bg_x, bg_y}")

text.blit_loading_text(screen)
pygame.display.update()

# Jump
# jump = Jump()

Events = UserEvents()

# Groups---
# bat_list = MyGroup()
# bullets = MyGroup() #pygame.sprite.Group()

drops = Drops_class.Drops(screen)
# bulletDrops = MyGroup()
# foodDrops = MyGroup()
# drops_list = MyGroup()

actors = Actors.Actors_()

# Player
player = Player(WIDTH//2, HEIGHT//2, drops) # 150, 300
dummy = Dummy(WIDTH//2 + 200, HEIGHT//2, actors['bullets'])

# 3 variants of add
actors['actors'].add(dummy)
# actors['actors'] = dummy
# actors.add('actors', dummy)

# test_group = MyGroup()
# print('test_group empty ', bool(test_group))

# test_group.add(Dummy(WIDTH//2 + 200, HEIGHT//2, actors['bullets']))
# print('test_group not empty ', bool(test_group))

# Update
def update_objects():
    # bat_list.update()
    player.update()
    # bullets.update()
    drops.update()
    actors.update()

# Draw
def draw_objects(isBoundRects):
    colourGreen, colourRed = Actors.get_colour(isBoundRects)
    drops.draw(screen, colourGreen)
    actors.draw(screen, colourRed)
    player.draw(screen, colourGreen)

# Sound
# bg_sound = pygame.mixer.Sound('sounds/Black Sabbath - Paranoid.mp3')
# bg_sound.play()

# Bool triggers
isBoundRects = False
# gameplay = True
run = True

def initialize():
    player.init()
    actors.clear()
    dummy.init()
    actors['actors'].add(dummy)
    drops.empty()
    # jump.is_jump = False
    Events.set_timer()

# Main loop
while run:
    FPS.tick(60)

    screen.blit(bg, (bg_x, bg_y))

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
        
        # Player jump
        # if keys[pygame.K_SPACE]:
        #     jump.jump_start(player)
        # jump.jump_end(player)

        update_objects()
        draw_objects(isBoundRects)

        
        if isBoundRects:
            text.print_fps(screen, FPS)
            text.print_debug_info(screen, actors, drops, player)
            # if Girl:
            #     text.print_girl_info(screen, Girl.sprites()[-1]) # the last one

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
        # if not Girl:
        if event.type == Events.BAT_TIMER:
            actors['bats'].add(Bat(screen, drops, player, actors['bullets']))
        if event.type == Events.BAT_SP_TIMER:
            actors['bats'].add(BatSpecial(screen, drops, player, actors['bullets']))
        if event.type == Events.BULLET_DROP_TIMER:
            drops.create_bulletDrop()
        if event.type == Events.FOOD_DROP_TIMER:
            drops.create_foodDrop()
        if player.gameplay and event.type == pygame.MOUSEBUTTONDOWN:
            # Створення кулі з позиції гравця до позиції миші
            player.shoot(screen, actors['bullets'], pygame.mouse.get_pos())
        if player.gameplay and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e or event.key == pygame.K_q:
                # Створення кулі, яка летітиме у напрямку player.direction
                player.shoot(screen, actors['bullets'])
            if event.key == pygame.K_TAB:
                if not isBoundRects:
                    isBoundRects = True
                else:
                    isBoundRects = False
            if event.key == pygame.K_t:
                Events.switch()
            if event.key == pygame.K_p:
                player.effects.add("poison")
            if event.key == pygame.K_i:
                player.effects.add("iron")
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_o:
                player.effects.add("speed")
            if event.key == pygame.K_m: # unlimited
                actors.add('actors', Dance_Girl(screen, player, actors, drops.foodDrops))
        # працює незалежно від player.gameplay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                initialize()

pygame.quit()

