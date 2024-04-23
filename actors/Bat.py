import pygame
import random
import os
from pygame.math import Vector2
import interface.HealthBar as HealthBar
# import interface.Effects as Effects
from add.Path import resource_path
from actors.Actor import Actor, ActorEffects
from loot.Drops import Drops
import interface.Shields as Shields

class Bat(ActorEffects):
    def __init__(self, drops : Drops, player, bullets):
        super().__init__() # self.screen

        # self.screen = pygame.display.get_surface()
        self.drops = drops
        self.player = player
        self.bullet_list = bullets

        self.dir_image = None
        self.image = self.load_random_frame_new()
        self.rect = self.image.get_rect()

        self.speed = random.randint(2, 4)
        self.damage = random.randint(15, 30)

        # self.effects = Effects.EffectQueue_draw(self)
  
    def load_random_frame(self):
        i = random.randint(0, 17) # max bat index
        img_url = resource_path(f'img/bat/bat{i}.png')
        frame = pygame.image.load(img_url)
        
        self.createDirection(i, frame)

        return frame

    def load_random_frame_new(self):
        img_list = []
        path = resource_path(f'img/bat')
        for img in os.listdir(path):
            if img.endswith(".png"):
                img_path = os.path.join(path, img)
                if os.path.isfile(img_path):
                    img_list.append(img_path)

        rand_img = random.choice(img_list)
        frame = pygame.image.load(rand_img)

        index = self.get_num(os.path.basename(rand_img))
        # print("index: ", index)
        self.createDirection(index, frame)

        return frame

    def get_num(self, string):
        num = str()
        for ch in string:
            if ch.isdigit():
                num += ch
            elif num:
                break

        if num.isdigit():
            num = int(num)
            return num
        else:
            return None

    def createDirection(self, number, image):
        left_list = [0, 1, 3, 5, 9, 10, 11, 14, 15]
        if number in left_list:
            self.dir_image = DirectionImage(image)

    def update(self):
        super().update() # effects update

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
        self.killed()

    def killed(self):
        # pygame.event.post(pygame.event.Event(Events.BAT_KILLED))
        self.player.killedBats += 1
        self.drops.createFallenDrop(self.rect.center)
        self.kill()

class BatMoving(Bat):
    def __init__(self, *args):
        super().__init__(*args)
        self.rect.center = self.get_right_position()

    def get_right_position(self):
        WIDTH = self.screen.get_width()
        HEIGHT = self.screen.get_height()
        half_image = self.image.get_height()//2
        max_heigth = HEIGHT - half_image

        bat_y = random.randint(0 + half_image, max_heigth)

        return Vector2(WIDTH + half_image, bat_y)

    def update(self):
        super().update() # effects update
        self.rect = self.rect.move(-self.speed, 0)

        self.collide()

        if self.rect.right < 0:
            self.kill()

class BatSpecial(Bat):
    def __init__(self, *args):
        super().__init__(*args)

        self.set_rand_pos(self.screen)
        # self.food_list = food_list
        # self.speed = random.randint(1, 3)
        self.speed = 2
        self.createHealth()
        # self.direction = Vector2()
        self.target = None

        self.health.set_damage(10) # test

    def createHealth(self):
        max_health = random.randint(30, 55) # bullet damage 25
        self.health = HealthBar.Health(max_health)

        health_bar_rect = pygame.Rect(self.rect.midtop, (self.rect.width, 7))
        health_bar_temp = HealthBar.FancyBoundHealthBar(health_bar_rect, self.health, 1)
        self.health_bar = Shields.AllHealthBars(health_bar_temp)

        self.createRandomShield()
        self.update_bar_pos()

    def createRandomShield(self):
        isShield = random.randint(0, 2)
        # 0 = no shield
        if isShield == 1:
            self.createBlueShield()
        elif isShield == 2:
            max_shield = random.randint(20, 50)
            self.createGrayShield(max_shield)

    def createBlueShield(self): # , AllBar : Shields.AllHealthBars
        maximum = 3
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

    def createGrayShield(self, max_shield):
        # max_shield = random.randint(20, 50)
        shield = HealthBar.Health(max_shield)

        shield_bar_rect = pygame.Rect(self.rect.midtop, (self.rect.width, 7))
        shield_bar_temp = Shields.GrayShield(shield_bar_rect, shield, 1)
        self.health_bar.shieldbar = shield_bar_temp
        self.health_bar.align = 'left'

    def update(self):
        self.changeTarget() # player position as default
        self.direction = self.direction_by_point(self.target)
        self.rect.center += round(self.direction * self.speed)

        if self.dir_image and self.dir_image.is_changed(self.direction):
            self.image = self.dir_image.update_image(self.direction)

        # self.update_bar_pos()
        # self.health_bar.update_health()
        self.collide()
        self.collide_food()
        if self.health.empty():
            self.kill()

        super().update() # effects

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

    # def draw(self, screen):
    #     super().draw(screen)
    #     self.health_bar.draw(screen)

    def update_bar_pos(self):
        new_pos = Vector2(self.rect.midtop)
        new_pos.y -= 10
        self.health_bar.update_pos(new_pos)

    # def direction_by_point(self, target_pos):
    #     target_pos = Vector2(target_pos)
    #     character_pos = Vector2(self.rect.center)

    #     direction = target_pos - character_pos
    #     if direction:   # not Zero
    #         direction = direction.normalize()

    #     return direction

    def set_damage(self, damage: int):
        self.health_bar.set_damage(damage)
        if self.health.empty():
            super().killed()

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

class DirectionImage():
    # Takes left image as an argument
    def __init__(self, image):
        self.direct = Vector2()
        self.left = image
        self.right = self.flip(image)

    def flip(self, image : pygame.Surface) -> pygame.Surface:
        return pygame.transform.flip(image, True, False)

    def is_changed(self, direction : Vector2):
        if direction.x < 0 and self.direct.x < 0:
            return False
        elif direction.x > 0 and self.direct.x > 0:
            return False
        else:
            return True

    def update_image(self, direction : Vector2):
        self.direct = direction
        # move left
        if direction.x < 0:
            return self.left
        # move right
        elif direction.x > 0:
            return self.right
        else:
            return self.left
        # elif direction.x == 0:
        #     # move up
        #     if direction.y < 0:
        #         return self.left
        #     # move down
        #     elif direction.y > 0:
        #         return self.right