import game
from controllers.arrow_keys import ArrowKeyController
from controllers.distance_sensor import SensorController
from gpiozero import LED
import config

green_led = LED(config.GREEN_LED_PIN)

# controller = ArrowKeyController()
controller = SensorController()
try:
    green_led.off()
    game.run(controller, green_led)

finally:
    green_led.off()
    controller.close()
