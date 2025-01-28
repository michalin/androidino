import sys
import time
from telemetrix import telemetrix

mcu = None
try:
    mcu = telemetrix.Telemetrix(sleep_tune=0.1)
    # mcu = telemetrix.Telemetrix(sleep_tune=0.000001)
    while True:
        try:
            time.sleep(.5)
        except KeyboardInterrupt:
            mcu.shutdown()
            sys.exit(0)
except KeyboardInterrupt:
    mcu.shutdown()
    sys.exit(0)
