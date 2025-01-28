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
    for i in range(3):
        lcd.backlight()
        time.sleep(1)
        lcd.noBacklight()
        time.sleep(1)


board = telemetrix.Telemetrix()
try:
    pcf8574(board)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
    