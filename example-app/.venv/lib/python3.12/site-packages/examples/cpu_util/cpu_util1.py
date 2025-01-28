import sys
import time
from telemetrix import telemetrix


class Cpu1:
    def __init__(self):
        # instantiate telemetrix
        self.board = telemetrix.Telemetrix()

        # set up pin 6 a digital output pin
        self.board.set_pin_mode_digital_output(6)

        # set up pin 9 for PWM output
        self.board.set_pin_mode_analog_output(9)

        # set up pin A2 for input
        self.board.set_pin_mode_analog_input(2, callback=self.the_callback)

        while True:
            # blink led on pin 6
            # wait for analog input
            try:
                self.board.digital_write(6, 1)
                time.sleep(.5)
                self.board.digital_write(6, 0)
                time.sleep(.5)
            except KeyboardInterrupt:
                self.board.shutdown()
                sys.exit(0)

    def the_callback(self, data):
        # data[2] contains the analog value
        # calculate a value within the range of 0 - 255
        # set pin 9 to this value
        self.board.analog_write(9, data[2] // 4)


Cpu1()
