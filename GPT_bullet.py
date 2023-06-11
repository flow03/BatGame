import pygame
import math

pygame.init()

FPS = pygame.time.Clock()
# Ініціалізація вікна гри
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Політ кулі")

# Кольори
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Позиція гравця
player_pos = [0, 30]

# Позиція противника
enemy_pos = [100, 100]

# Позиція кулі
bullet_pos = player_pos.copy()

# Швидкість кулі
bullet_speed = 3

# Функція для малювання гравця, противника та кулі
def draw_objects():
    pygame.draw.circle(screen, WHITE, player_pos, 10)  # гравець
    pygame.draw.circle(screen, RED, enemy_pos, 10)  # противник
    pygame.draw.circle(screen, WHITE, bullet_pos, 5)  # куля

# Головний цикл гри
running = True
while running:
    FPS.tick(30)

    screen.fill((0, 0, 0))

    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass

    # Обчислення вектора напрямку від гравця до противника
    direction = [enemy_pos[0] - player_pos[0], enemy_pos[1] - player_pos[1]]
    length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)

    # Нормалізація вектора напрямку
    direction[0] /= length
    direction[1] /= length

    # Рух кулі
    bullet_pos[0] += direction[0] * bullet_speed
    bullet_pos[1] += direction[1] * bullet_speed

    # Малювання об'єктів
    draw_objects()

    # Оновлення екрану
    pygame.display.flip()

pygame.quit()
