import pygame       as pg
import os

from .constants     import *
from .sounds         import *

class Treasure_Gem(pg.sprite.Sprite):
    """
    STATIC SPRITES FOR TREASURE CHEST
    ON HIT THE STATE CHANGES TO OPEN AND IT SPAWNS RANDOM TREASURE
    ART CREDIT: https://laredgames.itch.io/gems-coins-free
    """
    def __init__(self, name, position, sprite_groups):
        super().__init__(sprite_groups)
        
        self.visible_sprites = sprite_groups[0]
        self.name = name
        self.value = {
            "ruby": 10,
            "diamond": 20
        }
        
        self.spawn_time = pg.time.get_ticks()
        self.last_animation_change = self.spawn_time
        self.animation_frame = 0
        self.animation_interval = 100 #FREQUENCY TO CHANGE ANIMATION FRAME IN MS
        self.animation_frames = ["1.png", "2.png", "3.png", "4.png"]

        self.load_image(self.animation_frames[self.animation_frame])
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
    
    def load_image(self, image_file_name):
        self.image = pg.image.load(os.path.join(f"assets/treasure/{self.name}", image_file_name)).convert_alpha()
        self.image = pg.transform.scale(self.image, (32,32)) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
    
    def update(self):
        """
        CYCLE THROUGH ANIMATION FRAMES AND CHECK IF PICKED UP
        """
        current_tick = pg.time.get_ticks()
        if current_tick - self.last_animation_change >= self.animation_interval:
            
            #KEEP ANIMATION FRAME WITHIN 0-3 
            if self.animation_frame >= 3:
                self.animation_frame = 0
            else:
                self.animation_frame += 1
            
            self.last_animation_change = current_tick
        
        self.load_image(self.animation_frames[self.animation_frame])
        self.pick_up()
    
    def pick_up(self):
        for sprite in self.visible_sprites:
            try:
                if sprite.hitbox.colliderect(self.rect):
                    if sprite.name == "player":
                        sprite.gold += self.value[self.name]
                        pg.mixer.Sound.play(sound_gold)
                        self.kill()
            except AttributeError:
                pass