import pygame
# import random
# import spritesheet
from Player_class import Player
from Jump_class import Jump
# from Bullet_class import Bullet
from Drops_class import BulletDrop
from MyGroup_class import MyGroup
from Bat_class import Bat
from Bat_class import BatSpecial
from Text_class import Text
from Dance_Girl_class import Dance_Girl
from Drops_class import Food
from Path import resource_path

FPS = pygame.time.Clock()
pygame.init()

WIDTH = 1200
HEIGHT = 600

# screen = pygame.display.set_mode((600, 300), flags=pygame.NOFRAME)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bat Game")
icon = pygame.image.load(resource_path('img/fangs.png')).convert_alpha()
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
pygame.time.set_timer(BAT_TIMER, 3000)
BULLET_DROP_TIMER = pygame.USEREVENT + 2
pygame.time.set_timer(BULLET_DROP_TIMER, 3000)
FOOD_DROP_TIMER = pygame.USEREVENT + 3
pygame.time.set_timer(FOOD_DROP_TIMER, 3000)
BAT_SP_TIMER = pygame.USEREVENT + 4
pygame.time.set_timer(BAT_SP_TIMER, 6000)

# Bullet
bullets = MyGroup() #pygame.sprite.Group()
bulletDrops = MyGroup()
foodDrops = MyGroup()

# Update
def update_objects():
    bat_list.update(player)
    player.update(bulletDrops, foodDrops)
    bullets.update(screen, bat_list, player)
    Margosh.update(player)

# Draw
def draw_objects(isBoundRects):
    if not isBoundRects:
        colourGreen = None
        colourRed = None
    else:
        colourGreen = "Green"
        colourRed = "Red"

    bulletDrops.draw(screen, colourGreen)
    foodDrops.draw(screen, colourGreen)
    bat_list.draw(screen, colourRed)
    player.draw(screen, colourGreen)
    bullets.draw(screen, colourGreen)
    Margosh.draw(screen, colourGreen)


# Sound
# bg_sound = pygame.mixer.Sound('sounds/Black Sabbath - Paranoid.mp3')
# bg_sound.play()

# Bool triggers
isBoundRects = False
# gameplay = True
run = True

def initialize():
    # gameplay = True
    player.init()
    Margosh.empty()
    bat_list.empty()
    bullets.empty()
    bulletDrops.empty()
    foodDrops.empty()
    # bullets_count = 5
    # killedBats = 0
    jump.is_jump = False
    # nextFrame = clock() + anim_delay

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
            text.print_debug_info(screen, bat_list, foodDrops, player)
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
        if not Margosh:
            if event.type == BAT_TIMER:
                bat_list.add(Bat(screen))
            if event.type == BAT_SP_TIMER:
                bat_list.add(BatSpecial(screen, foodDrops))
            if event.type == BULLET_DROP_TIMER:
                bulletDrops.add(BulletDrop(screen))
            if event.type == FOOD_DROP_TIMER:
                new_food = Food()
                new_food.check_random_coordinates(foodDrops, screen)
                foodDrops.add(new_food)
        if player.gameplay and event.type == pygame.MOUSEBUTTONDOWN:
            # Створення кулі з позиції гравця до позиції миші
            player.shoot(bullets, pygame.mouse.get_pos())
        if player.gameplay and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e or event.key == pygame.K_q:
                # Створення кулі, яка летітиме у напрямку player.direction
                player.shoot(bullets)
            if event.key == pygame.K_TAB:
                if not isBoundRects:
                    isBoundRects = True
                else:
                    isBoundRects = False
            if event.key == pygame.K_m:
                if not Margosh:
                    Margosh.add(Dance_Girl(screen, foodDrops))
        # працює незалежно від player.gameplay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                initialize()

pygame.quit()

