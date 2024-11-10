# import pygame
from pygame.math import Vector2
import interface.HealthBar as HealthBar
from add.Clock import Clock

class EffectQueue:
    def __init__(self, player):
        self.player = player
        self.queue = {}
        # self.isDraw = False

    def add(self, effect_key):
        if not self.get(effect_key):
            if effect_key == "poison" or effect_key == "stand":
                if self.get("speed"):
                    self.remove("speed")
                    # print("speed removed")
            elif effect_key == "speed":
                if self.get("poison") or self.get("stand"):
                    effect_key = None
                    # print("speed ignored")

            self.createEffect(effect_key) # creation and adding
        else: 
            self.queue[effect_key].increase()
            # print(effect_key, "increased")

    def remove(self, key):
        if self.get(key):
            self.queue[key].__del__()
            self.queue.pop(key)
            # print(key, "removed")

    def get(self, key):
        return self.queue.get(key, None)

    def remove_off(self):
        for key in list(self.queue.keys()):
            if self.queue[key].off():
                self.remove(key)

    def update(self):
        if self.queue:
            self.remove_off() # +cycle

            for effect in self.queue.values():
                effect.update()

    def draw(self, screen):
        ...

    def clear(self):
        for effect in self.queue.values():
            effect.__del__()
        self.queue.clear() # does not call effect destructors of effects

    # def empty(self):
    #     return not bool(self.queue)

    # factory method
    def createEffect(self, effect_key):
        effect = None
        if effect_key == "poison":
            effect = PoisonEffect(self.player)
        if effect_key == "speed":
            effect = SpeedEffect(self.player)
        if effect_key == "ironskin":
            effect = IronskinEffect(self.player)
        if effect_key == "onepunch":
            effect = OnepunchEffect(self.player)
        if effect_key == "harmless":
            effect = HarmlessEffect(self.player)
        if effect_key == "stand":
            effect = StandingEffect(self.player)
        if effect_key == "bullets":
            effect = BulletsEffect(self.player)

        if effect: # not None
            self.queue[effect_key] = effect
        # return effect

class EffectQueue_draw(EffectQueue):
    def __init__(self, player):
        super().__init__(player)

    def add(self, key):
        super().add(key)

        if self.get(key):
            self.queue[key].create_effect_bar()     

    # super.check calls
    # def remove(self, key):
    #     self.queue[key].effect_bar = None
    #     super().remove(key)

    def update_pos(self):
        if self.queue:
            position = Vector2(self.player.rect.midbottom)
            shift = 10
            for effect in self.queue.values():
                position.y += shift
                effect.effect_bar.update_pos(position)

    def update(self):
        super().update() # super check or current???

        for effect in self.queue.values():
            effect.effect_bar.update()
        
        self.update_pos()  

    def draw(self, screen):
        if self.queue:
            for effect in self.queue.values():
                effect.effect_bar.draw(screen)

    # def clear(self):
    #     super().clear()

class Effect:
    def __init__(self, player, time : int):
        self.player = player
        self.effect_bar = None

        self.timer = Clock(time)
        self.timer.start()
        self.boost = 1

    def update(self):
        pass

    def increase(self):
        self.timer.restart()

    def off(self):
        if self.timer.end():
            return True
        return False

    def time(self):
        return self.timer.time()

    def duration(self):
        return self.timer.delay

    def __del__(self):
        pass

    def create_effect_bar(self):
        # warning! cyclic references
        # GC will not delete this object while it is referenced
        if not self.effect_bar:
            self.effect_bar = HealthBar.EffectBar(self)

# ignores defence
class PoisonEffect(Effect):
    def __init__(self, player):
        time = 20000
        super().__init__(player, time)

        self.player.add_speed -= 1
        self.healthBar = self.player.health_bar.healthbar
        self.healthBar.change_colour("forestgreen")
        # self.damage_percent = 2 # percent
        self.poison_damage = 5

        self.tick_timer = Clock(1200)
        self.tick_timer.start()
        # self.healthBar.health.set_damage(self.poison_damage) # first tick

    def get_damage(self, percent):
        damage = self.healthBar.health.get_percent(percent)
        return damage

    def update(self):
        if self.tick_timer.next():
            self.healthBar.health.set_damage(self.poison_damage) # directly, without defence        

    def increase(self):
        # no restart
        # if self.player.add_speed > -2:
        #     self.player.add_speed -= 1
        if self.poison_damage < 10:
            self.poison_damage += 2
            self.boost += 1

    def increase_old(self):
        # no restart
        if self.player.add_speed > -2:
            self.player.add_speed -= 1
        if self.damage_percent < 6:
            self.damage_percent += 2
            self.boost += 1
        self.poison_damage = self.get_damage(self.damage_percent)

    def __del__(self):
        self.healthBar.change_colour("red")
        self.player.add_speed = 0

class SpeedEffect(Effect):
    def __init__(self, player):
        time = 6000
        super().__init__(player, time)

        # self.speed_bonus = 1
        # self.default_speed = self.player.speed
        self.increase_speed(2) # boost = 2
        self.boost = 1

    def increase(self):
        super().increase() # restart
        self.increase_speed(2)

    def increase_speed(self, speed):  
        if (self.player.speed + self.player.add_speed) < 10:
            self.player.add_speed += speed
            self.boost += 1
    
    def __del__(self):
        self.player.add_speed = 0

class IronskinEffect(Effect):
    def __init__(self, player):
        time = 8000
        super().__init__(player, time)

        self.default_defence = self.player.defence
        self.player.defence += 60

    def increase(self):
        super().increase()
        # if self.player.defence < 90:
        #     self.player.defence += 10
        #     self.boost += 1
    
    def __del__(self):
        self.player.defence = self.default_defence

class OnepunchEffect(Effect):
    def __init__(self, player):
        time = 8000
        super().__init__(player, time)
        self.player.add_b_speed = 20
        self.player.add_damage = 1000000
    
    def __del__(self):
        self.player.add_b_speed = 0
        self.player.add_damage = 0
        pass

# TODO те ж саме, що і зі StandingEffect
class HarmlessEffect(Effect):
    def __init__(self, player):
        time = 8000
        super().__init__(player, time)

# TODO поки що прив'язаний тільки до гравця
# потрібно створити змінну is_moving у класі Actor
# і завжди звірятися з нею у методах руху дочірніх класів
class StandingEffect(Effect):
    def __init__(self, player):
        time = 1000
        super().__init__(player, time)

class BulletsEffect(Effect):
    def __init__(self, player):
        time = 10000
        super().__init__(player, time)

        self.b_speed_bonus = 3
        self.add_bullet_speed()
        self.boost = 1

    def increase(self):
        super().increase()
        self.add_bullet_speed()

    def add_bullet_speed(self):
        if self.player.add_b_speed < self.b_speed_bonus * 3:
            self.player.add_b_speed += self.b_speed_bonus
            self.boost += 1
    
    def __del__(self):
        self.player.add_b_speed = 0
