"""
 Copyright (c) 2023 Alan Yorinks All rights reserved.

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
Simulate a rotary encoder
"""

"""
Setup pins for digital inputs and monitor their changes changes
"""

# Set up a pin for analog input and monitor its changes
CLOCK_WISE_PIN = 12  # arduino pin number
ANIT_CLOCK_WISE_PIN = 13

# some globals
astate = None
last_state = None
update = False
counter = 0


def the_callback(data):
    """
    A callback function to report data changes

    :param data: [report type, pin, current reported value, pin_mode, timestamp]
    """
    global astate, last_state, update, counter
    the_pin = data[1]
    the_pin_state = data[2]

    if the_pin == CLOCK_WISE_PIN:
        astate = the_pin_state
        if astate != last_state:
            last_state = astate
            update = True
    else:
        if update:
            if the_pin_state != astate:
                counter = counter + 1
            else:
                counter = counter - 1
            update = False
    print(f'astate: {astate}   last_state: {last_state}   update: {update}    counter: '
          f'{counter}')


def rotary_simulator(my_board, clockwise_pin, anti_clockwise_pin):
    """
     This function establishes the pins as
     digital inputs. Any changes on the pins will
     be reported through the call back function.

     :param my_board: a telemetrix instance
     :param clockwise_pin: Arduino pin number
     :param anti_clockwise_pin : Arduino pin number
     """

    # set the pin mode
    my_board.set_pin_mode_digital_input(clockwise_pin, the_callback)
    my_board.set_pin_mode_digital_input(anti_clockwise_pin, the_callback)

    try:
        while True:
            time.sleep(.0001)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)


board = telemetrix.Telemetrix(arduino_wait=4)

try:
    rotary_simulator(board, CLOCK_WISE_PIN, ANIT_CLOCK_WISE_PIN)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
