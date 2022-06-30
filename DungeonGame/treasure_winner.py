import pygame       as pg
import os

from .constants     import *
from .sounds         import *

class Treasure_Winner(pg.sprite.Sprite):
    """
    MAIN TREASURE THAT ENDS THE GAME ON COLLECTION
    ART CREDIT: https://pixel-boy.itch.io/ninja-adventure-asset-pack
    """
    def __init__(self, name, position, sprite_groups, level):
        super().__init__(sprite_groups)
        
        self.visible_sprites = sprite_groups[0]
        self.name = name
        self.value = 100
        
        self.level = level
        
        self.load_image("winner_gem.png")
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
    
    def load_image(self, image_file_name):
        self.image = pg.image.load(resource_path(os.path.join("assets/treasure", image_file_name))).convert_alpha()
        self.image = pg.transform.scale(self.image, (32,32)) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
    
    def update(self):
        self.pick_up()
    
    def pick_up(self):
        for sprite in self.visible_sprites:
            try:
                if sprite.hitbox.colliderect(self.rect):
                    if sprite.name == "player":
                        sprite.gold += self.value
                        pg.mixer.Sound.play(sound_coin)
                        self.kill()
                        self.level.complete = True
            except AttributeError:
                pass