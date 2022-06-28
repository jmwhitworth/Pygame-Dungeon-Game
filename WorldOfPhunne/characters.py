import pygame       as pg
import os

from .constants      import *
from .debug          import debug

class Character(pg.sprite.Sprite):
    """
    CLASS FOR MANAGING CHARACTERS
        - MOVEMENT
        - COLLISION WITH OBSTACLE SPRITES
        - ANIMATION CYCLING
    """
    def __init__(self, name, position, sprite_groups, obstacle_sprites):
        super().__init__(sprite_groups)
        
        self.name = name
        self.direction = pg.math.Vector2()
        self.facing = "South" #DETERMINES IDLE SPRITE
        self.speed = 1
        self.animation_interval = FPS/8 #SPEED TO ROTATE ANIMATE FRAME
        self.counter = [0, 0] #INTERVAL COUNT, COUNT
        self.attacking = False #IS CHARACTER ATTACKING
        self.attackCooldown = 0 #FRAMES UNTIL CAN ATTACK AGAIN
        
        self.load_animations()
        self.load_image(self.cycle_south[1])
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-10,-20)
        
        self.obstacle_sprites = obstacle_sprites
    
    def load_animations(self):
        """
        ALL ANIMATION CYCLE LISTS MUST HAVE LENGTH OF 4
        """
        self.cycle_north = [f"{self.name}/walk_North_1.png", f"{self.name}/walk_North_2.png", f"{self.name}/walk_North_3.png", f"{self.name}/walk_North_2.png"]
        self.cycle_south = [f"{self.name}/walk_South_1.png", f"{self.name}/walk_South_2.png", f"{self.name}/walk_South_3.png", f"{self.name}/walk_South_2.png"]
        self.cycle_east  = [f"{self.name}/walk_East_1.png", f"{self.name}/walk_East_2.png", f"{self.name}/walk_East_3.png", f"{self.name}/walk_East_2.png"]
        self.cycle_west  = [f"{self.name}/walk_West_1.png", f"{self.name}/walk_West_2.png", f"{self.name}/walk_West_3.png", f"{self.name}/walk_West_2.png"]
    
    def input(self):
        """
        THIS WILL BE AI TO DETERMINE OUTPUT VECTOR
        """
        pass
    
    def load_image(self, image_file_name, size=(30,32)):
        if self.attackCooldown <= 10: #ONLY CHANGE IMAGE IF CHARACTER ISN'T ATTACKING
            self.image = pg.image.load(os.path.join("assets", image_file_name)).convert_alpha()
            self.image = pg.transform.scale(self.image, size) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
    
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #STOP DIAGANALS BEING TOO FAST
        
        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed
        self.collision('verticle')
        self.rect.center = self.hitbox.center
    
    def attack(self):
        if self.attackCooldown > 0:
            self.attackCooldown -= 1
        elif self.attacking:
            self.load_image(f"{self.name}/attack_{self.facing}.png")
            print(self.check_hit(self.facing)) #GET SPRITE OF CHARACTER HIT
            self.attackCooldown = int(FPS/10 + 10) #RESET COOLDOWN
        self.attacking = False
    
    def check_hit(self, direction):
        return f"{self.name} hit {direction}"
    
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
        self.move()
        self.attack()
        self.increment_animations()
