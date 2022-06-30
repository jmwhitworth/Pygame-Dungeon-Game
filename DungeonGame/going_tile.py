import pygame       as pg
import os

from .constants     import *

class Going_Tile(pg.sprite.Sprite):
    """
    STATIC SPRITES FOR TREASURE CHEST
    ON HIT THE STATE CHANGES TO OPEN AND IT SPAWNS RANDOM TREASURE
    """
    def __init__(self, name, position, sprite_groups):
        super().__init__(sprite_groups)
        
        self.visible_sprites = sprite_groups[0]
        self.name = name
        
        self.load_image("blank.png")
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect
    
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
                        sprite.going = self.name
            except AttributeError:
                pass