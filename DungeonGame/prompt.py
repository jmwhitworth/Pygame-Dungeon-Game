import pygame as pg
from .constants import *

pg.init()
font = pg.font.Font(None,60)

"""
DISPLAYS INFORMATION PASSED TO IT ON THE GIVEN X & Y COORDINATES
"""

class Prompt(pg.sprite.Sprite):
    """
    FLASHING SPRITE THAT IS CREATED WHEN CHARACTER IS HIT
    CYCLES THROUGH 5 ANIMATION STAGES OVER SPECIFIED DURATION, DEFAULT 100MS
    ANIMATION CREDIT: https://marketplace.yoyogames.com/assets/7007/pixel-art-hit-effect
    """
    def __init__(self, sprite_groups, info, colour):
        super().__init__(sprite_groups)
        self.duration = 1000 #TIME IN MS THAT FLASH SHOWS FOR
        
        self.spawn_time = pg.time.get_ticks()
        self.is_alive = True
        self.info = info
        self.colour = colour
        
        self.x=SCREENHEIGHT/2
        self.y=(SCREENWIDTH-200)/2
    
    def show(self):
        display_surface = pg.display.get_surface()
        debug_surf = font.render(str(self.info),True,'white')
        debug_rect = debug_surf.get_rect(center=(self.x,self.y))
        pg.draw.rect(display_surface,self.colour,debug_rect)
        display_surface.blit(debug_surf,debug_rect)
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time <= self.duration:      
            self.show()
        else:
            self.is_alive = False
            self.kill()
