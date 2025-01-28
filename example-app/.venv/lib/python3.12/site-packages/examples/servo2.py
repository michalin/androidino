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
Attach a pin to a servo and move it about.
"""

# some globals
SERVO_PIN = 5

# Create a Telemetrix instance.
board = telemetrix.Telemetrix()
board.set_pin_mode_servo(2, 100, 3000)
time.sleep(.2)
board.set_pin_mode_servo(3, 100, 3000)
time.sleep(.2)
board.set_pin_mode_servo(4, 100, 3000)
time.sleep(.2)
board.set_pin_mode_servo(5, 100, 3000)
time.sleep(.2)
board.set_pin_mode_servo(6, 100, 3000)
time.sleep(.2)
board.set_pin_mode_servo(7, 100, 3000)
for x in range(2, 8):
    board.servo_write(x, 33)
    time.sleep(.3)
time.sleep(3)


board.shutdown()
