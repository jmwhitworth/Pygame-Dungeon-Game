import pygame       as pg
import os

from .constants     import *
from .debug         import debug

class Attack(pg.sprite.Sprite):
    """
    ATTACK SPRITE WHICH IS SPAWNED WHEN A CHARACTER ATTACKS
    IF IT HAS COLLISION WITH A SPECIFIED SPRITE IT'LL DAMAGE THAT SPRITE
    """
    def __init__(self, sprite_groups, position, duration, visible_sprites, target_names, damage):
        super().__init__(sprite_groups)
        
        self.duration = duration/2 #TIME IN MS OF HOW LONG ATTACK LASTS
        self.spawn_time = pg.time.get_ticks()
        self.visible_sprites = visible_sprites
        self.target_names = target_names
        self.damage = damage
        
        self.image = pg.image.load(resource_path(os.path.join("assets", "blank.png"))).convert_alpha()
        self.image = pg.transform.scale(self.image, (30,32)) #SCALE THE 16X16 IMAGE TO GIVEN SIZE
        self.rect = self.image.get_rect(topleft = position)
    
    def update(self):
        self.hit_detection()
        current_tick = pg.time.get_ticks()
        if current_tick - self.spawn_time >= self.duration:
            self.kill()
    
    def hit_detection(self):
        """
        GO THROUGH ALL OBSTACLES AND IF ATTACK COLLIDES,
        APPLY DAMAGE TO SPRITE HIT
        """
        for sprite in self.visible_sprites:
            try:
                for target in self.target_names:
                    if sprite.hitbox.colliderect(self.rect):
                        if sprite.name == target:
                            sprite.hit(self.damage)
                            self.kill()
            except AttributeError:
                pass