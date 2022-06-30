import pygame       as pg
import random

from .characters    import Character
from .treasure_coin import Treasure_Coin
from .treasure_health   import Treasure_Health
from .constants     import *
from .debug         import debug

class Enemy(Character):
    """
    SUBCLASS OF CHARACTER CLASS TO HANDLE ENEMY CREATION AND PATHING
    MOVES TOWARDS PLAYER WHEN WITHIN SPECIFIED RANGE, AND ATTACKS WHEN CLOSE ENOUGH
    ENEMY ART CREDIT: https://pixel-boy.itch.io/ninja-adventure-asset-pack
    """
    def __init__(self, name, position, sprite_groups, obstacle_sprites, target, damage, health):
        super().__init__(name, position, sprite_groups, obstacle_sprites, target, damage, health)
        self.speed = 2
        self.damage = damage
        
        self.target = target.name
        self.target_position = target.rect
        self.targetRange = 250
    
    def input(self):
        """
        FINDS THE PATH TO THE PLAYER IF THE PLAYER IS WITHIN TARGETRANGE
        ONCE CLOSE ENOUGH, WILL ATTEMPT TO ATTACK THE PLAYER
        """
        diffx = self.rect.x - self.target_position.x
        diffy = self.rect.y - self.target_position.y
        diffTotal = abs(diffx) + abs(diffy)
        tollerance = 30
        
        if diffTotal < self.targetRange and (abs(diffx) > tollerance or abs(diffy) > tollerance):
            if diffx > 0:
                self.direction.x = -1
                self.facing = "West"
                self.load_image(self.cycle_west[self.animation_frame])
            elif diffx < 0:
                self.direction.x = 1
                self.facing = "East"
                self.load_image(self.cycle_east[self.animation_frame])
            else:
                self.direction.x = 0
            
            if diffy > 0:
                self.direction.y = -1
                self.facing = "North"
                self.load_image(self.cycle_north[self.animation_frame])
            elif diffy < 0:
                self.direction.y = 1
                self.facing = "South"
                self.load_image(self.cycle_south[self.animation_frame])
            else:
                self.direction.y = 0
        elif diffTotal < self.targetRange:
            self.attacking = True
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.load_image(self.cycle_south[self.animation_frame])


    def check_alive(self):
        """
        IF HEALTH DROPPED BELOW 0, DETERMINE TREASURE TYPE
        DROP CHOSEN TREASURE TYPE
        """
        if self.health <= 0:
            self.kill()
            spawn_chance = random.randrange(0,10)+1
            if spawn_chance >= 3:
                Treasure_Coin(
                    name     = "gold", #ART CREDIT https://pixel-boy.itch.io/ninja-adventure-asset-pack
                    position = (self.rect.x, self.rect.y),
                    sprite_groups = [self.visible_sprites]
                )
            else:
                Treasure_Health(
                    name     = "health", #ART CREDIT https://pixel-boy.itch.io/ninja-adventure-asset-pack
                    position = (self.rect.x, self.rect.y),
                    sprite_groups = [self.visible_sprites]
                )




