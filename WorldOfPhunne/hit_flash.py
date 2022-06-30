import pygame       as pg
import os

from .constants     import *
from .debug         import debug
from .sounds         import *

class Hit_Flash(pg.sprite.Sprite):
    """
    FLASHING SPRITE THAT IS CREATED WHEN CHARACTER IS HIT
    CYCLES THROUGH 5 ANIMATION STAGES OVER SPECIFIED DURATION, DEFAULT 100MS
    ANIMATION CREDIT: https://marketplace.yoyogames.com/assets/7007/pixel-art-hit-effect
    """
    def __init__(self, sprite_groups, position):
        super().__init__(sprite_groups)
        self.duration = 100 #TIME IN MS THAT FLASH SHOWS FOR
        
        self.spawn_time = pg.time.get_ticks()
        
        self.animation_frames = ["hit/1.png", "hit/2.png", "hit/3.png", "hit/4.png", "hit/5.png"]
        self.load_image(self.animation_frames[0])
        self.rect = self.image.get_rect(center = position)
        
        pg.mixer.Sound.play(sound_hit)
    
    def load_image(self, image_file_name, size=(48,48)):
        self.image = pg.image.load(os.path.join("assets/effects", image_file_name)).convert_alpha()
        self.image = pg.transform.scale(self.image, size) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
    
    def update(self):
        """
        CYCLE THROUGH ALL ANIMATION FRAMES THEN REMOVE ITSELF
        """
        current_tick = pg.time.get_ticks()
        alive_time = current_tick - self.spawn_time
        if alive_time <= (self.duration/5)*1:
            self.load_image(self.animation_frames[0])
        elif alive_time <= (self.duration/5)*2:
            self.load_image(self.animation_frames[1])
        elif alive_time <= (self.duration/5)*3:
            self.load_image(self.animation_frames[2])
        elif alive_time <= (self.duration/5)*4:
            self.load_image(self.animation_frames[3])
        elif alive_time <= self.duration:
            self.load_image(self.animation_frames[4])
        else:
            self.kill()
