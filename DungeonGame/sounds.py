import os

import pygame as pg

from .constants import *

"""
SOUNDS & MUSIC TO BE USED BY THE GAME
SOUND CREDIT: https://marketplace.yoyogames.com/assets/7007/pixel-art-hit-effect
"""
sound_music = pg.mixer.music.load(
    resource_path(os.path.join("assets/sounds", "Temple.wav"))
)
pg.mixer.music.set_volume(0.1)
sound_bonus = pg.mixer.Sound(resource_path(os.path.join("assets/sounds", "Bonus.wav")))
sound_bonus.set_volume(0.1)
sound_coin = pg.mixer.Sound(resource_path(os.path.join("assets/sounds", "Coin.wav")))
sound_coin.set_volume(0.1)
sound_gold = pg.mixer.Sound(resource_path(os.path.join("assets/sounds", "Gold1.wav")))
sound_gold.set_volume(0.1)
sound_hit = pg.mixer.Sound(resource_path(os.path.join("assets/sounds", "Hit1.wav")))
sound_hit.set_volume(0.1)
sound_kill = pg.mixer.Sound(resource_path(os.path.join("assets/sounds", "Kill.wav")))
sound_kill.set_volume(0.1)
sound_sword = pg.mixer.Sound(resource_path(os.path.join("assets/sounds", "Sword.wav")))
sound_sword.set_volume(0.1)
