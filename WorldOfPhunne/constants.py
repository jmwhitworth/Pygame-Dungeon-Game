"""
UNCHANGING GAME VARIABLES
"""
import os
import json

with open(os.path.join("WorldOfPhunne/configs", "settings.json"), 'r') as settings_file:
    settings = json.load(settings_file)

TILESIZE =  settings["TILESIZE"]
FPS = settings["FPS"]
SCREENWIDTH = settings["SCREENWIDTH"]
SCREENHEIGHT = settings["SCREENHEIGHT"]

