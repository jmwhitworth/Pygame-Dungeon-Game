import pygame       as pg
import random

from .characters    import Character
from .constants     import *
from .debug         import debug

class Enemy(Character):
    def __init__(self, name, position, sprite_groups, obstacle_sprites, target):
        super().__init__(name, position, sprite_groups, obstacle_sprites)
        self.speed = 2
        
        self.target = target
        self.targetRange = 250
    
    def input(self):
        diffx = self.rect.x - self.target.rect.x
        diffy = self.rect.y - self.target.rect.y
        diffTotal = abs(diffx) + abs(diffy)
        tollerance = 20
        
        if diffTotal < self.targetRange and (abs(diffx) > tollerance or abs(diffy) > tollerance):
            if diffx > 0:
                self.direction.x = -1
                self.facing = "West"
                self.load_image(self.cycle_west[self.counter[1]])
            elif diffx < 0:
                self.direction.x = 1
                self.facing = "East"
                self.load_image(self.cycle_east[self.counter[1]])
            else:
                self.direction.x = 0
            
            if diffy > 0:
                self.direction.y = -1
                self.facing = "North"
                self.load_image(self.cycle_north[self.counter[1]])
            elif diffy < 0:
                self.direction.y = 1
                self.facing = "South"
                self.load_image(self.cycle_south[self.counter[1]])
            else:
                self.direction.y = 0
        elif diffTotal < self.targetRange:
            self.attacking = True
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.load_image(self.cycle_south[self.counter[1]])
