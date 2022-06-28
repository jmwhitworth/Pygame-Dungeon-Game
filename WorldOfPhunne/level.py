import pygame as pg
import os

from .constants import *
from .tile import Tile
from .player import Player
from .debug import debug

class Level():
    """
    - LOADS THE MAP DATA
    - PLACES ALL SPRITES
    - CALLS UPDATE METHOD
    """
    def __init__(self):
        
        #SET UP SPRITE GROUPS
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()
        
        #GETS GAME SURFACE WITHOUT NEEDING TO PASS AS ARG
        self.display_surface = pg.display.get_surface()
        
        self.create_map()
    
    def create_map(self, level=1):
        #LOAD THE LEVEL FILE PASSED AS PARAMETER
        with open(os.path.join("WorldOfPhunne/rooms", f"{level}.txt"), 'r') as level_file:
            world_map = level_file.readlines()
        
        for row_index, row in enumerate(world_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col.lower() == 'x':
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                if col.lower() == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
    
    def run(self):
        #DRAW ALL VISIBLE SPRITES
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pg.sprite.Group):
    """
    CUSTOM SPRITE GROUP CLASS TO:
        - ORDER SPRITES BY THEIR Y COORDINATE SO OVERLAP IS CORRECT
        - CREATE A CAMERA BY OFFSETTING VISIBLE SPRITES BASED ON PLAYER POSITION
    """
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width      = SCREENWIDTH//2
        self.half_height     = SCREENHEIGHT//2
        self.offset          = pg.math.Vector2()
    
    def custom_draw(self,player):
        #GETTING THE OFFSET
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #OFFSET SPRITE POSITIONS
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)