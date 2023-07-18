import pygame
# import sys
# import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)

from Bullet_test_class import Bullet
from RedDot_class import RedDot

pygame.init()

# Визначення кольорів
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
text_COLOR = WHITE

# Встановлення розмірів вікна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Політ кулі")

clock = pygame.time.Clock()

# Створення групи куль
bullet_group = pygame.sprite.Group()

# Список для зберігання позицій курсора миші
red_dots = pygame.sprite.Group()

# Позиція гравця і противника
player = pygame.Surface((20, 20))
player.fill(WHITE)
player_pos = (400, 300)
player_rect = player.get_rect(center=(player_pos))
# player_rect.center = player_pos
# player_pos = (width // 2, height - 50)
# enemy_pos = (200, 200)

myFont = pygame.font.SysFont(None, 24)

# Поточні координати
current_bullet_pos = None
current_enemy_pos = None

# Основний цикл програми
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Створення кулі з позиції гравця до позиції противника (позиція миші)
            target_pos = pygame.mouse.get_pos()
            new_bullet = Bullet(player_pos, target_pos)
            bullet_group.add(new_bullet)

            # Додавання позиції курсора миші до списку червоних цяток
            red_dots.add(RedDot(*target_pos))

            # Збереження поточних координат кулі і позиції противника
            # current_bullet_pos = pygame.mouse.get_pos()
            current_enemy_pos = target_pos

    screen.fill(BLACK)

    bullet_group.update(screen, red_dots)
    # for bullet_el in bullet_group:
    #     current_bullet_pos = bullet_el.get_pos()
    #     current_distance = bullet_el.distance
    if bullet_group:
        last_bullet = bullet_group.sprites()[-1]
        current_bullet_pos = last_bullet.get_pos()
        current_distance = last_bullet.distance
        current_position = last_bullet.position
    
    # Відображення гравця
    screen.blit(player, player_rect)

    # Відображення куль на екрані
    bullet_group.draw(screen)
    for bullet in bullet_group:
        pygame.draw.rect(screen, 'Red', bullet.rect, 2)
    # Відображення червоних цяток
    red_dots.draw(screen)
    # for dot in red_dots:
    #     pygame.draw.circle(screen, RED, dot, 5)
    

    # Виведення поточних координат на екран
    if current_bullet_pos:
        if current_enemy_pos and current_bullet_pos == current_enemy_pos:
            text_COLOR = RED
        
        y = 10
        bullet_pos_text = myFont.render(f"Bullet: {current_bullet_pos}", True, WHITE)
        screen.blit(bullet_pos_text, (10, y))
        y += 30
        position_text = myFont.render(f"position: {current_position}", True, WHITE)
        screen.blit(position_text, (10, y))
        y += 30
        enemy_pos_text = myFont.render(f"Enemy: {current_enemy_pos}", True, text_COLOR)
        screen.blit(enemy_pos_text, (10, y))
        y += 30
        distance_text = myFont.render(f"distance: {current_distance}", True, WHITE)
        screen.blit(distance_text, (10, y))

        
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
