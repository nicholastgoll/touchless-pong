import game
from controllers.arrow_keys import ArrowKeyController
from controllers.distance_sensor import SensorController

# controller = ArrowKeyController()
try:
    controller = SensorController()

    game.run(controller)
    
finally:
    SensorController.sensor.close()
