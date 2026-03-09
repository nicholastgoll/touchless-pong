import pygame as pg
import sys
import random
import config

def ball_movement():
    ball.x += config.BALL_SPEED_X
    ball.y += config.BALL_SPEED_Y
    
    if ball.left <= 0 or ball.right >= WIDTH:
        config.BALL_SPEED_X *= -1
    if ball.top <= 0:
        config.PLAYER_SCORE += 1
        if config.PLAYER_SCORE == 7:
            goodbye()
            pg.quit()
        else: 
            ball_restart()
    if ball.bottom >= HEIGHT:
        config.OPPONENT_SCORE += 1
        if config.OPPONENT_SCORE == 7:
            goodbye()
            pg.quit()
        else: 
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
    
    if opponent.left <= 0:
        opponent.left = 0
    if opponent.right >= WIDTH:
        opponent.right = WIDTH
        
    if opponent.centerx < ball.x - 10:
        opponent.right += config.OPPONENT_SPEED
    if opponent.centerx > ball.x + 10:
        opponent.left -= config.OPPONENT_SPEED 
        
def ball_restart():
    ball.center = (WIDTH/2, HEIGHT/2)
    config.BALL_SPEED_X *= random.choice((1, -1))
    
def goodbye():
    pg.event.pump()
    screen.fill(config.BLACK)
    if config.PLAYER_SCORE == 7:
        text = goodbye_font.render("YOU WIN!!!", True, config.WHITE)
    if config.OPPONENT_SCORE == 7:
        text = goodbye_font.render("YOU LOSE :(", True, config.WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pg.display.flip()
    pg.time.wait(5000)
    

pg.init()

WIDTH, HEIGHT = config.DISPLAY
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Touchless Pong")

clock = pg.time.Clock()

# game rects
ball = pg.Rect(WIDTH/2 - 10, HEIGHT/2 - 10, 20, 20)
player = pg.Rect(WIDTH/2 - 70, HEIGHT - 10, 140, 10)
opponent = pg.Rect(WIDTH/2 - 70, 0, 140, 10)
#original speed needed for opponent movement pauses
old_speed = config.OPPONENT_SPEED

#Font Objects
goodbye_font = pg.font.Font(None, 96)
countdown_text = pg.font.Font(None, 240)
score_player = pg.font.Font(None, 96)
score_opponent = pg.font.Font(None, 96)

# countdown from 5 at start of game
for i in range(5,0,-1):
    pg.event.pump()
    screen.fill(config.BLACK)
    text = countdown_text.render(f"{i}", True, config.WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pg.display.flip()
    pg.time.wait(1000)
    
pg.event.pump()
screen.fill(config.BLACK)
text = countdown_text.render("PONG!", True, config.WHITE)
text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
screen.blit(text, text_rect)
pg.display.flip()
pg.time.wait(1000)

running = True

while running:
    # poll for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                config.PLAYER_SPEED -= config.PLAYER_SPEED_INC
            if event.key == pg.K_RIGHT:
                config.PLAYER_SPEED += config.PLAYER_SPEED_INC
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                config.PLAYER_SPEED += config.PLAYER_SPEED_INC
            if event.key == pg.K_RIGHT:
                config.PLAYER_SPEED -= config.PLAYER_SPEED_INC
    
    ball_movement()
    player_movement()
    if ball.y >= HEIGHT/2:
        config.OPPONENT_SPEED = 0
    else:
        config.OPPONENT_SPEED = old_speed
    opponent_movement()
    
    screen.fill(config.BLACK)
    
    pg.draw.line(screen, config.WHITE, (0,0), (0,HEIGHT), 5)
    pg.draw.line(screen, config.WHITE, (WIDTH - 2, 0), (WIDTH - 2, HEIGHT), 5)
    for i in range(0, WIDTH + 1, 15):
        pg.draw.line(screen, config.WHITE, (i, HEIGHT/2), ((i + 5), HEIGHT/2), 5)
        
    pg.draw.rect(screen, config.WHITE, ball)
    pg.draw.rect(screen, config.WHITE, player)
    pg.draw.rect(screen, config.WHITE, opponent)
    
    score_player_surface = score_player.render(f"{config.PLAYER_SCORE}", True, config.WHITE)
    score_opponent_surface = score_opponent.render(f"{config.OPPONENT_SCORE}", True, config.WHITE)
    
    screen.blit(score_player_surface, (WIDTH-48,(HEIGHT/2)+10))
    screen.blit(score_opponent_surface, (WIDTH-48, (HEIGHT/2)-72))
        
    # takes everything that came before it in loop and draws it
    pg.display.flip()
    
    clock.tick(config.FPS)        

pg.quit()
sys.exit()