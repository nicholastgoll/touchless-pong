'''
The purpose of this file is to provide constants to other files that are easily adjustable instead of hardcoding in those files.
'''

import random

# ----- distance_sensor.py -----
ECHO_PIN = 18
TRIGGER_PIN = 17
MAX_DISTANCE = 0.5

SENSOR_MAX = 0.2
SENSOR_MIN = 0.02

# ----- game.py -----
DISPLAY = (500,600)
FPS = 60
# ball movement
BALL_SPEED_X = 9 * random.choice((1, -1))
BALL_SPEED_Y = 9 * random.choice((1, -1))
# player movement w arrow keys
ARROW_SPEED = 0.01
# opponent movement
OPPONENT_SPEED = 6
#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Score
PLAYER_SCORE = 0
OPPONENT_SCORE = 0
