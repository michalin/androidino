"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

 DHT support courtesy of Martyn Wheeler
 Based on the DHTNew library - https://github.com/RobTillaart/DHTNew
"""

import sys
import time

from telemetrix import telemetrix

"""
Setup a pin for output and fade its intensity
"""

# some globals
# make sure to select a PWM pin
DIGITAL_PIN = 6
SERVO_PIN = 5

# Create a Telemetrix instance.
board = telemetrix.Telemetrix()

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_analog_output(DIGITAL_PIN)
board.set_pin_mode_analog_output(9)
board.set_pin_mode_analog_output(10)
board.set_pin_mode_analog_output(11)

# board.set_pin_mode_analog_output(DIGITAL_PIN)
board.set_pin_mode_servo(SERVO_PIN, 100, 3000)
time.sleep(.2)
board.servo_write(SERVO_PIN, 90)
time.sleep(1)
board.servo_write(SERVO_PIN, 0)
time.sleep(1)

# When hitting control-c to end the program
# in this loop, we are likely to get a KeyboardInterrupt
# exception. Catch the exception and exit gracefully.

try:

    time.sleep(.2)
    board.servo_write(SERVO_PIN, 90)
    time.sleep(1)
    while True:
        print('Fading up...')
        board.servo_write(SERVO_PIN, 90)

        for i in range(255):
            board.analog_write(DIGITAL_PIN, i)
            board.analog_write(9, i)
            board.analog_write(10, i)
            board.analog_write(11, i)

            time.sleep(.005)
        print('Fading down...')
        board.servo_write(SERVO_PIN, 00)

        for i in range(255, -1, -1):
            board.analog_write(DIGITAL_PIN, i)
            board.analog_write(9, i)
            board.analog_write(10, i)
            board.analog_write(11, i)
            time.sleep(.005)

        time.sleep(3)


except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
