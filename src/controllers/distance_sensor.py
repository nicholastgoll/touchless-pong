#pigpio library works as a client-server setup. The PiGPIOFactory() doesn't talk to the GPIO pins directly — 
# it connects to a background daemon process (pigpiod) that does the actual hardware-timed GPIO work. 
# That daemon listens on localhost:8888 by default.
# must run sudo pigpiod in terminal first on pi!!
# sudo systemctl enable pigpiod then sudo systemctl start pigpiod to keep it running even after reboot
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config
from collections import deque
from time import sleep

class SensorController():
    def __init__(self):
        self.sensor = DistanceSensor(
            echo=config.ECHO_PIN,
            trigger=config.TRIGGER_PIN,
            max_distance=config.MAX_DISTANCE,
            pin_factory=config.FACTORY
        )
        
        self.smoothed = 0.5
        self.alpha = 0.3
        
    def get_paddle_pos(self):
        raw = self.sensor.distance
        mapped = (raw - config.SENSOR_MIN) / (config.SENSOR_MAX - config.SENSOR_MIN)
        
        # clamp to 0.0–1.0
        clamped = max(0.0, min(1.0, mapped))

        # smooth over last 5 readings and reject spikes
        if abs(clamped - self.smoothed) > 0.3:
            return self.smoothed
        self.smoothed += self.alpha * (clamped - self.smoothed)
        return self.smoothed
    
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
