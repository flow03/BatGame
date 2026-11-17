import pygame

from interface.HealthBar import BulletBar, Bullets, FancyHealthBar, Health
from interface.Shields import AllHealthBars
# from actors.Groups import MyGroup, Actors

# клас для малювання спрайтів та груп спрайтів на екрані
class Drawer():
    def __init__(self):
        # self.screen = pygame.display.get_surface()
        # self.displayText = False
        self.drawer = Draw() # common as default

    def draw_group(self, group : pygame.sprite.Group):
        self.drawer.draw_group(group)

    def draw(self, sprite : pygame.sprite.Sprite):
        self.drawer.draw_sprite(sprite)

    def common(self):
        self.drawer = Draw()

    def rect(self):
        self.drawer = DrawRect()

    def alpha(self, color): # "Red"
        self.drawer = DrawAlpha()
        self.drawer.color = color

class Draw():
    def __init__(self):
        self.screen = pygame.display.get_surface()
    
    def draw_sprite(self, sprite : pygame.sprite.Sprite):
        sprite.draw(self.screen)

    def draw_group(self, group : pygame.sprite.Group):
        sprites = group.sprites()
        if sprites:
            for sprite in sprites:
                self.draw_sprite(sprite)

class DrawRect(Draw):
    def __init__(self):
        super().__init__()
        self.color = "Red"
    
    def draw_sprite(self, sprite : pygame.sprite.Sprite):
        sprite.draw(self.screen)
        pygame.draw.rect(self.screen, self.color, sprite.rect, 2)

class DrawAlpha(Draw):
    def __init__(self):
        super().__init__()
        self.color = "Red"
    
    def draw_sprite(self, sprite : pygame.sprite.Sprite):
        alpha_rect = self.create_alpha(self.color, sprite.rect.size)
        self.screen.blit(alpha_rect, sprite.rect)
        sprite.draw(self.screen)

    def create_alpha(self, color, size):
        alpha_rect = pygame.Surface(size)
        alpha_rect.fill(color)
        alpha_rect.set_alpha(100)
        return alpha_rect

class interfaceDrawer:
    def __init__(self, health : Health, bullets : Bullets):
        start_pos = pygame.Vector2(20, 30)
        
        # health_bar
        self.health = health
        self.bullets = bullets
        health_bar_rect = pygame.Rect(start_pos, (258, 17)) # 254, 13
        health_bar_temp = FancyHealthBar(health_bar_rect, self.health, 2)
        self.health_bar = AllHealthBars(health_bar_temp)

        # bullet_bar
        start_pos.y += 17 + 5
        self.bullet_bar = BulletBar(start_pos, 254, 16) # 15+13+(2*2)

        # self.health_bar.createBlueShield(4) # del after debug
        # self.health_bar.createGrayShield(50)
        # self.health_bar.set_damage(90)
    
    # def reload(self):
    #     self.health_bar.restore() # restore
    #     self.bullet_bar.update(self.bullets)

    def update(self):
        self.health_bar.update_health()
        self.bullet_bar.update(self.bullets)

    def draw(self, screen):
        self.health_bar.draw(screen)
        self.bullet_bar.draw(screen)
    
    # def set_damage(self, damage: int):
    #     # damage = self.defence_damage(damage)
    #     self.health_bar.set_damage(damage)

    # def set_heal(self, heal: int):
    #     self.health_bar.set_heal(heal)
