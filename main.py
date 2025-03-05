import asyncio
import sys

import pygame as pg

from DungeonGame.constants import *
from DungeonGame.debug import debug
from DungeonGame.level import Level

screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pg.display.set_caption("Python Dungeon Game by Jack Whitworth")
programIcon = pg.image.load(
    resource_path(os.path.join("assets/treasure", "winner_gem.png"))
)
pg.display.set_icon(programIcon)
clock = pg.time.Clock()


async def run():
    level = Level()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill((126, 200, 80))
        level.run()
        debug(f"FPS: {int(clock.get_fps())}")
        pg.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(run())
