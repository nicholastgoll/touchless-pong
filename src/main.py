import game
from controllers.arrow_keys import ArrowKeyController
from controllers.distance_sensor import DistanceSensor

controller = ArrowKeyController()
#controller = DistanceSensor()

game.run(controller)