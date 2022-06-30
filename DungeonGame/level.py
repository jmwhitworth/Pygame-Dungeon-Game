import pygame   as pg
import os
import random
import json
import time

from .constants import *
from .scenery   import Scenery
from .player    import Player
from .enemy     import Enemy
from .treasure_chest    import Treasure_Chest
from .move_room import Move_Room
from .going_tile import Going_Tile
from .sounds    import *
from .debug     import debug
from .prompt    import Prompt
from .treasure_winner   import Treasure_Winner

class Level():
    """
    - LOADS THE MAP DATA
    - PLACES ALL SPRITES
    - CALLS UPDATE METHOD
    """
    def __init__(self):
        #SET UP SPRITE GROUPS
        self.visible_sprites  = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()
        self.prompts          = pg.sprite.Group()
        
        self.display_surface = pg.display.get_surface()
        
        self.data_files = ["player.json"]
        self.room_list = ['1', '2', '3', '4', '5', '6', '7']
        [self.data_files.append(f"rooms/{room}/status.json") for room in self.room_list]
        [self.data_files.append(f"rooms/{room}/layout.txt") for room in self.room_list]
        
        self.going_dict = {"n":"North","e":"East","s":"South","w":"West"}
        self.direction_list = ['n', 'e', 's', 'w']
        
        self.current_room = self.room_list[0]
        
        pg.mixer.music.play(-1)
        
        self.complete = False
        self.reset_game()
        self.create_map(self.current_room)
    
    def create_map(self, level='1'):
        self.current_room = level
        
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        
        #LOAD THE LEVEL FILE PASSED AS PARAMETER
        with open(resource_path(os.path.join(f"DungeonGame/data/live/rooms/{level}", "layout.txt")), 'r') as level_file:
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
                
                #ROOM MOVING TILES
                elif col.lower() in self.room_list:
                    Move_Room(
                        name     = col.lower(),
                        position = (x, y),
                        sprite_groups = [self.visible_sprites],
                        level = self
                    )
                
                #WINNER TREASURE
                elif col.lower() == "m":
                    Treasure_Winner(
                        name     = col.lower(),
                        position = (x, y),
                        sprite_groups = [self.visible_sprites],
                        level = self
                    )
                
                #GOING TILES
                elif col.lower() in self.direction_list:
                    Going_Tile(
                        name     = self.going_dict[col.lower()],
                        position = (x, y),
                        sprite_groups = [self.visible_sprites]
                    )
                
        player_data = self.load_json_data("player.json")
        room_sprite_data = self.load_json_data(f"rooms/{level}/status.json")
        
        self.player = Player(
            name             = "player",
            position         = (room_sprite_data["entries"][player_data["Going"]]["X"], room_sprite_data["entries"][player_data["Going"]]["Y"]),
            sprite_groups    = [self.visible_sprites], #MUST PASS 'visible_sprites' FIRST
            obstacle_sprites = self.obstacle_sprites,
            target           = "enemy",
            damage           = 100,
            health           = player_data["Health"],
            gold             = player_data["Gold"]
        )
        
        try:
            for chest in room_sprite_data["chests"]:
                Treasure_Chest(
                    name     = "treasure_chest",
                    position = (room_sprite_data["chests"][chest]["Position X"], room_sprite_data["chests"][chest]["Position Y"]),
                    sprite_groups = [self.visible_sprites, self.obstacle_sprites],
                    health   = room_sprite_data["chests"][chest]["Health"]
                )
        except KeyError:
            print("No chests data provided this room.")
        
        try:
            for enemy in room_sprite_data["enemies"]:
                if room_sprite_data["enemies"][enemy]["Health"] > 0:
                    Enemy(
                        name             = "enemy",
                        position         = (room_sprite_data["enemies"][enemy]["Position X"], room_sprite_data["enemies"][enemy]["Position Y"]),
                        sprite_groups    = [self.visible_sprites], #MUST PASS 'visible_sprites' FIRST
                        obstacle_sprites = self.obstacle_sprites,
                        target           = self.player,
                        damage           = 40,
                        health   = room_sprite_data["enemies"][enemy]["Health"]
                    )
        except KeyError:
            print("No enemy data provided this room.")
    
    def reset_game(self):
        """
        LOADS ALL STANDARD DATA FROM CORE DATA DIRECTORIES
        PASSES THEM TO THE LIVE VERSIONS TO BE RESET
        """
        self.complete = False
        for path in self.data_files:
            if path.endswith('.json'):
                data = self.load_json_data(path, "core")
                self.write_json_data(path, data)
            elif path.endswith('.txt'):
                data = self.load_text_data(path, "core")
                self.write_text_data(path, data)
            print(f"Reset: {path}")
    
    def write_json_data(self, path, data):
        """
        WRITES GIVEN DATA TO THE LIVE VERSIONS OF THE PATH PROVIDED
        """
        path = resource_path(os.path.join("DungeonGame/data/live/", path))
        
        with open(path, 'w+', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    def load_json_data(self, path, data_type="live"):
        """
        LOADS EITHER CORE OR LIVE DATA OF THE PATH GIVEN AS JSON
        """
        path = resource_path(os.path.join(f"DungeonGame/data/{data_type}/", path))
        print(f"Loading data from: {path}")
        with open(path, 'r') as status_file:
            status = json.load(status_file)
        return status
    
    def write_text_data(self, path, data):
        """
        WRITES GIVEN DATA TO THE LIVE VERSIONS OF THE PATH PROVIDED
        """
        path = resource_path(os.path.join("DungeonGame/data/live/", path))
        with open(path, 'w+') as file:
            file.writelines(data)
    
    def load_text_data(self, path, data_type="live"):
        """
        LOADS EITHER CORE OR LIVE DATA OF THE PATH GIVEN AS JSON
        """
        path = resource_path(os.path.join(f"DungeonGame/data/{data_type}/", path))
        print(f"Loading data from: {path}")
        with open(path, 'r') as layout_file:
            content = layout_file.read()
        return content
    
    def save_room_state(self, room):
        data = self.load_json_data(f"rooms/{room}/status.json")
        data["chests"] = {}
        data["enemies"] = {}
        count = 0
        for sprite in self.visible_sprites:
            if sprite.name == "treasure_chest":
                data["chests"][count] = {"Health": sprite.health, "Position X": sprite.rect.x, "Position Y": sprite.rect.y}
                count += 1
        count = 0
        for sprite in self.visible_sprites:
            if sprite.name == "enemy":
                data["enemies"][count] = {"Health": sprite.health, "Position X": sprite.rect.x, "Position Y": sprite.rect.y}
                count += 1
        self.write_json_data(f"rooms/{room}/status.json", data)
    
    def save_player_state(self):
        data = self.player.get_info()
        self.write_json_data("player.json", data)
    
    def run(self):
        #DRAW ALL VISIBLE SPRITES
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.prompts.update()
        
        if self.player.health <= 0:
            Prompt([self.visible_sprites, self.prompts], f"You died! Score: {self.player.gold}", "red")
            self.reset_game()
            self.create_map(1)
        
        if self.complete:
            Prompt([self.visible_sprites, self.prompts], f"You Won! Score: {self.player.gold}", "Blue")
            self.reset_game()
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
