import pygame       as pg
import os

from .constants      import *

class Tile(pg.sprite.Sprite):
    """
    STATIC SPRITES FOR OBSTACLES
    """
    def __init__(self, name, position, sprite_groups):
        super().__init__(sprite_groups)
        self.name = name
        self.load_image(f"{self.name}.png")
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
    
    def load_image(self, image_file_name, size=(32,32)):
        self.image = pg.image.load(os.path.join("assets", image_file_name)).convert_alpha()
        self.image = pg.transform.scale(self.image, size) #SCALE THE 16X16 IMAGE TO GIVEN SIZE