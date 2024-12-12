import pygame
from pygame.math import Vector2
from text.Iterator import ActiveIterator, BidirectionalIterator
# from text.Jokes import JokesCreator
from interface.HealthBar import CellHealthBar, CellMultiHealthBar, Health

class WhiteText:
    def __init__(self,  text : str, font : pygame.font.Font):
        # super().__init__(*args)
        self.text = text
        self.font = font

        self.image = font.render(text, False, 'Black')
        self.rect = self.image.get_rect()
        # self.rect.center = position
    
        self.white_rect = pygame.Rect(self.rect)
        border = 5
        self.white_rect.width += border * 2
        self.white_rect.height += border * 2
        self.white_rect.center = self.rect.center
        # self.rect_health = pygame.Rect(self.rect.x + border, self.rect.y + border, 
            # self.rect.width - border * 2, self.rect.height - border * 2)

    def update_pos(self, midbottom):
        self.rect.midbottom = midbottom
        self.white_rect.center = self.rect.center

    def draw(self, screen):
        pygame.draw.rect(screen, "White", self.white_rect, border_radius=100)
        pygame.draw.rect(screen, "Black", self.white_rect, width=1, border_radius=100)
        # pygame.draw.rect(screen, "Red", self.rect, 2)
        screen.blit(self.image, self.rect)

class Button:
    def __init__(self, key : str, text : str, font : pygame.font.Font, position, color = 'Black'):
        self.key = key
        self.text = text
        self.font = font
        self.color = color

        self.image = font.render(text, False, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def change_color(self, color):
        self.color = color
        self.image = self.font.render(self.text, False, self.color)

    def change_text(self, text : str):
        self.text = text
        self.__init__(self.key, self.text, self.font, self.rect.center, self.color)

    def get_center(self):
        return self.rect.center

    def get_bottom(self):
        return self.rect.bottom

    def collide(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, "Red", self.rect, 2)

    def update_pos(self, pos):
        self.rect.center = pos

    def shift(self, vector : Vector2):
        # print(vector)
        # print(self.rect.center)
        new_pos = Vector2(self.rect.center) + Vector2(vector)
        self.rect.center = new_pos

    def press(self):
        # print("press", self.key)
        return self.key

class ButtonsHandler:
    def __init__(self, buttons : dict):
        self.buttons = buttons

        self.key_pressed = False
        self.mouse_pressed = False
        self.active = ActiveIterator(self.buttons)

        self.mouse_pos = None

    # повертає key першої клавіші, з якою відбулася колізія
    def collide_mouse(self, pos):
        for key in self.buttons:
            if self.buttons[key].collide(pos):
                # self.active.set_active(key)
                return key
            
    def update_mouse(self):
        # оновлює активну button, якщо миша рухається
        new_pos = pygame.mouse.get_pos()
        if new_pos != self.mouse_pos:  # not the same pos
            self.mouse_pos = new_pos
            key = self.collide_mouse(self.mouse_pos)
            if key:
                self.active.set_active(self.buttons[key])

        # обробляє натиск лівої і правоої кнопок миші
        left_mouse = pygame.mouse.get_pressed()[0]  # left mouse key
        right_mouse = pygame.mouse.get_pressed()[2]  # right mouse key
        if left_mouse:
            if not self.mouse_pressed:
                # mouse_pos = pygame.mouse.get_pos()
                key = self.collide_mouse(self.mouse_pos)
                if key:
                    self.mouse_pressed = True
                    self.post(self.buttons[key].press())
                    # return key
        elif right_mouse:
            if not self.mouse_pressed:
                self.mouse_pressed = True
                self.post("back")
        else:   # left mouse key is not pressed
            self.mouse_pressed = False

    def update_keys(self):
        keys = pygame.key.get_pressed()
        if keys and not self.key_pressed:
            if keys[pygame.K_RETURN]:
                self.key_pressed = True
                button = self.active.get_active()
                self.post(button.press())
                # return key
            elif (keys[pygame.K_UP] or keys[pygame.K_w]):
                self.key_pressed = True
                # print("up")
                self.active.up()
                # pygame.time.delay(200)
            # elif not (keys[pygame.K_UP] or keys[pygame.K_w]):
            #     key_pressed = False
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                self.key_pressed = True
                # print("down")
                self.active.down()
        elif not (keys[pygame.K_DOWN] or keys[pygame.K_s] or keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_RETURN]):
            self.key_pressed = False
        # else:
        #     print("Key still pressed")

    def post(self, keyname : str):
        # self.key_pressed = True
        event = pygame.event.Event(pygame.KEYDOWN, key=keyname)
        pygame.event.post(event)
        print(f"Event KEYDOWN {keyname} posted")

