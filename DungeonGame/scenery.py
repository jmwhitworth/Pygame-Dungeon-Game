import pygame       as pg
import os

from .constants      import *

class Scenery(pg.sprite.Sprite):
    """
    STATIC SPRITES FOR OBSTACLES
    ART CREDIT: https://pixel-boy.itch.io/ninja-adventure-asset-pack
    """
    def __init__(self, name, position, sprite_groups, size=(32,32)):
        super().__init__(sprite_groups)
        self.name = name
        self.size = size
        self.load_image(f"{self.name}.png", self.size)
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
    
    def load_image(self, image_file_name, size):
        self.image = pg.image.load(resource_path(os.path.join("assets/scenery", image_file_name))).convert_alpha()
        self.image = pg.transform.scale(self.image, size) #SCALE THE 16X16 IMAGE TO GIVEN SIZE