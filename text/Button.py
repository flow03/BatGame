import pygame
from pygame.math import Vector2
from text.Iterator import BidirectionalIterator

class Button:
    def __init__(self, text : str, font : pygame.font.Font, center=None, midbottom=None):
        self.text = text
        self.font = font

        self.image = font.render(text, False, 'Black')
        self.rect = self.image.get_rect()
        if center:
            self.rect.center = center
            # print("center", center)
        elif midbottom:
            self.rect.midbottom = midbottom
            # print("midbottom", midbottom)

    def change_color(self, color):
        self.image = self.font.render(self.text, False, color)

    def get_center(self):
        return self.rect.center

    def get_bottom(self):
        return self.rect.bottom

    def collide(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, "Red", self.rect, 2)

    def update_pos(self, midbottom):
        self.rect.midbottom = midbottom

    def shift(self, vector : Vector2):
        # print(vector)
        # print(self.rect.center)
        new_pos = Vector2(self.rect.center) + Vector2(vector)
        self.rect.center = new_pos

class WhiteButton(Button):
    def __init__(self, *args):
        super().__init__(*args)
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

class ButtonsHandler:
    def __init__(self, buttons):
        self.buttons = buttons
        self.active_color = "Red"

        self.active = None
        self.key_pressed = False
        self.mouse_pressed = False
        self.active_iterator()

        self.mouse_pos = None

    def active_iterator(self):
        if self.buttons:
            # if self.active:
            #     self.buttons[self.active].change_color("Black")
            self.active = BidirectionalIterator(list(self.buttons.keys()))
            self.buttons[self.active.current].change_color(self.active_color)
    
    def get_active(self):
        return self.active.current

    def set_active(self, key):
        if key != self.active.current:
            self.buttons[self.active.current].change_color("Black")
            self.active.set_index(key)
            self.buttons[self.active.current].change_color(self.active_color)

    def up(self):
        # self.key_pressed = True
        self.buttons[self.active.current].change_color("Black")
        self.buttons[self.active.prev].change_color(self.active_color)

    def down(self):
        # self.key_pressed = True
        self.buttons[self.active.current].change_color("Black")
        self.buttons[self.active.next].change_color(self.active_color)

    # @property
    # def pressed(self):
    #     return self.key_pressed
    # @property_name.getter призначений для зміни існуючого getter-а, 
    # раніше визначеного з допомогою @property 

    # @pressed.getter
    # def pressed(self, value : bool):
    #     self.key_pressed = value

    # повертає key першої клавіші, з якою відбулася колізія
    def collide_mouse(self, pos):
        for key in self.buttons:
            if self.buttons[key].collide(pos):
                return key
            
    # оновлює self.mouse_pos
    # повертає False, якщо нова позиція миші співпадає з попередньою
    def mouse_move(self):
        new_pos = pygame.mouse.get_pos()
        if new_pos != self.mouse_pos:
            self.mouse_pos = new_pos
            return True
        else:
            # print("Same mouse pos", self.mouse_pos)
            return False

    def update_mouse(self):
        # оновлює активну button, якщо миша рухається
        if self.mouse_move():   # not the same pos
            key = self.collide_mouse(self.mouse_pos)
            if key:
                self.set_active(key)

        # обробляє натиск лівої кнопки миші
        left_mouse = pygame.mouse.get_pressed()[0]  # left mouse key
        right_mouse = pygame.mouse.get_pressed()[2]  # right mouse key
        if left_mouse:
            if not self.mouse_pressed:
                # mouse_pos = pygame.mouse.get_pos()
                key = self.collide_mouse(self.mouse_pos)
                if key:
                    self.mouse_pressed = True
                    self.post(key)
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
                # print(self.get_active())
                # return self.get_active()
                self.key_pressed = True
                self.post(self.get_active())
                # return key
            elif (keys[pygame.K_UP] or keys[pygame.K_w]):
                self.key_pressed = True
                # print("up")
                self.up()
                # pygame.time.delay(200)
            # elif not (keys[pygame.K_UP] or keys[pygame.K_w]):
            #     key_pressed = False
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                self.key_pressed = True
                # print("down")
                self.down()
        elif not (keys[pygame.K_DOWN] or keys[pygame.K_s] or keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_RETURN]):
            self.key_pressed = False
        # else:
        #     print("Key still pressed")

    def post(self, keyname : str):
        # self.key_pressed = True
        event = pygame.event.Event(pygame.KEYDOWN, key=keyname)
        pygame.event.post(event)
        # print(f"Event KEYDOWN {keyname} posted")
        