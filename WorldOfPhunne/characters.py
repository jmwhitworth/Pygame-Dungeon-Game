import pygame       as pg
import os

from .constants     import *
from .debug         import debug
from .attack        import Attack
from .hit_flash     import Hit_Flash

class Character(pg.sprite.Sprite):
    """
    CLASS FOR MANAGING CHARACTERS
        - MOVEMENT
        - COLLISION WITH OBSTACLE SPRITES
        - ANIMATION CYCLING
    """
    def __init__(self, name, position, sprite_groups, obstacle_sprites, target, damage, health, gold=0):
        super().__init__(sprite_groups)
        
        self.health = health
        self.name = name
        self.target = target
        self.damage = damage
        self.direction = pg.math.Vector2()
        self.facing = "South" #DETERMINES IDLE SPRITE
        self.going = "South" #DETEMINES ENTRY POINT OF NEXT ROOM
        self.speed = 1
        self.visible_sprites = sprite_groups[0]
        self.gold = gold
        
        self.animation_interval = 100 #FREQUENCY TO CHANGE ANIMATION FRAME IN MS
        self.last_animation_change = 0 #GAME TICK OF LAST CHANGE
        self.animation_frame = 0 #CURRENT ANIMATION FRAME TO USE (0-3)
        
        self.attacking = False
        self.attack_cooldown = 500 #TIME IN MS UNTIL PLAYER CAN ATTACK AGAIN
        self.attack_animation_duration = 200 #TIME IN MS TO SHOW ATTACK FRAME
        self.last_attack_frame = 0
        
        self.load_animations()
        self.load_image(self.cycle_south[1], forced=True)
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(-10,-20) #MAKE HITBOX SMALLER THAN SPRITE FOR MOVEMENT AND COMBAT
        
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
    
    def load_image(self, image_file_name, size=(30,32), forced=False):
        current_tick = pg.time.get_ticks()
        if current_tick - self.last_attack_frame >= self.attack_animation_duration or forced:
            self.image = pg.image.load(os.path.join("assets/characters", image_file_name)).convert_alpha()
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
        if self.attacking:
            current_tick = pg.time.get_ticks()
            if current_tick - self.last_attack_frame >= self.attack_cooldown:
                self.load_image(f"{self.name}/attack_{self.facing}.png", forced=True) #LOAD APPROPRIATE ATTACK SPRITE
                
                #OFFSET THE SPRITE TO SPAWN IN THE DIRECTION PLAYER IS FACING
                if self.facing == "North":
                    attack_position = (self.rect.x, self.rect.y - self.rect.height)
                elif self.facing == "South":
                    attack_position = (self.rect.x, self.rect.y + self.rect.height)
                elif self.facing == "East":
                    attack_position = (self.rect.x + self.rect.width, self.rect.y)
                elif self.facing == "West":
                    attack_position = (self.rect.x - self.rect.width, self.rect.y)
                
                Attack([self.visible_sprites], attack_position, self.attack_animation_duration, self.visible_sprites, [self.target, "treasure_chest"], self.damage)
                
                self.last_attack_frame = current_tick
        self.attacking = False
    
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
        current_tick = pg.time.get_ticks()
        if current_tick - self.last_animation_change >= self.animation_interval:
            
            #KEEP ANIMATION FRAME WITHIN 0-3 
            if self.animation_frame >= 3:
                self.animation_frame = 0
            else:
                self.animation_frame += 1
            
            self.last_animation_change = current_tick
    
    def hit(self, damage):
        self.health -= damage
        Hit_Flash([self.visible_sprites], (self.rect.centerx, self.rect.centery+1))
        self.check_alive()
    
    def check_alive(self):
        if self.health <= 0:
            self.kill()
    
    def add_health(self, hp):
        self.health += hp
        if self.health > 100:
            self.health = 100
    
    def get_info(self):
        data = {
            "Health": self.health,
            "Position X": self.rect.x,
            "Position Y": self.rect.y,
        }
        if self.name == "player":
            data["Gold"] = self.gold
            data["Going"] = self.going
        return data
    
    def update(self):
        self.input()
        self.move()
        self.attack()
        self.increment_animations()
        
        if self.name == "player":
            self.display_stats()
