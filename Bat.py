import pygame
import random
from pygame.math import Vector2
import visuals.HealthBar as HealthBar
import visuals.Effects as Effects
from add.Path import resource_path
import Drops as Drops
import visuals.Shields as Shields

class Bat(pygame.sprite.Sprite):
    def __init__(self, drops : Drops.Drops, player, bullets):
        super().__init__()

        self.screen = pygame.display.get_surface()
        self.drops = drops
        self.player = player
        self.bullet_list = bullets

        WIDTH = self.screen.get_width()
        HEIGHT = self.screen.get_height()
        self.image = self.load_random_frame()

        bat_y = random.randint(0 + self.image.get_height()//2, 
        HEIGHT - self.image.get_height()//2)
        self.rect = self.image.get_rect(midleft=(WIDTH, bat_y))

        self.speed = random.randint(2, 4)
        self.damage = random.randint(15, 30)

        self.effects = Effects.EffectQueue_draw(self)
  
    def load_random_frame(self):
        i = random.randint(0, 17) # max bat index
        img_url = resource_path(f'img/bat/bat{i}.png')
        frame = pygame.image.load(img_url)
        
        return frame

    def update(self):
        self.rect = self.rect.move(-self.speed, 0)

        self.collide()

        if self.rect.right < 0:
            self.kill()

        self.effects.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.effects:
            self.effects.draw(screen) 

    def collide(self):
        # Перевірка колізій з гравцем
        if self.rect.colliderect(self.player.rect):
            self.player.set_damage(self.damage)
            self.kill()
        # Перевірка колізій з кулями
        if self.bullet_list:
            bullet = pygame.sprite.spritecollideany(self, self.bullet_list)
            if bullet:
                self.set_damage(bullet.damage)
                bullet.kill()

    def set_damage(self, damage: int):
        self.player.killedBats += 1
        self.drops.createFallenDrop(self.rect.center)
        self.kill()

    def add_effect(self, effect_key : str):
        self.effects.add(effect_key)

class BatSpecial(Bat):
    def __init__(self, *args):
        super().__init__(*args)

        self.set_rand_pos(self.screen)
        # self.food_list = food_list
        # self.speed = random.randint(1, 3)
        self.speed = 2
        self.createHealth()
        self.direction = Vector2()
        self.target = None

    def createHealth(self):
        max_health = random.randint(30, 55) # bullet damage 25
        self.health = HealthBar.Health(max_health)

        health_bar_rect = pygame.Rect(self.rect.midtop, (self.rect.width, 7))
        health_bar_temp = HealthBar.FancyBoundHealthBar(health_bar_rect, self.health, 1)
        self.health_bar = Shields.AllHealthBars(health_bar_temp)

        self.createShield()
        self.update_bar_pos()

    def createShield(self):
        isShield = random.randint(0, 2)

        if isShield == 1:
            self.createBlueShield()
        elif isShield == 2:
            self.createGrayShield()

    def createBlueShield(self): # , AllBar : Shields.AllHealthBars
        maximum = 4
        max_shield = random.randint(1, maximum)

        if max_shield:
            shield = HealthBar.Health(max_shield)
            if max_shield == maximum:
                shield_width = self.rect.width
            else:
                shield_width = self.rect.width/maximum * max_shield

            shield_bar_rect = pygame.Rect(self.rect.midtop, (shield_width, 7))
            shield_bar_temp = Shields.BlueShield(shield_bar_rect, shield, 1)
            shield_bar_temp.shifting = True
            self.health_bar.shieldbar = shield_bar_temp
            self.health_bar.align = 'center'

    def createGrayShield(self):
        max_shield = random.randint(20, 50)
        shield = HealthBar.Health(max_shield)

        shield_bar_rect = pygame.Rect(self.rect.midtop, (self.rect.width, 7))
        shield_bar_temp = Shields.GrayShield(shield_bar_rect, shield, 1)
        self.health_bar.shieldbar = shield_bar_temp
        self.health_bar.align = 'left'

    def update(self):
        self.changeTarget() # player position as default
        self.direction = self.direction_by_point(self.target)
        self.rect.center += round(self.direction * self.speed)
        
        self.update_bar_pos()
        self.health_bar.update_health()
        self.collide()
        self.collide_food()
        if self.health.empty():
            self.kill()

        self.effects.update()

    def nearest_food(self):
        nearest_d = None # distance
        nearest_pos = Vector2()
        if self.drops.foodDrops:
            bat_pos = Vector2(self.rect.center)
            for food in self.drops.foodDrops:
                food_pos = Vector2(food.rect.center)
                distance = bat_pos.distance_to(food_pos)
                if not nearest_d:
                    nearest_d = distance
                    nearest_pos = food_pos
                if distance < nearest_d: # ???
                    nearest_d = distance
                    nearest_pos = food_pos

        return nearest_d, nearest_pos

    def changeTarget(self):
        bat_pos = Vector2(self.rect.center)
        player_p = Vector2(self.player.rect.center)

        if not self.health.full() and self.drops.foodDrops:
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

    def collide_food(self):
        if not self.health.full() and self.drops.foodDrops and not self.health.empty():
            food = pygame.sprite.spritecollideany(self, self.drops.foodDrops)
            if food:
                # self.health.set_heal(food.heal)
                food.do(self)
                # self.health_bar.update_health()
                self.target = Vector2(self.player.rect.center)
                food.kill()

    def draw(self, screen):
        super().draw(screen)
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

    def set_damage(self, damage: int):
        self.health_bar.set_damage(damage)
        if self.health.empty():
            self.player.killedBats += 1
            self.drops.createFallenDrop(self.rect.center)
            self.kill()

    def set_heal(self, heal: int):
        self.health_bar.set_heal(heal)
    
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

class BatBomb(Bat):
    def __init__(self, *args):
        super().__init__(*args)
        pass

class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        pass
        