import pygame as pg

pg.init()
screen = pg.display.set_mode((600,800))
clock = pg.time.Clock()

while running:
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill("black")
    
    pg.display.flip()
    clock.tick(60)        
pg.quit()
