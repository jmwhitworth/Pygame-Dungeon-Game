import pygame       as pg
import os

from .characters    import Character
from .constants     import *
from .debug         import debug

class Player(Character):
    """
    SUBCLASS OF CHARACTER FOR THE GAMES PLAYER
    HANDLES USER INPUT TO CONTROL THE CHARACTER ONSCREEN
    PLAYER ART CREDIT: https://pixel-boy.itch.io/ninja-adventure-asset-pack
    """
    def __init__(self, name, position, sprite_groups, obstacle_sprites, target, damage, health, gold):
        super().__init__(name, position, sprite_groups, obstacle_sprites, target, damage, health, gold)
        self.speed = 4
    
    def input(self):
        keys = pg.key.get_pressed()
        
        #IF UP/DOWN KEYS ARE PRESSED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction.y = -1
            self.facing = "North"
            self.load_image(self.cycle_north[self.animation_frame])
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction.y = 1
            self.facing = "South"
            self.load_image(self.cycle_south[self.animation_frame])
        else:
            self.direction.y = 0
        
        #IF RIGHT/LEFT KEYS ARE PRESSED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction.x = 1
            self.facing = "East"
            self.load_image(self.cycle_east[self.animation_frame])
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction.x = -1
            self.facing = "West"
            self.load_image(self.cycle_west[self.animation_frame])
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
        
        #CHECK IF CHARACTER IS ATTACKING
        if keys[pg.K_SPACE]:
            self.attacking = True
    
    def display_stats(self):
        #DISPLAY HEALTH
        debug(f"Health: {self.health}", x=10, y=SCREENHEIGHT-30)
        debug(f"Gold: {self.gold}", x=SCREENWIDTH-100, y=SCREENHEIGHT-30)
        debug(f"{self.rect.x}, {self.rect.y}", x=SCREENWIDTH-100, y=10)
        debug(f"{self.going}", x=SCREENWIDTH-100, y=40)

    def check_alive(self):
        if self.health <= 0:
            self.kill()