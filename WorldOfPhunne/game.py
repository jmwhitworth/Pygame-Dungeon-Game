import pygame   as pg
import sys

from .constants  import *
from .level      import Level

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
        
        self.level = Level() #SET UP THE LEVEL CLASS
    
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.level.run() #RUN THE LEVEL EACH LOOP
            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = WorldOfPhunne()
    game.run()