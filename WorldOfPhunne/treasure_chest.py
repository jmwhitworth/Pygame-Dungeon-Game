import pygame       as pg
import os
import random

from .constants     import *
from .hit_flash     import Hit_Flash
from .treasure_gem  import Treasure_Gem
from .sounds         import *

class Treasure_Chest(pg.sprite.Sprite):
    """
    STATIC SPRITES FOR TREASURE CHEST
    ON HIT THE STATE CHANGES TO OPEN AND IT SPAWNS RANDOM TREASURE
    ART CREDIT: https://pixel-boy.itch.io/ninja-adventure-asset-pack
    """
    def __init__(self, name, position, sprite_groups, health):
        super().__init__(sprite_groups)
        
        self.health = health
        self.visible_sprites = sprite_groups[0]
        
        #ROLL FOR LOOT TYPE TO SPAWN
        self.contents = random.randrange(0,2)
        self.treasures = {
            0: "ruby",
            1: "diamond"
        }
        
        self.name = name
        if self.health == 1:
            self.load_image("treasure_chest/closed.png")
        else:
            self.load_image("treasure_chest/open.png")

        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)
    
    def load_image(self, image_file_name):
        self.image = pg.image.load(os.path.join("assets/treasure", image_file_name)).convert_alpha()
        self.image = pg.transform.scale(self.image, (32,32)) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
    
    def hit(self, damage):
        """
        APPLY DAMAGE TO HEALTH AND CREATE HIT ANIMATION ON SELF
        """
        self.health -= damage
        Hit_Flash([self.visible_sprites], (self.rect.centerx, self.rect.centery+1))
        self.check_alive()
    
    def check_alive(self):
        """
        IF HEALTH < 0: CHANGE SPRITE TO OPEN CHEST AND SPAWN LOOT BELOW CHEST
        """
        if self.health <= 0:
            self.load_image("treasure_chest/open.png")
        Treasure_Gem(
                name     = self.treasures[self.contents], #ART CREDIT https://pixel-boy.itch.io/ninja-adventure-asset-pack
                position = (self.rect.x, self.rect.y+20),
                sprite_groups = [self.visible_sprites]
            )
        pg.mixer.Sound.play(sound_bonus)

    def get_info(self):
        data = {
            "Health": self.health,
            "Position X": self.rect.x,
            "Position Y": self.rect.y,
        }
        return data