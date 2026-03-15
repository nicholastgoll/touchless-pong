'''
The purpose of this file is to provide constants to other files that are easily adjustable instead of hardcoding in those files.
'''

import random

# ----- distance_sensor.py -----
ECHO_PIN = 18
TRIGGER_PIN = 17
MAX_DISTANCE = 0.5

SENSOR_MAX = 0.35 # 20 cm
SENSOR_MIN = 0.05 # 5 cm

# ----- game.py -----
DISPLAY = (500,600)
FPS = 60
# ball movement
SPEED_MULTIPLIER = 0.4
BALL_SPEED_X = 6 * random.choice((1, -1))
BALL_SPEED_Y = 6 * random.choice((1, -1))
# player movement w arrow keys
ARROW_SPEED = 0.01
# opponent movement
OPPONENT_SPEED = 3
#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Score
PLAYER_SCORE = 0
OPPONENT_SCORE = 0
