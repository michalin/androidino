import sys
import time

from telemetrix import telemetrix

board = telemetrix.Telemetrix()
# board.shutdown()
board.r4_hard_reset()

time.sleep(2)
board = telemetrix.Telemetrix()

# board.shutdown()
board.r4_hard_reset()
