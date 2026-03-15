import game
from controllers.arrow_keys import ArrowKeyController
from controllers.distance_sensor import SensorController
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import config

factory = PiGPIOFactory()
green_led = LED(config.GREEN_LED_PIN, pin_factory=factory)

# controller = ArrowKeyController()
controller = SensorController()
try:
    green_led.off()
    game.run(controller, green_led)

finally:
    green_led.off()
    controller.close()
