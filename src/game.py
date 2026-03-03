import pygame as pg
import config

pg.init()
screen = pg.display.set_mode(config.DISPLAY)
clock = pg.time.Clock()

running = True

while running:
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill("black")
    
    pg.display.flip()
    clock.tick(config.FPS)        
pg.quit()
