import game
import config
from controllers.arrow_keys import ArrowKeyController
from controllers.distance_sensor import SensorController

# controller = ArrowKeyController()
controller = SensorController()
try:
    config.GREEN_LED_PIN.on()
    game.run(controller)

finally:
    config.GREEN_LED_PIN.off()
    SensorController.sensor.close()
