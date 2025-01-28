import sys
import time

from telemetrix import telemetrix

# LEDs
DIGITAL_PIN1 = 6
DIGITAL_PIN2 = 9
DIGITAL_PIN3 = 10
DIGITAL_PIN4 = 11


# Create a Telemetrix instance.
board = telemetrix.Telemetrix()

# Set the DIGITAL_PINs as output pins
board.set_pin_mode_analog_output(DIGITAL_PIN1)
board.set_pin_mode_analog_output(DIGITAL_PIN2)
board.set_pin_mode_analog_output(DIGITAL_PIN3)
board.set_pin_mode_analog_output(DIGITAL_PIN4)

fade_values =[0, 65, 125, 255]
led_pins = [6, 9, 10, 11]

while True:
    try:
        for i in fade_values:
            for pin in led_pins:
                board.analog_write(pin, i)
            time.sleep(200)
    except KeyboardInterrupt:
        board.shutdown()