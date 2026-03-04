'''
The purpose of this file is to provide constants to other files that are easily adjustable instead of hardcoding in those files.
'''

import random

# distance_sensor.py *
ECHO_PIN = 18
TRIGGER_PIN = 17
MAX_DISTANCE = 0.5 # MUST TEST THIS AND ADJUST AS NEEDED

# game.py *
DISPLAY = (600, 800)
FPS = 60
# ball movement
BALL_SPEED_X = 6 * random.choice((1, -1))
BALL_SPEED_Y = 6 * random.choice((1, -1))
# player movement
PLAYER_SPEED = 0
# opponent movement
OPPONENT_SPEED = 7
#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
