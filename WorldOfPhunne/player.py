import pygame       as pg
import os

from .characters    import Character
from .constants     import *
from .debug         import debug

class Player(Character):
    def __init__(self, position, sprite_groups, obstacle_sprites):
        super().__init__(position, sprite_groups, obstacle_sprites)
    
    def load_animations(self):
        self.cycle_north = ["player/walk_n_1.png","player/walk_n_2.png","player/walk_n_3.png","player/walk_n_2.png"]
        self.cycle_south = ["player/walk_s_1.png","player/walk_s_2.png","player/walk_s_3.png","player/walk_s_2.png"]
        self.cycle_east  = ["player/walk_e_1.png","player/walk_e_2.png","player/walk_e_3.png","player/walk_e_2.png"]
        self.cycle_west  = ["player/walk_w_1.png","player/walk_w_2.png","player/walk_w_3.png","player/walk_w_2.png"]
    
    def input(self):
        keys = pg.key.get_pressed()
        
        #IF UP/DOWN KEYS ARE PRESSED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction.y = -1
            self.facing = "North"
            self.load_image(self.cycle_north[self.counter[1]])
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction.y = 1
            self.facing = "South"
            self.load_image(self.cycle_south[self.counter[1]])
        else:
            self.direction.y = 0
        
        #IF RIGHT/LEFT KEYS ARE PRESSED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction.x = 1
            self.facing = "East"
            self.load_image(self.cycle_east[self.counter[1]])
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction.x = -1
            self.facing = "West"
            self.load_image(self.cycle_west[self.counter[1]])
        else:
            self.direction.x = 0
        
        #IF NO KEYS ARE PRESSED USE IDLE IMAGE OF THAT DIRECTION
        if self.direction.x == 0 and self.direction.y == 0:
            if self.facing == "North":
                self.load_image(self.cycle_north[1])
            elif self.facing == "South":
                self.load_image(self.cycle_south[1])
            elif self.facing == "East":
                self.load_image(self.cycle_east[1])
            elif self.facing == "West":
                self.load_image(self.cycle_west[1])
        
        if keys[pg.K_SPACE]:
            self.attacking = True
    
    def attack(self):
        if self.attackCooldown > 0:
            self.attackCooldown -= 1
        if self.attacking and self.attackCooldown == 0:
            if self.facing == "North":
                self.load_image("player/attack_n.png")
            elif self.facing == "South":
                self.load_image("player/attack_s.png")
            elif self.facing == "East":
                self.load_image("player/attack_e.png")
            elif self.facing == "West":
                self.load_image("player/attack_w.png")
            self.attackCooldown = int(FPS/10 + 10)
        self.attacking = False
