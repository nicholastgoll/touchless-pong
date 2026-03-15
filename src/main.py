import game
from controllers.arrow_keys import ArrowKeyController
from controllers.distance_sensor import SensorController
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import config

factory = PiGPIOFactory()
red_led = LED(config.RED_LED_PIN, pin_factory=factory)
green_led = LED(config.GREEN_LED_PIN, pin_factory=factory)

# controller = ArrowKeyController()
controller = SensorController()
try:
    red_led.on()
    green_led.off()
    game.run(controller, red_led, green_led)

finally:
    green_led.off()
    red_led.on()
    controller.close()
