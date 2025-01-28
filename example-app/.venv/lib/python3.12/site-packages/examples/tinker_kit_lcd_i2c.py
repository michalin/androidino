"""
 Copyright (c) 2021 Alan Yorinks All rights reserved.

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

"""

"""
This is a port of the HelloWorld.ino from the tinkerkit LCD library.
It is implementing i2c.
"""

import sys
import time

from telemetrix import telemetrix

# TKLCD_Local lcd = TKLCD_Local(); // when programming a TKLCD module itself
# LiquidCrystal::begin(DEFAULT_SIZE_COL, DEFAULT_SIZE_ROWS)

