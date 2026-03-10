import pygame as pg
import config

class ArrowKeyController():
    def __init__(self):
        self.position = 0.5
        
    def get_paddle_pos(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.position -= config.ARROW_SPEED
        elif keys[pg.K_RIGHT]:
            self.position += config.ARROW_SPEED
            
        self.position = max(0.0, min(1.0, self.position))
        return self.position
        
        