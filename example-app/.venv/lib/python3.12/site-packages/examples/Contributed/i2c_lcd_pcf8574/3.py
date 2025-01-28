#!/usr/bin/env python3

import sys
import time
from telemetrix import telemetrix
from i2c_lcd_pcf8574 import LcdI2c


"""
This example sets up and control an pcf8574 i2c LCD display.
"""


def pcf8574(my_board):
    lcd = LcdI2c(my_board)
    lcd.begin()
    lcd.clear()
    lcd.backlight()

    lcd.setCursor(5, 1)  # Or setting the cursor in the desired position.
    lcd.print("World!")
    while True:
        time.sleep(1)




board = telemetrix.Telemetrix()
try:
    pcf8574(board)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
