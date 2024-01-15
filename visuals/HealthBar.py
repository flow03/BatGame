import pygame
from pygame.math import Vector2
from add.Clock import Clock
from add.Path import resource_path
from visuals.Effects import Effect

# --- bordered rects ---
# player  258 17
# dummy(all)  102 8
# bat  66 7

class Health:
    def __init__(self, max_health):
        self.max_health = max_health
        self.health = self.max_health
    
    def set_damage(self, damage: int):
        self.health -= int(damage)
        if self.health <= 0:
            overdamage = abs(self.health) # absolute_value
            self.health = 0
            return overdamage
        else:
            return False

    def set_heal(self, heal: int):
        self.health += int(heal)
        if self.health > self.max_health:
            overheal = self.health - self.max_health
            self.health = self.max_health
            return overheal
        else:
            return False

    def get_ratio(self):
        return self.health/self.max_health

    def restore(self):
        self.health = self.max_health

    def full(self):
        return self.health == self.max_health

    def empty(self):
        return self.health == 0

class HealthBar:
    def __init__(self, rect : pygame.Rect, health : Health, border = 1, colour = "Red"):
        self.health = health # reference
        # self.rect_health = pygame.Rect(rect) # new object
        # self.rect = pygame.Rect(self.rect_health.x - border, self.rect_health.y - border, 
        #     self.rect_health.width + border * 2, self.rect_health.height + border * 2)
        self.rect = pygame.Rect(rect)        
        self.rect_health = pygame.Rect(self.rect.x + border, self.rect.y + border, 
            self.rect.width - border * 2, self.rect.height - border * 2)

        self.max_width = self.rect_health.width
        self.border = border
        self.prev_health = self.health.health
        self.colour = colour

    def init(self):
        self.rect_health.width = self.max_width
        self.health.restore()

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect_health)
        pygame.draw.rect(screen, "Black", self.rect, self.border)

    def update_pos(self, pos):
        pos = Vector2(pos)
        if self.get_pos() != pos:
            self.rect.center = pos
            # self.bound_rect.midleft = self.rect.midleft
            new_rect_pos = Vector2(self.rect.midleft)
            new_rect_pos.x += self.border
            self.rect_health.midleft = Vector2(new_rect_pos)

    def update_pos_left(self, pos):
        pos = Vector2(pos)
        # if Vector2(self.rect.midleft) != pos:
        self.rect.midleft = pos

        new_rect_pos = Vector2(self.rect.midleft)
        new_rect_pos.x += self.border
        self.rect_health.midleft = new_rect_pos

    # center
    def get_pos(self):
        return Vector2(self.rect.center)
    
    def update_health(self):
        if self.prev_health != self.health.health:
            self.prev_health = round(self.health.health)
            
            ratio = self.health.get_ratio()
            self.rect_health.width = round(self.max_width * ratio)

    def set_health(self, health):
        self.health.health = health
        self.update_health()

    def change_colour(self, colour):
        self.colour = colour

    def set_damage(self, damage: int):
        return self.health.set_damage(damage)

    def set_heal(self, heal: int):
        return self.health.set_heal(heal)

    def restore(self):
        self.health.restore()

class FancyHealthBar(HealthBar):
    # def __init__(self, pos, width, height, border = 2):
    #     super().__init__(pos, width, height, border)
    def __init__(self, *params):
        super().__init__(*params)
    
        self.yellow_rect = pygame.Rect(self.rect_health)
        self.yellow_clock = Clock(500)  # delay before decrease
        self.green_rect = pygame.Rect(self.rect_health)
        self.green_clock = Clock(500)   # delay before increase

        self.init()

    def init(self):
        self.rect_health.width = self.max_width
        self.green_rect.width = self.max_width
        self.yellow_rect.width = self.max_width

        self.anim_speed = 3
        self.decrease = False
        self.increase = False
        self.health.restore()
        # self.prev_health = self.health.health

    def draw(self, screen):
        pygame.draw.rect(screen, "Yellow", self.yellow_rect)
        pygame.draw.rect(screen, "Green", self.green_rect)
        super().draw(screen)

    # for pos methods
    def fit_to_left(self):
        self.green_rect.midleft = self.rect_health.midleft
        self.yellow_rect.midleft = self.rect_health.midleft

    def update_pos(self, pos):
        super().update_pos(pos)
        self.fit_to_left()

    def update_pos_left(self, pos):
        super().update_pos_left(pos)
        self.fit_to_left()
    
    def update_health(self):
        if self.prev_health != self.health.health:

            ratio = self.health.get_ratio()

            if self.health.health < self.prev_health:
                self.green_rect.width = round(self.max_width * ratio)
                # self.rect_health.width = self.green_rect.width
                self.yellow_clock.start()
            elif self.health.health > self.prev_health:
                self.green_rect.width = round(self.max_width * ratio)
                self.green_clock.start()

            self.prev_health = round(self.health.health)

        if self.yellow_clock.end():
            self.decrease = True
        if self.decrease:
            self.yellow_decrease()

        if self.green_clock.end():
            self.increase = True
        if self.increase:
            self.red_increase()
        
        if not self.is_decrease():
            self.yellow_rect.width = self.green_rect.width
        if not self.is_increase():
            self.rect_health.width = self.green_rect.width
    
    def is_decrease(self):
        # delay or decrease
        return self.yellow_clock.active() or self.decrease

    def is_increase(self):
        # delay or increase
        return self.green_clock.active() or self.increase

    def yellow_decrease(self):
        if self.yellow_rect.width > self.green_rect.width:
                self.yellow_rect.width -= self.anim_speed
        else:
            self.yellow_rect.width = self.green_rect.width
            self.decrease = False

    def red_increase(self):
        if self.rect_health.width < self.green_rect.width:
            self.rect_health.width += self.anim_speed
        else:
            self.rect_health.width = self.green_rect.width
            self.increase = False

