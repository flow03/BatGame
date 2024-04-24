import pygame
# import random
# import spritesheet
# from actors.Player import Player
# from add.Jump import Jump
# from loot.Drops import Drops
# from add.MyGroup import MyGroup
# from interface.Text import Text
# from add.Path import resource_path
# from add.UserEvents import UserEvents
from actors.Dance_Girl import Dance_Girl
import actors.Bat as Bat
# from Bullet_class import Bullet
# from actors.Dummy import Dummy
import actors.Groups as Groups
# import gc # garbage collector
# from Food import FoodCreator
from Game import Game

game = Game()

# createDummies(groups)

# Update
def update_objects():
    # bat_list.update()
    player.update()
    # bullets.update()
    drops.update()
    groups.update()
    # Events.update()

# Draw
def draw_objects(isBoundRects):
    colourGreen, colourRed = Groups.get_colour(isBoundRects)
    drops.draw(screen, colourGreen)
    groups.draw(colourRed)
    player.draw(screen, colourGreen)

# Sound
# bg_sound = pygame.mixer.Sound('sounds/Black Sabbath - Paranoid.mp3')
# bg_sound.play()

# Bool triggers
displayText = False

# isTenBats = False

# gameplay = True
run = True

def initialize():
    player.init()
    groups.clear()
    drops.clear()
    # jump.is_jump = False
    Events.start()
    dummies.create() # after groups.clear
    text.change_BiggerFont()
    # isTenBats = False


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
            girl = groups.actors.get("girl")
            if girl:
                text.print_girl_info(screen, girl)

        # if not isTenBats and player.killedBats >= 10:
        #     pygame.event.post(pygame.event.Event(Events.TEN_BATS))
        #     isTenBats = True
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
            groups.add_bat(Bat.BatMoving(drops, player, groups.bullets))
        if event.type == Events.BAT_SP_TIMER:
            groups.add_bat(Bat.BatSpecial(drops, player, groups.bullets))
        if event.type == Events.BULLET_DROP_TIMER:
            drops.create_bulletDrop()
        if event.type == Events.FOOD_DROP_TIMER:
            drops.create_foodDrop()
        if event.type == Events.MUSHROOMS:
            drops.create_Mushrooms()
        if event.type == Events.TEN_BATS:
            for i in range(10):
                groups.add_bat(Bat.BatSpecial(drops, player, groups.bullets))
        # if event.type == Events.BAT_KILLED:
        #     killedBats += 1
        # Створення кулі з позиції гравця до позиції миші
        if player.gameplay and event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot(groups.bullets, pygame.mouse.get_pos())
        if player.gameplay and event.type == pygame.KEYDOWN:
            # Створення кулі, яка летітиме у напрямку player.direction
            # if event.key == pygame.K_e or event.key == pygame.K_q:
            #     player.shoot(groups.bullets)
            if event.key == pygame.K_TAB:
                if not displayText:
                    displayText = True
                else:
                    displayText = False
            if event.key == pygame.K_t:
                Events.switch()
            if event.key == pygame.K_p:
                dummieSwitcher = switchDummies(dummieSwitcher)
            if event.key == pygame.K_1:
                player.add_effect("poison")
            if event.key == pygame.K_2:
                player.add_effect("onepunch")
            if event.key == pygame.K_3 or event.key == pygame.K_LSHIFT:
                player.add_effect("speed")
            if event.key == pygame.K_4:
                player.add_effect("ironskin")
            if event.key == pygame.K_5:
                player.add_effect("harmless")
            if event.key == pygame.K_6:
                player.add_effect("stand")
            if event.key == pygame.K_7 or event.key == pygame.K_x:
                player.add_effect("bullets")
            if event.key == pygame.K_m: # unlimited recreates
                groups.add_actor("girl", Dance_Girl(player, groups.actors, drops))
            if event.key == pygame.K_c:
                pygame.event.post(pygame.event.Event(Events.BAT_SP_TIMER))
            if event.key == pygame.K_z:
                drops.create_foodDrop()
            if event.key == pygame.K_LEFTBRACKET or event.key == pygame.K_BACKQUOTE: # tilda
                drops.create_RedMushroom()
            if event.key == pygame.K_RIGHTBRACKET:
                drops.create_BlueMushroom()
            # if event.key == pygame.K_h:
            #     groups.actors_heal(5)
            #     player.set_heal(5)
            # if event.key == pygame.K_k:
            #     groups.actors_damage(5)
            #     player.set_damage(5)

        # працює незалежно від player.gameplay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                initialize()
            # if event.key == pygame.K_g:
            #     gc.collect()
            #     print(gc.get_stats())

pygame.quit()