class SwitchButton(Button):
    def __init__(self, states : list, text_dict : dict, font : pygame.font.Font, position : Vector2):
        self.states = BidirectionalIterator(states)
        self.text_dict = text_dict
        # TODO не страхує, якщо states пустий, або його елементи не рядки
        self.key = self.states.current
        super().__init__(self.key, text_dict[self.key], font, position)

    def press(self):
        self.key = self.states.next
        super().__init__(self.key, self.text_dict[self.key], self.font, self.rect.center, self.color)
        return self.key
    
    def change_text(self):
        self.text = self.text_dict[self.key]
        super().__init__(self.key, self.text_dict[self.key], self.font, self.rect.center, self.color)

class OnOffButton(SwitchButton):
    def __init__(self, name : str, text_dict : dict, font : pygame.font.Font, position : Vector2):
        self.name = name
        states = ["on", "off"]  # ключі мають називатись саме так, щоб їх можна було знайти у мовному файлі
        super().__init__(states, text_dict, font, position)

    def press(self):
        super().press()
        return self.name + '_' + self.key

# class OnOffButtonBar(OnOffButton):
#     def __init__(self, *args):
#         super().__init__(*args)
#         self.jokes = None

#     def create_bar(self, jokes, position : Vector2):
#         self.jokes = jokes
#         rect = pygame.Rect(position, (100, 15))
#         current_length, max_length = self.jokes.category_length(self.name)
#         health = Health(max_length)
#         health.health = current_length
#         self.bar = CellHealthBar(rect, health, 1, "White")

#     def draw(self, screen):
#         super().draw(screen)
#         self.bar.draw(screen)

class JokesBar:
    def __init__(self, jokes, buttonsHandler : ButtonsHandler): #   jokes : JokesCreator,
        self.jokes = jokes
        self.buttonsHandler = buttonsHandler
        self.bars = dict() # dict.fromkeys(jokes.data)
        for key in self.jokes.data:
            self.bars[key] = self.create_bar(key)
        self.active = None

        self.create_test_bar("common")
    
    def set_position(self, pos):
        for bar in self.bars.values():
            bar.update_pos(pos)

    def create_bar(self, category : str):
        # self.jokes = jokes
        position = Vector2(20,20)
        rect = pygame.Rect(position, (150, 12))
        health = Health(self.jokes.category_max_length(category))
        health.health = self.jokes.category_length(category)
        bar = CellHealthBar(rect, health, 2, "White")
        bar.set_cell_width(23)
        return bar
    
    def create_test_bar(self, category : str):
        position = Vector2(20,20)
        rect = pygame.Rect(position, (150, 12))
        health = Health(self.jokes.category_max_length(category))
        health.health = self.jokes.category_length(category)
        bar = CellMultiHealthBar(rect, health, 2, "White")
        bar.set_cell_width(23)
        bar.create_multiple(10)
        return bar

    # def categories_update(self):
    #     for category in self.bars:
    #         self.category_update(category)

    def category_update(self, category):
        if category in self.bars:
            length = self.jokes.category_length(category)
            if length: # None, якщо категорія вимкнена
                self.bars[category].health.health = length
                self.bars[self.active].update_health()

    def update(self):
        button = self.buttonsHandler.active.get_active()
        # показує лише увімкнені категорії
        if (button.key == "on") and button.name in self.bars: # button.key == "off" or 
            self.active = button.name
            # print("active", self.active)
            # self.bars["tits"].health.health = length
            self.category_update(self.active)
        else:
            self.active = None

    def draw(self, screen):
        if self.active:
            self.bars[self.active].draw(screen)
