from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config
from collections import deque
from time import sleep

class SensorController():
    def __init__(self):
        factory = PiGPIOFactory()
        self.sensor = DistanceSensor(
            echo=config.ECHO_PIN,
            trigger=config.TRIGGER_PIN,
            max_distance=config.MAX_DISTANCE,
            pin_factory=factory
        )
        
        self.readings = deque(maxlen=10)
        
    # returns float 0.0-1 where 1 is MAX_DISTANCE
    def get_paddle_pos(self):
        raw = self.sensor.distance
        mapped = (raw - config.SENSOR_MIN) / (config.SENSOR_MAX - config.SENSOR_MIN)
        
        # clamp to 0.0–1.0
        clamped = max(0.0, min(1.0, mapped))

        # smooth over last 5 readings
        self.readings.append(clamped)
        return sum(self.readings) / len(self.readings)
    
    def close(self):
        self.sensor.close()


# for testing
# factory = PiGPIOFactory()
# sensor = DistanceSensor(
#     echo=config.ECHO_PIN, 
#     trigger=config.TRIGGER_PIN, 
#     max_distance=config.MAX_DISTANCE,
#     pin_factory=factory
# )
# while True:
#     cm = sensor.distance * 100
#     print(f"Distance(cm): {cm:.2f}")
#     sleep(.5)
