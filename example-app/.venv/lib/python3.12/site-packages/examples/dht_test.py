import sys
import time

from telemetrix import telemetrix

"""
Setup a pin for digital output 
and toggle the pin 5 times.
"""

# some globals
DIGITAL_PIN = 14  # the board LED

def the_callback(data):
    print(data)


# Create a Telemetrix instance.
board = telemetrix.Telemetrix()

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_dht(DIGITAL_PIN,  the_callback)

while True:
    time.sleep(5)
    print('exp')
