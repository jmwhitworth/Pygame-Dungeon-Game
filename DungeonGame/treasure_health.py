import pygame       as pg
import os

from .constants     import *
from .sounds         import *

class Treasure_Health(pg.sprite.Sprite):
    """
    STATIC SPRITES FOR TREASURE CHEST
    ON HIT THE STATE CHANGES TO OPEN AND IT SPAWNS RANDOM TREASURE
    """
    def __init__(self, name, position, sprite_groups):
        super().__init__(sprite_groups)
        
        self.visible_sprites = sprite_groups[0]
        self.name = name
        self.value = 50
        
        self.spawn_time = pg.time.get_ticks()
        self.last_animation_change = self.spawn_time
        self.animation_frame = 0
        self.animation_interval = 100 #FREQUENCY TO CHANGE ANIMATION FRAME IN MS
        
        self.load_image("health_kit.png")
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
    
    def load_image(self, image_file_name):
        self.image = pg.image.load(resource_path(os.path.join("assets", image_file_name))).convert_alpha()
        self.image = pg.transform.scale(self.image, (32,32)) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
    
    def update(self):
        self.pick_up()
    
    def pick_up(self):
        for sprite in self.visible_sprites:
            try:
                if sprite.hitbox.colliderect(self.rect):
                    if sprite.name == "player":
                        sprite.add_health(self.value)
                        pg.mixer.Sound.play(sound_bonus)
                        self.kill()
            except AttributeError:
                pass