class BoundHealthBar(HealthBar):
    def __init__(self, *params):
        super().__init__(*params)

        self.bound = 1
        self.bound_rect = pygame.Rect(self.rect_health)
        self.bound_rect.width += self.bound

    def draw(self, screen):
        pygame.draw.rect(screen, "Black", self.bound_rect, self.bound)
        super().draw(screen)
        
    def update_health(self):
        super().update_health()
        self.bound_rect.width = self.rect_health.width + self.bound

    def update_pos(self, pos):
        super().update_pos(pos)
        self.bound_rect.midleft = self.rect_health.midleft

class FancyBoundHealthBar(FancyHealthBar):
    def __init__(self, *params):
        super().__init__(*params)

        self.bound = 1
        self.bound_rect = pygame.Rect(self.rect_health)
        self.bound_rect.width += self.bound

    def draw(self, screen):
        pygame.draw.rect(screen, "Yellow", self.yellow_rect)
        pygame.draw.rect(screen, "Green", self.green_rect)

        if not self.health.empty():
            pygame.draw.rect(screen, "Black", self.bound_rect, self.bound)
        # super().draw(screen)
        
        pygame.draw.rect(screen, self.colour, self.rect_health)
        pygame.draw.rect(screen, "Black", self.rect, self.border)

    def update_health(self):
        super().update_health()
        self.bound_rect.width = self.rect_health.width + self.bound

    def update_pos(self, pos):
        super().update_pos(pos)
        self.bound_rect.midleft = self.rect_health.midleft


class BulletBar:
    def __init__(self, pos, width, height):
        pos = Vector2(pos)
        self.rect = pygame.Rect(*pos, width, height)

        img_url = resource_path('img/bullet.png')
        self.bullet_image = pygame.image.load(img_url).convert_alpha()
        self.bullet_image = pygame.transform.rotate(self.bullet_image, 90)
        self.scale_image(height)
        # self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.capacity = (self.rect.width + 2)//(self.bullet_image.get_width() + 2)
        self.image_list = []

    def create_image(self, bullets_count):
        image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        position = Vector2(0, 0)
        bullets = 0
        width = self.bullet_image.get_width()
        for i in range(bullets_count):
            image.blit(self.bullet_image, position)
            position.x += width + 2
            bullets += 1
            if bullets >= self.capacity:
                break
            # if position.x > self.rect.width - width:
            #     break
        self.image_list.append(image)

    def update_variant_first(self, bullets_count):
        self.image_list.clear()
        while bullets_count > self.capacity:
            self.create_image(bullets_count)
            bullets_count -= self.capacity

        if bullets_count:
            self.create_image(bullets_count)

    def update_variant_second(self, bullets_count):
        full_images = bullets_count // self.capacity
        least_bullets = bullets_count % self.capacity

        # print(f"full_images: {full_images}")
        # print(f"least_bullets: {least_bullets}")

        if len(self.image_list) > full_images:
            while len(self.image_list) > full_images:
                self.image_list.pop()
        else: # <=
            if len(self.image_list): # != 0
                self.image_list.pop()

            while len(self.image_list) < full_images:
                self.create_image(self.capacity)

        if (least_bullets):
            self.create_image(least_bullets)

        # print(f"list_len: {len(self.image_list)}")
        # print()

    def update(self, bullets_count):
        # self.update_variant_first(bullets_count)
        self.update_variant_second(bullets_count)


    def draw(self, screen):
        # pygame.draw.rect(screen, "Red", self.rect, 2)
        position = Vector2(self.rect.topleft)
        for image in self.image_list:
            screen.blit(image, position)
            position.y += self.rect.height + 2

    def scale_image(self, new_height):
        original_width = self.bullet_image.get_width()
        original_height = self.bullet_image.get_height()
        new_width = int(original_width * (new_height / original_height))
        # print(new_width, new_height)
        self.bullet_image = pygame.transform.scale(self.bullet_image, (new_width, new_height))

