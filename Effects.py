import pygame
# from HealthBar import Health
from HealthBar import HealthBar
from Clock_class import Clock

class EffectQueue:
    def __init__(self, player):
        self.player = player
        self.queue = {}

    def add(self, effect_key):
        if not self.queue.get(effect_key):
            effect = self.createEffect(effect_key)
            if effect:
                self.queue[effect_key] = effect
                print(effect_key, "added to queue")
            else:
                print(effect_key, "not valid key")
        else: 
            self.queue[effect_key].increase()
            print(effect_key, "increased")

    def remove(self, effect_key):
        self.queue.pop(effect_key)
        print(effect_key, "removed")

    def remove(self, effect_keys : list):
        for key in effect_keys:
            self.queue.pop(key)
            print(key, "removed")

    def update(self):
        del_keys = []
        for key in self.queue.keys():
            self.queue[key].update()

            if self.queue[key].off():
                del_keys.append(key)

        if del_keys:
            self.remove(del_keys)

    def clear(self):
        self.queue.clear()

    def createEffect(self, effect_key):
        effect = None
        if effect_key == "poison":
            effect = PoisonEffect(self.player)
        if effect_key == "speed":
            effect = SpeedEffect(self.player)
        return effect

class PoisonEffect:
    def __init__(self, player):
        self.healthBar = player.health_bar
        self.healthBar.change_colour("forestgreen")
        self.default_damage = 2
        self.poison_damage = self.default_damage

        self.timer = Clock(20000)
        self.tick_timer = Clock(900)
        self.timer.start()
        self.tick_timer.start()

    def update(self):
        if self.tick_timer.isNextFrame():
            self.healthBar.health.set_damage(self.poison_damage)    

    def off(self):
        if self.timer.end():
            return True
        return False
    
    def time(self):
        return self.timer.time()
    
    def increase(self):
        self.poison_damage += self.default_damage
        # self.timer.restart()

    def __del__(self):
        self.healthBar.change_colour("red")

class SpeedEffect:
    def __init__(self, player):
        self.player = player
        self.speed_bonus = 3
        self.default_speed = self.player.speed
        self.player.speed += self.speed_bonus

        self.timer = Clock(4000)
        self.timer.start()

    def time(self):
        return self.timer.time()    

    def update(self):
        ...
    
    def off(self):
        if self.timer.end():
            return True
        return False

    def increase(self):
        self.player.speed += self.speed_bonus
        self.timer.restart()
    
    def __del__(self):
        self.player.speed = self.default_speed
