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
    lcd.createChar(0, [0b00000,
    0b10001,
    0b00000,
    0b00000,
    0b10001,
    0b01110,
    0b00000,
    0b00000])
    lcd.createChar(1, [0b01110,
    0b01010,
    0b01110,
    0b00100,
    0b10101,
    0b10101,
    0b01110,
    0b00100])
    lcd.write(1)
    lcd.write(0)
    time.sleep(2)
    # Flashing the backlight
    for i in range(2):
        lcd.noBacklight()
        time.sleep(1)
        lcd.backlight()
        time.sleep(1)
    lcd.cursor()
    lcd.blink()
    lcd.print("     Hello")  # You can make spaces using well... spaces
    time.sleep(2)
    lcd.noBlink()
    lcd.setCursor(5, 1)  # Or setting the cursor in the desired position.
    lcd.print("World!")
    lcd.delayMiliseconds(500)

    # Flashing the backlight
    for i in range(5):
        lcd.backlight()
        lcd.delayMiliseconds(500)
        lcd.noBacklight()
        lcd.delayMiliseconds(500)

    lcd.backlight()
    lcd.clear()
    lcd.delayMiliseconds(500)


board = telemetrix.Telemetrix()
try:
    pcf8574(board)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
