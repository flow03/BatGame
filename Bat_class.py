import pygame
import random
from pygame.math import Vector2
from HealthBar import FancyHealthBar
from HealthBar import Health
from Path import resource_path
import Drops_class

class Bat(pygame.sprite.Sprite):
    def __init__(self, screen, food_list, bullet_list, drops_list):
        super().__init__()

        self.screen = screen
        self.food_list = food_list
        self.bullet_list = bullet_list
        self.drops_list = drops_list

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
        img_url = resource_path(f'img/bat/bat{i}.png')
        frame = pygame.image.load(img_url)
        
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
        self.createDrops()
        self.kill()

    def createDrops(self):
        rand_drop = random.randint(0, 1)
        new_drop = None
        drop_group = None
        if rand_drop:
            new_drop = Drops_class.Food()
            self.food_list.add(new_drop)
            drop_group = self.food_list
        else:
            new_drop = Drops_class.BulletDrop()
            self.bullet_list.add(new_drop)
            drop_group = self.bullet_list

        dest = Vector2()
        dest.x = self.rect.centerx
        dest.y = random.randint(self.rect.centery, self.screen.get_height() - 15)
        
        self.drops_list.add(Drops_class.Drop(new_drop, drop_group, self.rect.center, dest))


class BatSpecial(Bat):
    def __init__(self, screen, food_list, bullet_list, drops_list):
        super().__init__(screen, food_list, bullet_list, drops_list)

        self.set_rand_pos(screen)
        # self.food_list = food_list
        # self.speed = random.randint(1, 3)
        self.speed = 2
        max_health = random.randint(30, 55) # bullet damage 25
        self.health = Health(max_health)
        self.direction = Vector2()
        self.target = None

        health_bar_rect = pygame.Rect(self.rect.midtop, (self.rect.width, 5))
        self.health_bar = FancyHealthBar(health_bar_rect, self.health, 1)
        self.update_bar_pos()

    def update(self, player):
        self.changeTarget(player) # player position as default
        self.direction = self.direction_by_point(self.target)
        self.rect.center += self.direction * self.speed
        
        self.update_bar_pos()
        self.health_bar.update_health()
        self.collide(player)
        self.collide_food(player)

    def nearest_food(self):
        nearest_d = None # distance
        nearest_pos = Vector2()
        if self.food_list:
            bat_pos = Vector2(self.rect.center)
            for food in self.food_list:
                food_pos = Vector2(food.rect.center)
                distance = bat_pos.distance_to(food_pos)
                if not nearest_d:
                    nearest_d = distance
                    nearest_pos = food_pos
                if distance < nearest_d: # ???
                    nearest_d = distance
                    nearest_pos = food_pos

        return nearest_d, nearest_pos

    def changeTarget(self, player):
        bat_pos = Vector2(self.rect.center)
        player_p = Vector2(player.rect.center)

        if not self.health.full() and self.food_list:
            player_d = bat_pos.distance_to(player_p)
            food_d, food_p = self.nearest_food()

            if food_d <= player_d:
                self.target = food_p
                # print(f"nearest food: {food_p}")
                # print(f"distance: {food_d}")
            else:
                self.target = player_p
        else:
            self.target = player_p

    def collide_food(self, player):
        if not self.health.full() and self.food_list:
            food = pygame.sprite.spritecollideany(self, self.food_list)
            if food:
                self.health.set_heal(food.heal)
                # self.health_bar.update_health()
                self.target = Vector2(player.rect.center)
                food.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.health_bar.draw(screen)

    def update_bar_pos(self):
        new_pos = Vector2(self.rect.midtop)
        new_pos.y -= 10
        self.health_bar.update_pos(new_pos)

    def direction_by_point(self, target_pos):
        target_pos = Vector2(target_pos)
        character_pos = Vector2(self.rect.center)

        direction = target_pos - character_pos
        if direction:   # not Zero
            direction = direction.normalize()

        return direction

    def set_damage(self, player, damage: int):
        if not self.health.set_damage(damage):
            super().set_damage(player, damage)
        # self.health_bar.update_health()
    
    # def set_heal(self, heal: int):
    #     self.health += int(heal)
    #     if self.health > self.max_health:
    #         self.health = self.max_health

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
