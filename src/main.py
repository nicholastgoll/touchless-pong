import game
import config
from controllers.arrow_keys import ArrowKeyController

controller = ArrowKeyController()
try:
    stats = game.run(controller)
    print(stats)

finally:
    game.pg.quit()

    