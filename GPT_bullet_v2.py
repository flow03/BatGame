import pygame
# import math
import Bullet_class

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
red_dots = []

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
            new_bullet = Bullet_class.Bullet(player_pos, target_pos)
            bullet_group.add(new_bullet)

            # Додавання позиції курсора миші до списку червоних цяток
            red_dots.append(target_pos)

            # Збереження поточних координат кулі і позиції противника
            # current_bullet_pos = pygame.mouse.get_pos()
            current_enemy_pos = target_pos

    screen.fill(BLACK)

    bullet_group.update(screen)
    for bullet_el in bullet_group:
        current_bullet_pos = bullet_el.get_pos()
    
    # Відображення гравця
    screen.blit(player, player_rect)

    # Відображення куль на екрані
    bullet_group.draw(screen)
    # Відображення червоних цяток
    for dot in red_dots:
        pygame.draw.circle(screen, RED, dot, 5)

    # Виведення поточних координат на екран
    if current_bullet_pos is not None:
        if current_enemy_pos is not None and current_bullet_pos == current_enemy_pos:
            text_COLOR = RED
            
        bullet_pos_text = myFont.render(f"Bullet: {current_bullet_pos}", True, WHITE)
        screen.blit(bullet_pos_text, (10, 10))
        enemy_pos_text = myFont.render(f"Enemy: {current_enemy_pos}", True, text_COLOR)
        screen.blit(enemy_pos_text, (10, 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
