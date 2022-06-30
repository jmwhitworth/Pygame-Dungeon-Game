import pygame       as pg
import os

from .constants     import *

class Move_Room(pg.sprite.Sprite):
    """
    STATIC SPRITES FOR TREASURE CHEST
    ON HIT THE STATE CHANGES TO OPEN AND IT SPAWNS RANDOM TREASURE
    ART CREDIT: https://pixel-boy.itch.io/ninja-adventure-asset-pack
    """
    def __init__(self, name, position, sprite_groups, level):
        super().__init__(sprite_groups)
        
        self.name = name
        self.visible_sprites = sprite_groups[0]
        self.level = level
        
        self.load_image()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
    
    def load_image(self):
        self.image = pg.image.load(os.path.join("assets", "blank.png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (32,32)) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
    
    def update(self):
        self.check_collision()
    
    def check_collision(self):
        for sprite in self.visible_sprites:
            try:
                if sprite.hitbox.colliderect(self.rect):
                    if sprite.name == "player":
                        print(f"Current room: {self.level.current_room}. Going to: {self.name}")
                        self.level.save_room_state(self.level.current_room)
                        self.level.save_player_state()
                        self.level.create_map(int(self.name))
            except AttributeError:
                pass