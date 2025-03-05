"""
UNCHANGING GAME VARIABLES
"""

import json
import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


with open(
    resource_path(os.path.join("DungeonGame/configs", "settings.json")), "r"
) as settings_file:
    settings = json.load(settings_file)

TILESIZE = settings["TILESIZE"]
FPS = settings["FPS"]
SCREENWIDTH = settings["SCREENWIDTH"]
SCREENHEIGHT = settings["SCREENHEIGHT"]
