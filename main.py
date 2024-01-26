import pygame
# import random
# import spritesheet
from Player import Player
# from add.Jump import Jump
import Drops as Drops
# from add.MyGroup import MyGroup
from visuals.Text import Text
from add.Path import resource_path
from add.UserEvents import UserEvents
from Dance_Girl import Dance_Girl
import Bat
# from Bullet_class import Bullet
from Dummy import Dummy
import Actors
import gc # garbage collector
from Food import FoodCreator

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
Events.isEvents = False
Events.start()

# Groups---
# bat_list = MyGroup()
# bullets = MyGroup() #pygame.sprite.Group()

drops = Drops.Drops()

food = FoodCreator()

# actors = Actors.Actors_()
groups = Actors.Groups()

# Player
player = Player(WIDTH//2, HEIGHT//2, drops) # 150, 300

def createDummies(actors_param):
    left_dummy = Dummy(WIDTH//2 - 200, HEIGHT//2, actors_param.bullets,"fancy_blue", 50, 5)
    right_dummy = Dummy(WIDTH//2 + 200, HEIGHT//2, actors_param.bullets, "fancy_gray", 50, 30)
    topleft_dummy = Dummy(WIDTH//2 - 200, HEIGHT//2 - 200, actors_param.bullets,"blue", 3)
    topright_dummy = Dummy(WIDTH//2 + 200, HEIGHT//2 - 200, actors_param.bullets, "gray", 50)
    down_dummy = Dummy(WIDTH//2, HEIGHT//2 + 200, actors_param.bullets, "cell", 15)

    actors_param.add_actor("left_dummy", left_dummy)
    actors_param.add_actor("right_dummy", right_dummy)
    actors_param.add_actor("topleft_dummy", topleft_dummy)
    actors_param.add_actor("topright_dummy", topright_dummy)
    actors_param.add_actor("down_dummy", down_dummy)

# 3 variants of add
# actors['actors'].add(dummy)
# actors['actors'] = dummy
# actors.add('actors', dummy)

# createDummies(groups)



# Update
def update_objects():
    # bat_list.update()
    player.update()
    # bullets.update()
    drops.update()
    groups.update()

# Draw
def draw_objects(isBoundRects):
    colourGreen, colourRed = Actors.get_colour(isBoundRects)
    drops.draw(screen, colourGreen)
    groups.draw(screen, colourRed)
    player.draw(screen, colourGreen)
    food.draw(screen)

# Sound
# bg_sound = pygame.mixer.Sound('sounds/Black Sabbath - Paranoid.mp3')
# bg_sound.play()

# Bool triggers
displayText = False
# gameplay = True
run = True

def initialize():
    player.init()
    groups.clear()
    drops.clear()
    # jump.is_jump = False
    Events.start()
    # createDummies(groups) # after groups.clear

# Main loop
while run:
    FPS.tick(60)

    screen.blit(bg, (bg_x, bg_y))

    if player.gameplay:
        
        player.input()

        update_objects()
        draw_objects(displayText)
        
        if displayText:
            text.print_fps(screen, FPS)
            text.print_debug_info(screen, groups, drops, player)
            # if Girl:
            #     text.print_girl_info(screen, Girl.sprites()[-1]) # the last one
            girl = groups.get_actor("girl")
            if girl:
                text.print_girl_info(screen, girl)

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
            groups.add_bat(Bat.Bat(drops, player, groups.bullets))
        if event.type == Events.BAT_SP_TIMER:
            groups.add_bat(Bat.BatSpecial(drops, player, groups.bullets))
        if event.type == Events.BULLET_DROP_TIMER:
            drops.create_bulletDrop()
        if event.type == Events.FOOD_DROP_TIMER:
            drops.create_foodDrop()
        if player.gameplay and event.type == pygame.MOUSEBUTTONDOWN:
            # Створення кулі з позиції гравця до позиції миші
            player.shoot(groups.bullets, pygame.mouse.get_pos())
        if player.gameplay and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e or event.key == pygame.K_q:
                # Створення кулі, яка летітиме у напрямку player.direction
                player.shoot(groups.bullets)
            if event.key == pygame.K_TAB:
                if not displayText:
                    displayText = True
                else:
                    displayText = False
            if event.key == pygame.K_t:
                Events.switch()
            if event.key == pygame.K_p:
                player.add_effect("poison")
            if event.key == pygame.K_i:
                player.add_effect("ironskin")
            if event.key == pygame.K_LSHIFT:
                player.add_effect("speed")
            if event.key == pygame.K_o:
                player.add_effect("onepunch")
            if event.key == pygame.K_n:
                player.add_effect("harmless")
            if event.key == pygame.K_b:
                player.add_effect("standing")
            if event.key == pygame.K_m: # unlimited
                groups.add_actor("girl", Dance_Girl(player, groups.actors, drops.foodDrops))
            if event.key == pygame.K_h:
                groups.actors_heal(5)
                player.set_heal(5)
            if event.key == pygame.K_k:
                groups.actors_damage(5)
                player.set_damage(5)

        # працює незалежно від player.gameplay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                initialize()
            if event.key == pygame.K_g:
                gc.collect()
                print(gc.get_stats())

pygame.quit()

