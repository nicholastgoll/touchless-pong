import pygame
import sys
import random
from gpiozero import DistanceSensor

# --- Game constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

BALL_SIZE = 15
BALL_SPEED_X = 6
BALL_SPEED_Y = 6

SCORE_FONT_SIZE = 40

# AI settings
AI_MAX_SPEED = 6        # max speed per frame for AI paddle
AI_REACTION_MARGIN = 10 # how close ball's center needs to be before AI stops moving

# Distance sensor pins (BCM numbering)
TRIG_PIN = 23
ECHO_PIN = 24

# --- Classes ---


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move(self, dy):
        self.rect.y += dy
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(
            WIDTH // 2 - BALL_SIZE // 2,
            HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE,
        )
        self.speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
        self.speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
        self.speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

    def update(self, player_paddle, ai_paddle):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top / bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

        # Collision with paddles
        if self.rect.colliderect(player_paddle.rect):
            self.rect.right = player_paddle.rect.left
            self.speed_x *= -1

        if self.rect.colliderect(ai_paddle.rect):
            self.rect.left = ai_paddle.rect.right
            self.speed_x *= -1

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)


# --- Helper functions ---


def draw_center_line(surface):
    dash_height = 20
    gap = 10
    x = WIDTH // 2 - 1
    y = 0
    while y < HEIGHT:
        pygame.draw.rect(surface, (200, 200, 200), (x, y, 2, dash_height))
        y += dash_height + gap


def ai_control(ai_paddle, ball):
    # Simple AI: move towards the ball's y position
    if ball.speed_x < 0:  # Only move when ball is coming towards AI
        target_y = ball.rect.centery
        diff = target_y - ai_paddle.rect.centery

        if abs(diff) > AI_REACTION_MARGIN:
            # Clamp movement speed
            move = max(-AI_MAX_SPEED, min(AI_MAX_SPEED, diff))
            ai_paddle.move(move)


def map_distance_to_paddle_y(dist_value):
    """
    dist_value: sensor.distance from gpiozero, in range [0.0, 1.0]
    Returns y position for the top of the paddle in [0, HEIGHT - PADDLE_HEIGHT].
    Close (0.0) = top, far (1.0) = bottom.
    """
    d = max(0.0, min(1.0, dist_value))  # clamp

    y = d * (HEIGHT - PADDLE_HEIGHT)
    return int(y)


def choose_control_mode():
    print("Choose control mode:")
    print("1. Motion Sensor (Raspberry Pi)")
    print("2. Arrow Keys (Keyboard)")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        return "sensor"
    else:
        return "keyboard"


# --- Main game loop ---


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Touchless Pong - Player vs AI")

    mode = choose_control_mode()

    clock = pygame.time.Clock()

    sensor = None
    if mode == "sensor":
        try:
            sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=1.0)
        except Exception as e:
            print("Distance sensor not available on this device, falling back to keyboard controls.")
            print("Reason:", e)
            mode = "keyboard"

    # Create paddles
    player_paddle = Paddle(
        WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2
    )  # Right side (human, sensor-controlled)

    ai_paddle = Paddle(
        40 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2
    )  # Left side (AI)

    # Create ball
    ball = Ball()

    # Scores
    player_score = 0
    ai_score = 0
    font = pygame.font.SysFont("Arial", SCORE_FONT_SIZE)

    running = True
    while running:
        clock.tick(FPS)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Player input ---
        if mode == "sensor" and sensor is not None:
            dist = sensor.distance  # 0.0 (close) to 1.0 (far)
            target_y = map_distance_to_paddle_y(dist)

            # Smooth movement: move paddle toward target_y, capped by paddle speed
            dy = target_y - player_paddle.rect.y
            if abs(dy) > player_paddle.speed:
                dy = player_paddle.speed if dy > 0 else -player_paddle.speed
            player_paddle.move(dy)
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_paddle.move(-player_paddle.speed)
            if keys[pygame.K_DOWN]:
                player_paddle.move(player_paddle.speed)

        # --- AI movement ---
        ai_control(ai_paddle, ball)

        # --- Ball update ---
        ball.update(player_paddle, ai_paddle)

        # --- Scoring ---
        if ball.rect.left <= 0:
            player_score += 1
            ball.reset()
        if ball.rect.right >= WIDTH:
            ai_score += 1
            ball.reset()

        # --- Drawing ---
        screen.fill((0, 0, 0))  # Black background

        draw_center_line(screen)

        player_paddle.draw(screen)
        ai_paddle.draw(screen)
        ball.draw(screen)

        # Draw scores
        player_text = font.render(str(player_score), True, (255, 255, 255))
        ai_text = font.render(str(ai_score), True, (255, 255, 255))
        screen.blit(ai_text, (WIDTH // 4 - ai_text.get_width() // 2, 20))
        screen.blit(
            player_text,
            (3 * WIDTH // 4 - player_text.get_width() // 2, 20),
        )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