class EffectBar:
    def __init__(self, effect : Effect):
        self.effect = effect
        max_time = self.effect.duration()
        status_bar_rect = pygame.Rect((0,0), (60, 7))   # pos (0,0)
        self.effect_bar = BoundHealthBar(status_bar_rect, Health(max_time), 1)
        self.effect_bar.change_colour("Yellow")
        
    def update_pos(self, position):
        self.effect_bar.update_pos(position)

    def update(self):
        time = self.effect.time()
        if time:
            self.effect_bar.set_health(time)

    def draw(self, screen):
        self.effect_bar.draw(screen)


# class HealthCell:
#     def __init__(self, rect : pygame.Rect):
#         self.cell = FancyHealthBar(rect, 1, 1)

class CellHealthBar:
    def __init__(self, rect : pygame.Rect, health : Health, border = 1, colour = "Red"):
        self.health = health # reference
        self.rect = pygame.Rect(rect) # new object
        self.border = border
        self.colour = colour
        self.cell_list = list() # []

        self.init()

    def init(self):
        self.health.restore()
        self.createCellList()
        # self.update_pos(self.rect.center)
        # self.fit_rect(self.cell_list_width())
        # print("cell constructor call") 

    def createCellList(self):
        self.cell_list.clear()
        # cell_width = round(self.rect.width/self.health.max_health)
        cell_width = round((self.rect.width + (self.health.max_health - 1) * self.border)/self.health.max_health)
        # cell_width = round((self.rect.width - (self.health.max_health - 1) * self.border)/self.health.max_health)
        # cell_width = (self.rect.width - self.health.max_health + 1)//self.health.max_health + 1
        # print(cell_width)
        cell_rect = pygame.Rect((0,0), (cell_width, self.rect.height))
        for i in range(self.health.max_health):
            self.cell_list.append(FancyHealthBar(pygame.Rect(cell_rect), Health(1), self.border, self.colour))

        self.update_cells_left() # builds cell order

        # return cell_list

    def cell_list_width(self):
        midleft = Vector2(self.cell_list[0].rect.midleft)
        midright = Vector2(self.cell_list[-1].rect.midright)
        width = midright.x - midleft.x
        return int(width)

    def cell_visible_width(self):
        midleft = Vector2(self.cell_list[0].rect.midleft)
        midright = Vector2(self.current_cell().rect.midright)
        width = midright.x - midleft.x
        return int(width)

    # changes rect width if necessary
    def fit_rect(self, new_width):
        # print("fit_rect call")
        center = self.rect.center
        if self.rect.width != new_width:
            # print(f"fit_rect: {self.rect.width} != {new_width}")
            self.rect.width = new_width
            self.update_pos(center)

    def update_pos(self, pos):
        self.rect.center = pos
        self.update_cells_left()

    def update_pos_left(self, pos):
        # print('cell update_pos_left')
        self.rect.midleft = pos
        self.update_cells_left()
        
    def update_cells_left(self):
        position = Vector2(self.rect.midleft)
        for cell in self.cell_list:
            cell.update_pos_left(position)
            position.x += cell.rect.width - self.border

    def draw(self, screen):
        for cell in self.cell_list:
            cell.draw(screen)

        # pygame.draw.rect(screen, "Green", self.rect, 1)

    def update_health(self):
        for index in range(self.health.max_health):
            # if not self.health.empty():
                # full cells
            if index < self.health.health:
                if self.cell_list[index].health.empty():
                    self.cell_list[index].health.set_heal(1)
            # empty cells
            else:
                if self.cell_list[index].health.full(): # or not empty()
                    self.cell_list[index].health.set_damage(1)
            # always update health
            self.cell_list[index].update_health()

    def change_colour(self, colour):
        for cell in self.cell_list:
            cell.change_colour(colour)

    def set_damage(self, damage: int):
        return self.health.set_damage(damage)

    def set_heal(self, heal: int):
        return self.health.set_heal(heal)
    
    def current_cell(self):
        return self.cell_list[self.health.health - 1]