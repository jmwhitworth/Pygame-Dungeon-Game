import pygame   as pg
import sys

from .constants import *
from .level     import Level
from .debug     import debug

class DungeonGame:
    """
    MAIN WINDOW HANDLER
        - CREATES WINDOW
        - HANDLES MAIN GAME LOOP
    """
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pg.display.set_caption("Python Dungeon Game JW")
        programIcon = pg.image.load(resource_path(os.path.join("assets/treasure", "winner_gem.png")))
        pg.display.set_icon(programIcon)
        self.clock = pg.time.Clock()
        
        """
        LEVEL CLASS GENERATES EVERYTHING AND HANDLES SPRITES
        """
        self.level = Level()
    
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            self.screen.fill((126,200,80))
            self.level.run() #UPDATE GAME EACH FRAME
            #debug(round(self.clock.get_fps(), 2)) #DISPLAY FPS IN TOPLEFT CORNER
            pg.display.update()
            self.clock.tick(FPS)
