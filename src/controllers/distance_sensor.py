from gpiozero import DistanceSensor
import config
from time import sleep

class SensorController():
    def __init__(self):
        self.sensor = DistanceSensor(
            echo=config.ECHO_PIN,
            trigger=config.TRIGGER_PIN,
            max_distance=config.MAX_DISTANCE
        )
        
    # returns float 0.0-1 where 1 is MAX_DISTANCE
    def get_paddle_pos(self):
        return self.sensor.distance



#for testing

# sensor = DistanceSensor(echo=config.ECHO_PIN, trigger=config.TRIGGER_PIN, max_distance=config.MAX_DISTANCE)
# while True:
#     cm = sensor.distance * config.MAX_DISTANCE * 100
#     print(f"Distance(cm): {cm:.2f}")
#     sleep(.5)
