#!/usr/bin/env python3
"""
 Copyright (c) 2020 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import sys
import time
from telemetrix import telemetrix
from i2c_lcd_pcf8574 import LCD_I2C


"""
This example sets up and control an pcf8574 i2c LCD display.
"""
def pcf8574(board):
    lcd = LCD_I2C(board)
    lcd.begin()
    lcd.clear()
    lcd.backlight()

    # Flashing the backlight
    for i in range(5):
        lcd.noBacklight()
        time.sleep(1)
        lcd.backlight()
        time.sleep(1)


    lcd.print("     Hello") # You can make spaces using well... spaces
    lcd.setCursor(5, 1) # Or setting the cursor in the desired position.
    lcd.print("World!")
    lcd.delayMiliseconds(500)
#
#    # Flashing the backlight
#    for i in range(5):
#        lcd.backlight()
#        lcd.delayMiliseconds(500)
#        lcd.noBacklight()
#        lcd.delayMiliseconds(500)
#
#    lcd.backlight()
#    lcd.clear()
#    lcd.delayMiliseconds(500)


board = telemetrix.Telemetrix()
try:
    pcf8574(board)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
