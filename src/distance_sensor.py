from gpiozero import DistanceSensor
from time import sleep
import config

sensor = DistanceSensor(echo=config.ECHO_PIN, trigger=config.TRIGGER_PIN, max_distance=config.MAX_DISTANCE)

while True:
    cm = sensor.distance * config.max_distance * 100
    print("Distance(cm): " + cm)
    sleep(.5)
    