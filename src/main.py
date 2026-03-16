import game
import config
from controllers.arrow_keys import ArrowKeyController
from controllers.distance_sensor import SensorController

#controller = ArrowKeyController()
controller = SensorController()
try:
    config.GREEN_LED_PIN.on()
    stats = game.run(controller)
    print(stats)

finally:
    controller.sensor.close()
    game.pg.quit()
    config.GREEN_LED_PIN.off()
    