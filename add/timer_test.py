import pygame
import time

pygame.init()

# Константи
EVENT_ID = pygame.USEREVENT + 1
TIMER_INTERVAL = 2000  # мілісекунди

# Створюємо вікно
screen = pygame.display.set_mode((640, 480))

class TimerManager:
    def __init__(self, interval):
        self.interval = interval
        self.start_time = 0
        self.pause_time = 0
        self.paused = False

    def start_timer(self):
        self.start_time = time.time()
        pygame.time.set_timer(EVENT_ID, self.interval)

    def pause_timer(self):
        if not self.paused:
            self.pause_time = time.time() - self.start_time
            pygame.time.set_timer(EVENT_ID, 0)  # Зупиняємо таймер
            self.paused = True

    def resume_timer(self):
        if self.paused:
            remaining_time = self.interval - int(self.pause_time * 1000)
            pygame.time.set_timer(EVENT_ID, remaining_time)
            self.paused = False
            print("Часу залишилось:", remaining_time)

# Створюємо екземпляр менеджера таймерів
timer_manager = TimerManager(TIMER_INTERVAL)
timer_manager.start_timer()
counter = 0

# Основний цикл програми
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Перевіряємо, чи спрацювала подія таймера
        elif event.type == EVENT_ID:
            counter += 1
            print("Таймер спрацював!", counter)

        # Управління паузою (натискаємо клавішу P для паузи, R для продовження)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Пауза
                timer_manager.pause_timer()
                print("Таймер поставлений на паузу.")
            elif event.key == pygame.K_r:  # Продовження
                timer_manager.resume_timer()
                print("Таймер відновлений.")

    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
