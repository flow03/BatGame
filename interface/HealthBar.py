import pygame
from pygame.math import Vector2
from add.Clock import Clock
from add.Path import resource_path
from interface.Effects import Effect

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

    def get_percent(self, percent):
        damage = round(self.max_health * (percent / 100))
        return damage

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
        self.yellow_delay = Clock(500)  # delay before decrease
        self.green_rect = pygame.Rect(self.rect_health)
        self.green_delay = Clock(500)   # delay before increase

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
                self.decrease = True
                # print("decrease True")
                self.yellow_delay.restart()
            elif self.health.health > self.prev_health:
                self.green_rect.width = round(self.max_width * ratio)
                self.increase = True
                # print("increase True")
                self.green_delay.restart()

            self.prev_health = round(self.health.health)

        if self.decrease and self.yellow_delay.end():
            self.yellow_decrease()
        elif not self.decrease:
            self.yellow_rect.width = self.green_rect.width

        if self.increase and self.green_delay.end():
            self.red_increase()
        elif not self.increase:
            self.rect_health.width = self.green_rect.width

        # if self.yellow_clock.end():
        #     self.decrease = True
        # if self.decrease:
        #     self.yellow_decrease()

        # if self.green_clock.end():
        #     self.increase = True
        # if self.increase:
        #     self.red_increase()
        
        # if not self.is_decrease():
        #     self.yellow_rect.width = self.green_rect.width
        # if not self.is_increase():
        #     self.rect_health.width = self.green_rect.width
    
    # def is_decrease(self):
    #     # delay or decrease
    #     return self.yellow_delay.active() or self.decrease

    # def is_increase(self):
    #     # delay or increase
    #     return self.green_delay.active() or self.increase

    def yellow_decrease(self):
        # print("yellow_decrease")
        if self.yellow_rect.width > self.green_rect.width:
            self.yellow_rect.width -= self.anim_speed
        else:
            self.yellow_rect.width = self.green_rect.width
            self.decrease = False
            # print("decrease False")
            # print()

    def red_increase(self):
        # print("red_increase")
        if self.rect_health.width < self.green_rect.width:
            self.rect_health.width += self.anim_speed
        else:
            self.rect_health.width = self.green_rect.width
            self.increase = False
            # print("increase False")
            # print()

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

    # def update_variant_first(self, bullets_count):
    #     self.image_list.clear()
    #     while bullets_count > self.capacity:
    #         self.create_image(bullets_count)
    #         bullets_count -= self.capacity

    #     if bullets_count:
    #         self.create_image(bullets_count)

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

    def get_bottom(self):
        bottom = self.rect.top
        bottom += (self.rect.height + 2) * len(self.image_list)
        return bottom

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


class CellHealthBar:
    def __init__(self, rect : pygame.Rect, health : Health, border = 1, colour = "Red"):
        self.health = health # reference
        self.rect = pygame.Rect(rect) # new object
        self.border = border
        self.colour = colour
        self.cell_list = list()

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
        # print("cell_width", cell_width)
        self.set_cell_width(cell_width)

    def set_cell_width(self, cell_width):
        cell_rect = pygame.Rect((0,0), (cell_width, self.rect.height))
        self.cell_list.clear()
        for i in range(self.health.max_health):
            self.cell_list.append(HealthBar(pygame.Rect(cell_rect), Health(1), self.border, self.colour))

        self.update_cells()
        self.fit_rect() # self.cell_list_width()

    def cell_list_width(self):
        midleft = Vector2(self.cell_list[0].rect.midleft)
        midright = Vector2(self.cell_list[-1].rect.midright)
        width = midright.x - midleft.x
        return int(width)

    # def cell_visible_width(self):
    #     midleft = Vector2(self.cell_list[0].rect.midleft)
    #     midright = Vector2(self.current_cell().rect.midright)
    #     width = midright.x - midleft.x
    #     return int(width)

    # changes rect width if necessary
    def fit_rect(self):
        # print("fit_rect call")
        new_width = self.cell_list_width()
        center = self.rect.center
        if self.rect.width != new_width:
            # print(f"fit_rect: {self.rect.width} != {new_width}")
            self.rect.width = new_width
            self.update_pos(center)

    def update_pos(self, pos):
        self.rect.center = pos
        self.update_cells()

    def update_pos_left(self, pos):
        # print('cell update_pos_left')
        self.rect.midleft = pos
        self.update_cells()

    # розміщує по порядку усі комірки починаючи від крайньої лівої    
    def update_cells(self):
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

