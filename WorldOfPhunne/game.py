import pygame   as pg
import sys

from .constants import *
from .level     import Level
from .debug     import debug

class WorldOfPhunne:
    """
    MAIN WINDOW HANDLER
        - CREATES WINDOW
        - HANDLES MAIN GAME LOOP
    """
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pg.display.set_caption("World of Phunne")
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
            debug(round(self.clock.get_fps(), 2))
            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = WorldOfPhunne()
    game.run()