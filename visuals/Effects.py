import pygame
from pygame.math import Vector2
import visuals.HealthBar as HealthBar
from add.Clock import Clock

class EffectQueue:
    def __init__(self, player):
        self.player = player
        self.queue = {}
        # self.isDraw = False

    def add(self, effect_key):
        if not self.queue.get(effect_key):
            effect = self.createEffect(effect_key)
            if effect:
                self.queue[effect_key] = effect
                # print(effect_key, "added to queue")
            # else:
            #     print(effect_key, "not valid key")
        else: 
            self.queue[effect_key].increase()
            # print(effect_key, "increased")

    def remove(self, key):
        self.queue[key].__del__()
        self.queue.pop(key)
        # print(key, "removed")

    # def check_old(self):
    #     del_keys = []
    #     for key in self.queue.keys():
    #         if self.queue[key].off():
    #             del_keys.append(key)

    #     if del_keys:
    #         for key in del_keys:
    #             self.remove(key)

    def check(self):
        for key in list(self.queue.keys()):
            if self.queue[key].off():
                self.remove(key)

    def update(self):
        self.check() # +cycle

        # for key in self.queue.keys():
        #     self.queue[key].update()
        for effect in self.queue.values():
            effect.update()

    def draw(self, screen):
        ...

    def clear(self):
        for effect in self.queue.values():
            effect.__del__()
        self.queue.clear() # does not call effect destructors of effects

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
        if effect_key == "standing":
            effect = StandingEffect(self.player)
        return effect

class EffectQueue_draw(EffectQueue):
    def __init__(self, player):
        super().__init__(player)

    def add(self, key):
        super().add(key)

        if not self.queue[key].effect_bar:
            # warning! cyclic references
            # GC will not delete this object while it is referenced
            self.queue[key].effect_bar = HealthBar.EffectBar(self.queue[key])     

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

    def update(self):
        ...

    def increase(self):
        ...

    def off(self):
        if self.timer.end():
            return True
        return False

    def time(self):
        return self.timer.time()

    def duration(self):
        return self.timer.delay

class PoisonEffect(Effect):
    def __init__(self, player):
        time = 20000
        super().__init__(player, time)

        self.healthBar = self.player.health_bar.healthbar
        self.healthBar.change_colour("forestgreen")
        self.default_damage = 2
        self.poison_damage = self.default_damage

        self.tick_timer = Clock(900)
        self.tick_timer.start()

    def update(self):
        if self.tick_timer.isNextFrame():
            self.healthBar.health.set_damage(self.poison_damage) # directly, without defence        
 
    def increase(self):
        self.poison_damage += self.default_damage
        # self.timer.restart()

    def __del__(self):
        self.healthBar.change_colour("red")

class SpeedEffect(Effect):
    def __init__(self, player):
        time = 6000
        super().__init__(player, time)

        self.speed_bonus = 2
        self.default_speed = self.player.speed
        self.player.speed += self.speed_bonus

    def increase(self):
        self.player.speed += self.speed_bonus - 1
        self.timer.restart()
    
    def __del__(self):
        self.player.speed = self.default_speed

class IronskinEffect(Effect):
    def __init__(self, player):
        time = 8000
        super().__init__(player, time)

        self.default_defence = self.player.defence
        self.player.defence += 60

    def increase(self):
        if self.player.defence < 90:
            self.player.defence += 10
        self.timer.restart()
    
    def __del__(self):
        self.player.defence = self.default_defence

class OnepunchEffect(Effect):
    def __init__(self, player):
        time = 8000
        super().__init__(player, time)

        self.player.onepunch = True

    def increase(self):
        self.timer.restart()
    
    def __del__(self):
        self.player.onepunch = False

class HarmlessEffect(Effect):
    def __init__(self, player):
        time = 8000
        super().__init__(player, time)

        self.player.harmless = True

    def increase(self):
        self.timer.restart()
    
    def __del__(self):
        self.player.harmless = False

class StandingEffect(Effect):
    def __init__(self, player):
        time = 5000
        super().__init__(player, time)

        self.player.standing = True

    def increase(self):
        self.timer.restart()
    
    def __del__(self):
        self.player.standing = False
