import pygame as pg
import sys
import random
import config

def ball_movement():
    ball.x += config.BALL_SPEED_X
    ball.y += config.BALL_SPEED_Y
    
    if ball.left <= 0 or ball.right >= WIDTH:
        config.BALL_SPEED_X *= -1
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_restart()
    
    if ball.colliderect(player) or ball.colliderect(opponent):
        config.BALL_SPEED_Y *= -1

def player_movement():
    player.x += config.PLAYER_SPEED
    if player.left <= 0:
        player.left = 0
    if player.right >= WIDTH:
        player.right = WIDTH
        
def opponent_movement():
    if opponent.right < ball.x:
        opponent.right += config.OPPONENT_SPEED
    if opponent.left > ball.x:
        opponent.left -= config.OPPONENT_SPEED 
    if opponent.left <= 0:
        opponent.left = 0
    if opponent.right >= WIDTH:
        opponent.right = WIDTH
        
def ball_restart():
    ball.center = (WIDTH/2, HEIGHT/2)
    config.BALL_SPEED_X *= random.choice((1, -1))

pg.init()
WIDTH, HEIGHT = config.DISPLAY
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Touchless Pong")

clock = pg.time.Clock()

# game rects
ball = pg.Rect(WIDTH/2 - 10, HEIGHT/2 - 10, 20, 20)
player = pg.Rect(WIDTH/2 - 70, HEIGHT - 10, 140, 10)
opponent = pg.Rect(WIDTH/2 - 70, 0, 140, 10)

running = True

while running:
    # poll for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                config.PLAYER_SPEED -= 7
            if event.key == pg.K_RIGHT:
                config.PLAYER_SPEED += 7
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                config.PLAYER_SPEED += 7
            if event.key == pg.K_RIGHT:
                config.PLAYER_SPEED -= 7
    
    ball_movement()
    player_movement()
    opponent_movement()
    
    screen.fill(config.BLACK)
    
    pg.draw.line(screen, config.WHITE, (0,0), (0,HEIGHT), 5)
    pg.draw.line(screen, config.WHITE, (WIDTH - 2, 0), (WIDTH - 2, HEIGHT), 5)
    for i in range(0, WIDTH + 1, 15):
        pg.draw.line(screen, config.WHITE, (i, HEIGHT/2), ((i + 5), HEIGHT/2), 5)
        
    pg.draw.rect(screen, config.WHITE, ball)
    pg.draw.rect(screen, config.WHITE, player)
    pg.draw.rect(screen, config.WHITE, opponent)
    

        
    # takes everything that came before it in loop and draws it
    pg.display.flip()
    
    clock.tick(config.FPS)        

pg.quit()
sys.exit()