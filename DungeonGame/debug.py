import pygame as pg

pg.init()
font = pg.font.Font(None, 24)

"""
DISPLAYS INFORMATION PASSED TO IT ON THE GIVEN X & Y COORDINATES
"""


def debug(info, y=10, x=10):
    display_surface = pg.display.get_surface()
    debug_surf = font.render(str(info), True, "white")
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pg.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)
