import signal
import sys
import game
from controllers.arrow_keys import ArrowKeyController
from controllers.distance_sensor import SensorController
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import config

factory = PiGPIOFactory()
green_led = LED(config.GREEN_LED_PIN, pin_factory=factory)
controller = SensorController(factory)

def cleanup():
    green_led.off()
    controller.close()

signal.signal(signal.SIGTERM, lambda _s, _f: (cleanup(), sys.exit(0)))
signal.signal(signal.SIGINT, lambda _s, _f: (cleanup(), sys.exit(0)))

# controller = ArrowKeyController()
try:
    green_led.off()
    game.run(controller, green_led)
finally:
    cleanup()
