import pygame as pg
import random
import config
import time

def ball_movement(ball, player, opponent, WIDTH, HEIGHT, screen, goodbye_font):
    ball.x += config.BALL_SPEED_X * config.SPEED_MULTIPLIER
    ball.y += config.BALL_SPEED_Y * config.SPEED_MULTIPLIER
    
    if ball.left <= 0 or ball.right >= WIDTH:
        config.BALL_SPEED_X *= -1
    if ball.top <= 0:
        config.PLAYER_SCORE += 1
        config.SCORE_SOUND.play()
        if config.PLAYER_SCORE == 7:
            goodbye(ball, player, opponent, WIDTH, HEIGHT, screen, goodbye_font)
            return False
        else: 
            ball_restart(ball, WIDTH, HEIGHT)
    if ball.bottom >= HEIGHT:
        config.OPPONENT_SCORE += 1
        config.LOST_POINT_SOUND.play()
        if config.OPPONENT_SCORE == 7:
            goodbye(ball, player, opponent, WIDTH, HEIGHT, screen, goodbye_font)
            return False
        else: 
            ball_restart(ball, WIDTH, HEIGHT)
    
    if ball.colliderect(player) or ball.colliderect(opponent):
        config.BALL_SPEED_Y *= -1
        config.SPEED_MULTIPLIER = 1.0

    return True
    
def player_movement(player, controller, WIDTH):
    player.centerx = int(controller.get_paddle_pos() * WIDTH)
    if player.left <= 0:
        player.left = 0
    if player.right >= WIDTH:
        player.right = WIDTH
        
def opponent_movement(opponent, ball, WIDTH):
    
    if opponent.left <= 0:
        opponent.left = 0
    if opponent.right >= WIDTH:
        opponent.right = WIDTH
        
    if opponent.centerx < ball.x - 10:
        opponent.right += config.OPPONENT_SPEED
    if opponent.centerx > ball.x + 10:
        opponent.left -= config.OPPONENT_SPEED 
        
def ball_restart(ball, WIDTH, HEIGHT):
    ball.center = (WIDTH//2, HEIGHT//2)
    config.BALL_SPEED_X *= random.choice((1, -1))
    config.SPEED_MULTIPLIER = 0.4
    
def goodbye(ball, player, opponent, WIDTH, HEIGHT, screen, goodbye_font):
    pg.event.pump()
    screen.fill(config.BLACK)
    if config.PLAYER_SCORE == 7:
        config.WIN_SOUND.play()
        text = goodbye_font.render("YOU WIN!!!", True, config.WHITE)
    if config.OPPONENT_SCORE == 7:
        config.LOSE_SOUND.play()
        text = goodbye_font.render("YOU LOSE :(", True, config.WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pg.display.flip()
    pg.time.wait(5000)
    
def run(controller):
    pg.init()

    WIDTH, HEIGHT = config.DISPLAY
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Touchless Pong")
    
    clock = pg.time.Clock()
    
    # game rects
    ball = pg.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)
    player = pg.Rect(WIDTH//2 - 60, HEIGHT - 10, 120, 10)
    opponent = pg.Rect(WIDTH//2 - 60, 0, 120, 10)
    #original speed needed for opponent movement pauses
    old_speed = config.OPPONENT_SPEED

    #Font Objects
    goodbye_font = pg.font.Font(None, 96)
    countdown_text = pg.font.Font(None, 240)
    score_player = pg.font.Font(None, 96)
    score_opponent = pg.font.Font(None, 96)

    def check_quit():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True
        return False


    start_time = time.time()
    # countdown from 5 at start of game
    for i in range(5,0,-1):
        if check_quit():
            return
        config.COUNTDOWN_SOUND.play()
        screen.fill(config.BLACK)
        text = countdown_text.render(f"{i}", True, config.WHITE)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
        pg.display.flip()
        pg.time.wait(1000)

    if check_quit():
            return
    config.GAME_START_SOUND.play()
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
        
        if not running:
            break
                
        running = ball_movement(ball, player, opponent, WIDTH, HEIGHT, screen, goodbye_font)
        if not running:
            break
        
        player_movement(player, controller, WIDTH)
        
        if ball.y >= HEIGHT//2:
            config.OPPONENT_SPEED = 0
        else:
            config.OPPONENT_SPEED = old_speed
        opponent_movement(opponent, ball, WIDTH)
        
        screen.fill(config.BLACK)
        
        pg.draw.line(screen, config.WHITE, (0,0), (0,HEIGHT), 5)
        pg.draw.line(screen, config.WHITE, (WIDTH - 2, 0), (WIDTH - 2, HEIGHT), 5)
        for i in range(0, WIDTH + 1, 15):
            pg.draw.line(screen, config.WHITE, (i, HEIGHT//2), ((i + 5), HEIGHT//2), 5)
            
        pg.draw.rect(screen, config.WHITE, ball)
        pg.draw.rect(screen, config.WHITE, player)
        pg.draw.rect(screen, config.WHITE, opponent)
        
        score_player_surface = score_player.render(f"{config.PLAYER_SCORE}", True, config.WHITE)
        score_opponent_surface = score_opponent.render(f"{config.OPPONENT_SCORE}", True, config.WHITE)
        
        screen.blit(score_player_surface, (WIDTH-48,(HEIGHT//2)+10))
        screen.blit(score_opponent_surface, (WIDTH-48, (HEIGHT//2)-72))
            
        # takes everything that came before it in loop and draws it
        pg.display.flip()
        
        clock.tick(config.FPS)
    
    duration = round(time.time() - start_time)
    
    stats = {
        "player_score": config.PLAYER_SCORE,
        "opponent_score": config.OPPONENT_SCORE,
        "winner": "player" if config.PLAYER_SCORE > config.OPPONENT_SCORE else "opponent",
        "duration_seconds": duration,
    }
    
    # reset for replay
    config.PLAYER_SCORE = 0
    config.OPPONENT_SCORE = 0
    config.SPEED_MULTIPLIER = 0.4
    config.OPPONENT_SPEED = 3
    
    return stats
