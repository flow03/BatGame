import pygame
import random
from pygame.math import Vector2
from HealthBar_class import FancyHealthBar

class Bat(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        self.image = self.load_random_frame()

        bat_y = random.randint(0 + self.image.get_height()//2, 
        HEIGHT - self.image.get_height()//2)
        self.rect = self.image.get_rect(midleft=(WIDTH, bat_y))

        self.speed = random.randint(3, 6)
        self.damage = random.randint(15, 30)
  
    def load_random_frame(self):
        i = random.randint(0, 14) # max bat index
        frame = pygame.image.load(f'img/bat/bat{i}.png')
        
        return frame

    def update(self, player):
        self.rect = self.rect.move(-self.speed, 0)

        self.collide(player)

        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, player):
        if self.rect.colliderect(player.rect):
            player.set_damage(self.damage)
            self.kill()

    def set_damage(self, player, damage: int):
        player.killedBats += 1
        self.kill()


class BatSpecial(Bat):
    def __init__(self, screen, food_list):
        super().__init__(screen)

        self.set_rand_pos(screen)
        self.food_list = food_list
        # self.speed = random.randint(1, 3)
        self.speed = 2
        self.max_health = random.randint(40, 60) # bullet damage 25
        self.health = self.max_health
        self.direction = Vector2()

        self.health_bar = FancyHealthBar(self.rect.midtop, self.rect.width, 5, 1)
        self.health_bar.set_max_health(self.health)
        self.health_bar.init()
        self.update_bar_pos()

    def update(self, player):
        self.direction = self.direction_by_player(player.rect.center)
        self.rect.center += self.direction * self.speed
        
        self.update_bar_pos()
        self.health_bar.update_health(self.health)
        self.collide(player)
        self.collide_food()

    def collide_food(self):
        if self.food_list:
            food = pygame.sprite.spritecollideany(self, self.food_list)
            if food and self.health != self.max_health:
                self.set_heal(food.heal)
                food.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.health_bar.draw(screen)

    def update_bar_pos(self):
        self.hp_bar_pos = Vector2(self.rect.midtop)
        self.hp_bar_pos.y -= 10
        self.health_bar.update_pos(self.hp_bar_pos)

    def direction_by_player(self, player_pos):
        player_pos = Vector2(player_pos)
        character_pos = Vector2(self.rect.center)

        direction = player_pos - character_pos
        if direction:   # not Zero
            direction = direction.normalize()

        return direction

    def set_damage(self, player, damage: int):
        self.health -= int(damage)
        if self.health <= 0:
            player.killedBats += 1
            self.kill()
    
    def set_heal(self, heal: int):
        self.health += int(heal)
        if self.health > self.max_health:
            self.health = self.max_health

    def set_rand_pos(self, screen):
        out_x = [0 - (self.rect.width//2+1), screen.get_width() + (self.rect.width//2+1)]
        out_y = [0 - (self.rect.height//2+1), screen.get_height() + (self.rect.width//2+1)]
        selected_var = random.choice(['x', 'y'])
        if selected_var == 'x':
            new_x = random.choice(out_x)
            new_y = random.randint(0, screen.get_height())
        else:
            new_x = random.randint(0, screen.get_width())
            new_y = random.choice(out_y)

        self.rect.center = (new_x, new_y)
