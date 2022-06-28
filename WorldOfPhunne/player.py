import pygame       as pg
import os

from .constants      import *
from .debug          import debug

class Player(pg.sprite.Sprite):
    """
    CLASS FOR MANAGING PLAYER CHARACTER
        - MONITORS USER INPUT
        - MOVES PLAYER BASED ON GIVEN INPUTS
        - HANDLES COLLISION WITH OBSTACLE SPRITES
    """
    def __init__(self, position, sprite_groups,obstacle_sprites):
        super().__init__(sprite_groups)
        self.load_image("player/idle.png")
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-10,-20)
        
        self.direction = pg.math.Vector2()
        self.facing = "South"
        self.speed = 4
        self.animation_interval = FPS/8
        self.counter = [0, 0] #Interval count, Count
        
        self.obstacle_sprites = obstacle_sprites
        
        self.cycle_north = ["player/walk_n_1.png","player/walk_n_2.png","player/walk_n_3.png","player/walk_n_2.png"]
        self.cycle_south = ["player/walk_s_1.png","player/walk_s_2.png","player/walk_s_3.png","player/walk_s_2.png"]
        self.cycle_east = ["player/walk_e_1.png","player/walk_e_2.png","player/walk_e_3.png","player/walk_e_2.png"]
        self.cycle_west = ["player/walk_w_1.png","player/walk_w_2.png","player/walk_w_3.png","player/walk_w_2.png"]
    
    def load_image(self, image_file_name, size=(30,32)):
        self.image = pg.image.load(os.path.join("assets", image_file_name)).convert_alpha()
        self.image = pg.transform.scale(self.image, size) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
    
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
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #STOP DIAGANALS BEING TOO FAST
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('verticle')
        self.rect.center = self.hitbox.center
    
    def collision(self,direction):
        """
        GO THROUGH ALL OBSTACLES AND IF PLAYER COLLIDES,
        SET PLAYER EDGE TO LINE UP WITH THE OPPOSING EDGE OF OBSTACLE
        """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #MOVING RIGHT
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #MOVING LEFT
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == 'verticle':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #MOVING DOWN
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #MOVING UP
                        self.hitbox.top = sprite.hitbox.bottom
    
    def increment_animations(self):
        """
        SETS A VARIABLE TO AN INT FROM 1-4 WHICH IS USED TO DETERMINE WHICH IMAGE IS LOADED IN ANIMATIONS
        ANIMATION INTERVAL DETERMINS HOW FAST THE ANIMATION CYCLES IN FPS
        """
        self.counter[0] += 1
        if self.counter[0] >= self.animation_interval:
            self.counter[1] = (self.counter[1] +1) % 4
            self.counter[0] = 0
    
    def update(self):
        self.input()
        self.move(self.speed)
        self.increment_animations()
