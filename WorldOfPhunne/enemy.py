import pygame       as pg
import random

from .characters    import Character
from .constants     import *
from .debug         import debug

class Enemy(Character):
    def __init__(self, position, sprite_groups, obstacle_sprites, target):
        super().__init__(position, sprite_groups, obstacle_sprites)
        self.speed = 2

        self.target = target
        self.targetRange = 250
    
    def load_animations(self):
        self.cycle_north = ["enemy/walk_n_1.png", "enemy/walk_n_2.png", "enemy/walk_n_3.png", "enemy/walk_n_2.png"]
        self.cycle_south = ["enemy/walk_s_1.png", "enemy/walk_s_2.png", "enemy/walk_s_3.png", "enemy/walk_s_2.png"]
        self.cycle_east  = ["enemy/walk_e_1.png", "enemy/walk_e_2.png", "enemy/walk_e_3.png", "enemy/walk_e_2.png"]
        self.cycle_west  = ["enemy/walk_w_1.png", "enemy/walk_w_2.png", "enemy/walk_w_3.png", "enemy/walk_w_2.png"]
    
    def input(self):
        diffx = self.rect.x - self.target.rect.x
        diffy = self.rect.y - self.target.rect.y
        diffTotal = abs(diffx) + abs(diffy)
        tollerance = 10
        
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

    def attack(self):
        if self.attackCooldown > 0:
            self.attackCooldown -= 1
        if self.attacking and self.attackCooldown == 0:
            if self.facing == "North":
                self.load_image("enemy/attack_n.png")
            elif self.facing == "South":
                self.load_image("enemy/attack_s.png")
            elif self.facing == "East":
                self.load_image("enemy/attack_e.png")
            elif self.facing == "West":
                self.load_image("enemy/attack_w.png")
            self.attackCooldown = int(FPS/10 + 10)
        self.attacking = False