class FancyCellHealthBar(CellHealthBar):
    def __init__(self, *params):
        super().__init__(*params)

    def set_cell_width(self, cell_width):
        cell_rect = pygame.Rect((0,0), (cell_width, self.rect.height))
        self.cell_list.clear()
        for i in range(self.health.max_health):
            self.cell_list.append(FancyHealthBar(pygame.Rect(cell_rect), Health(1), self.border, self.colour))

        self.update_cells()
        self.fit_rect() # self.cell_list_width()


class CellMultiHealthBar(CellHealthBar):
    def __init__(self, *params):

        self.draw_list = []
        self.rect_list = []

        super().__init__(*params)

        self.draw_list.append(self.cell_list)
        self.rect_list.append(self.rect)

        self.offset = 10
        self.shift = None

        self.health.restore()
        self.createCellList()

    def init(self):
        pass

    def create_multiple(self, limit):
        if len(self.cell_list) > limit:
            self.draw_list.clear()
            self.rect_list.clear()

            for i in range(0, len(self.cell_list), limit):
                chunk = self.cell_list[i:i + limit]
                # print(f"original_list[{i}:{i + limit}]")
                self.fit_cells(chunk)
                self.draw_list.append(chunk)
                self.rect_list.append(self.get_rect(chunk))

            self.update_pos(self.rect_list[0].center)
            self.shift = self.calculate_shift()

    def fit_cells(self, cells : list, position = None):
        if position:
            position = Vector2(position)
        else:
            position = Vector2(cells[0].rect.midleft)

        for cell in cells:
            cell.update_pos_left(position)
            position.x += cell.rect.width - self.border

    def get_rect(self, cells : list):
        topleft = Vector2(cells[0].rect.topleft)
        bottomright = Vector2(cells[-1].rect.bottomright)

        width = bottomright.x - topleft.x
        height = bottomright.y - topleft.y

        return pygame.Rect(topleft, (width, height))

    def update_pos(self, pos : Vector2):
        pos = Vector2(pos)
        if len(self.draw_list) == len(self.rect_list):
            if self.shift:
                pos.y -= self.shift
            for i in range(len(self.draw_list)):
                self.rect_list[i].center = pos
                self.fit_cells(self.draw_list[i], self.rect_list[i].midleft)
                pos.y += self.offset

    def calculate_shift(self):
        first = Vector2(self.rect_list[0].center)
        last = Vector2(self.rect_list[-1].center)
        average = (first + last) / 2
        return int(average.y - first.y)

    # def draw(self, screen):
    #     for cell in self.cell_list:
    #         cell.draw(screen)

    def set_cell_width(self, cell_width):
        cell_rect = pygame.Rect((0,0), (cell_width, self.rect.height))
        self.cell_list.clear()
        for i in range(self.health.max_health):
            self.cell_list.append(FancyHealthBar(pygame.Rect(cell_rect), Health(1), self.border, self.colour))

        self.update_pos(self.rect_list[0].center)
        # self.fit_rect(self.cell_list_width())

    def fit_rect(self, new_width):
        # print("fit_rect call")
        # new_width = self.cell_list_width()
        center = self.rect.center
        if self.rect.width != new_width:
            # print(f"fit_rect: {self.rect.width} != {new_width}")
            self.rect.width = new_width
            self.update_pos(center)
