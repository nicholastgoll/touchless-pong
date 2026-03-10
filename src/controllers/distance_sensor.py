from gpiozero import DistanceSensor
import config
from collections import deque
from time import sleep

class SensorController():
    def __init__(self):
        self.sensor = DistanceSensor(
            echo=config.ECHO_PIN,
            trigger=config.TRIGGER_PIN,
            max_distance=config.MAX_DISTANCE
        )
        
        readings = deque(maxlen=5)
        
    # returns float 0.0-1 where 1 is MAX_DISTANCE
    def get_paddle_pos(self):
        raw = self.sensor.distance
        meters = raw * config.MAX_DISTANCE
        mapped = (meters - config.SENSOR_MIN) / (config.SENSOR_MAX - config.SENSOR_MIN)
        
        # clamp to 0.0–1.0
        clamped = max(0.0, min(1.0, mapped))

        # smooth over last 5 readings
        self.readings.append(clamped)
        return sum(self.readings) / len(self.readings)


#for testing

# sensor = DistanceSensor(echo=config.ECHO_PIN, trigger=config.TRIGGER_PIN, max_distance=config.MAX_DISTANCE)
# while True:
#     cm = sensor.distance * config.MAX_DISTANCE * 100
#     print(f"Distance(cm): {cm:.2f}")
#     sleep(.5)
