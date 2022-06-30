import pygame as pg
import os

"""
SOUNDS & MUSIC TO BE USED BY THE GAME
SOUND CREDIT: https://marketplace.yoyogames.com/assets/7007/pixel-art-hit-effect
"""

sound_music = pg.mixer.music.load(os.path.join("assets/sounds", 'Temple.wav'))
sound_bonus = pg.mixer.Sound(os.path.join("assets/sounds", 'Bonus.wav'))
sound_coin = pg.mixer.Sound(os.path.join("assets/sounds", 'Coin.wav'))
sound_gold = pg.mixer.Sound(os.path.join("assets/sounds", 'Gold1.wav'))
sound_hit = pg.mixer.Sound(os.path.join("assets/sounds", 'Hit1.wav'))
sound_kill = pg.mixer.Sound(os.path.join("assets/sounds", 'Kill.wav'))
sound_sword = pg.mixer.Sound(os.path.join("assets/sounds", 'Sword.wav'))