import pygame   as pg
import os
import random

from .constants import *
from .scenery   import Scenery
from .player    import Player
from .enemy     import Enemy
from .treasure_chest    import Treasure_Chest
from .debug     import debug

class Level():
    """
    - LOADS THE MAP DATA
    - PLACES ALL SPRITES
    - CALLS UPDATE METHOD
    """
    def __init__(self):
        #SET UP SPRITE GROUPS
        self.visible_sprites   = YSortCameraGroup()
        self.obstacle_sprites  = pg.sprite.Group()
        
        self.display_surface = pg.display.get_surface()
        
        self.create_map(1)
    
    def create_map(self, level=1):
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        
        #LOAD THE LEVEL FILE PASSED AS PARAMETER
        with open(os.path.join("WorldOfPhunne/rooms", f"{level}.txt"), 'r') as level_file:
            world_map = level_file.readlines()
        
        #GENERATE TERRAIN AND PLAYER BASED ON MAP FILE
        for row_index, row in enumerate(world_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                
                #BLOCKADES
                if col.lower() == 'x':
                    Scenery(
                        name     = "stump",
                        position = (x, y),
                        sprite_groups = [self.visible_sprites, self.obstacle_sprites]
                    )
                
                #FOLIAGE
                elif col.lower() == 'f':
                    Scenery(
                        name     = f"foliage/{random.randrange(0,7)+1}",
                        position = (x, y),
                        sprite_groups = [self.visible_sprites]
                    )
                
                #TREES
                elif col.lower() == 't':
                    Scenery(
                        name     = f"tree/{random.randrange(0,3)+1}",
                        position = (x, y),
                        sprite_groups = [self.visible_sprites, self.obstacle_sprites],
                        size     = (64,64)
                    )
                
                #TREASURE CHESTS
                elif col.lower() == 'c':
                    Treasure_Chest(
                        name     = "treasure_chest",
                        position = (x, y),
                        sprite_groups = [self.visible_sprites, self.obstacle_sprites]
                    )
                
                #PLAYER
                elif col.lower() == 'p':
                    self.player = Player(
                        name             = "player",
                        position         = (x, y),
                        sprite_groups    = [self.visible_sprites], #MUST PASS 'visible_sprites' FIRST
                        obstacle_sprites = self.obstacle_sprites,
                        target           = "enemy",
                        damage           = 100
                    )
        
        #ENEMIES CREATED ON SECOND PASS SO THAT PLAYER IS AVAILABLE TO PASS TO THEM AS ARG
        for row_index, row in enumerate(world_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col.lower() == 'e':
                    Enemy(
                        name             = "enemy",
                        position         = (x, y),
                        sprite_groups    = [self.visible_sprites], #MUST PASS 'visible_sprites' FIRST
                        obstacle_sprites = self.obstacle_sprites,
                        target           = self.player,
                        damage           = 40
                    )
    
    def run(self):
        #DRAW ALL VISIBLE SPRITES
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        
        #RESET GAME IF PLAYER DIES
        if self.player.health <= 0:
            self.create_map(1)


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