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

 LCD_I2C - Arduino library to control a 16x2 LCD via an I2C adapter based on PCF8574
 * 2021-11-18 Brewmanz: make changes to also work for 20x4 LCD2004

 Copyright(C) 2020 Blackhack <davidaristi.0504@gmail.com>

 This program is free software : you can redistribute it and /or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.If not, see < https://www.gnu.org/licenses/>.
"""

import sys
import time
from telemetrix import telemetrix

"""
/* This struct helps us constructing the I2C output based on data and control outputs.
   Because the LCD is set to 4-bit mode, 4 bits of the I2C output are for the control outputs
   while the other 4 bits are for the 8 bits of data which are send in parts using the enable output.*/
"""


class OutputState(object):
    def __init__(self):
        self.rs = 0
        self.rw = 0
        self.E = 0
        self.Led = 0
        self.data = 0

    def GetLowData(self):
        buffer = self.rs
        buffer |= self.rw << 1
        buffer |= self.E << 2
        buffer |= self.Led << 3
        buffer |= (self.data & 0x0F) << 4

        return buffer

    def GetHighData(self):
        buffer = self.rs
        buffer |= self.rw << 1
        buffer |= self.E << 2
        buffer |= self.Led << 3
        buffer |= (self.data & 0xF0)
        return buffer


class LCD_I2C(object):
    def __init__(self, board, address=0x27, columns=16, rows=2):
        self.board = board
        self._address = address
        self._columnMax = columns - 1
        self._rowMax = rows - 1
        self._displayState = 0x00
        self._entryState = 0x00
        self._output = OutputState()

        board.set_pin_mode_i2c()
        # board.i2c_write(self._address, [0])

    def begin(self):
        #        if (beginWire):
        #            Wire.begin()

        self.I2C_Write(0b00000000)  # Clear i2c adapter
        self.delayMiliseconds(50)  # Wait more than 40ms after powerOn.

        self.InitializeLCD()
        # time.sleep(1)

    def backlight(self):
        self._output.Led = 1
        self.I2C_Write(
            0b00000000 | self._output.Led << 3)  # Led pin is independent from LCD data and control lines.

    def noBacklight(self):
        self._output.Led = 0
        self.I2C_Write(
            0b00000000 | self._output.Led << 3)  # Led pin is independent from LCD data and control lines.

    def clear(self):
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00000001)
        # self.delayMicroseconds(1600)
        self.delayMiliseconds(50)
        # time.sleep(.5)

    def home(self):
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00000010)
        self.delayMicroseconds(1600)

    # Part of Entry mode set
    def leftToRight(self):
        self._output.rs = 0
        self._output.rw = 0

        self._entryState |= 1 << 1

        self.LCD_Write(0b00000100 | self._entryState)
        self.delayMicroseconds(37)

    # Part of Entry mode set
    def rightToLeft(self):
        self._output.rs = 0
        self._output.rw = 0

        self._entryState &= ~(1 << 1)

        self.LCD_Write(0b00000100 | self._entryState)
        self.delayMicroseconds(37)

    # Part of Entry mode set
    def autoscroll(self):
        self._output.rs = 0
        self._output.rw = 0

        self._entryState |= 1

        self.LCD_Write(0b00000100 | self._entryState)
        self.delayMicroseconds(37)

    # Part of Entry mode set
    def noAutoscroll(self):
        self._output.rs = 0
        self._output.rw = 0

        self._entryState &= ~1

        self.LCD_Write(0b00000100 | self._entryState)
        self.delayMicroseconds(37)

    # Part of Display control
    def display(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState |= 1 << 2

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMicroseconds(37)

    # Part of Display control
    def noDisplay(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState &= ~(1 << 2)

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMicroseconds(37)

    # Part of Display control
    def cursor(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState |= 1 << 1

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMicroseconds(37)

    # Part of Display control
    def noCursor(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState &= ~(1 << 1)

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMicroseconds(37)

    # Part of Display control
    def blink(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState |= 1

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMicroseconds(37)

    # Part of Display control
    def noBlink(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState &= ~1

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMicroseconds(37)

    # Part of Cursor or display shift
    def scrollDisplayLeft(self):
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00011000)
        self.delayMicroseconds(37)

    # Part of Cursor or display shift
    def scrollDisplayRight(self):
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00011100)
        self.delayMicroseconds(37)

    # Set CGRAM address
    def createChar(self, location, charmap=[]):
        self._output.rs = 0
        self._output.rw = 0

        location %= 8

        self.LCD_Write(0b01000000 | (location << 3))
        self.delayMicroseconds(37)

        for i in charmap:
            self.write(i)

        self.setCursor(0, 0)  # Set the address pointer back to the DDRAM

    # Set DDRAM address
    def setCursor(self, col, row):
        row_offsets = []
        row_offsets.extend([0x00, 0x40, 0x14, 0x54])
        self._output.rs = 0
        self._output.rw = 0

        if col > self._columnMax:
            col = self._columnMax  # sanity limits
        if row > self._rowMax:
            row = self._rowMax  # sanity limits

        newAddress = row_offsets[row] + col

        self.LCD_Write(0b10000000 | newAddress)
        self.delayMicroseconds(37)

    def write(self, character):
        self._output.rs = 1
        self._output.rw = 0

        self.LCD_Write(character)
        self.delayMicroseconds(41)

        return 1

    def InitializeLCD(self):
        # See HD44780U datasheet "Initializing by Instruction" Figure 24 (4-Bit Interface)
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00110000, True)
        self.delayMicroseconds(4200)
        self.LCD_Write(0b00110000, True)
        self.delayMicroseconds(150)
        self.LCD_Write(0b00110000, True)
        self.delayMicroseconds(37)
        self.LCD_Write(0b00100000, True)  # Function Set - 4 bits mode
        self.delayMicroseconds(37)
        self.LCD_Write(0b00101000)  # Function Set - 4 bits(Still), 2 lines, 5x8 font
        self.delayMicroseconds(37)

        self.display()
        # self.home()
        self.clear()
        self.leftToRight()

    def I2C_Write(self, output):
        self.board.i2c_write(self._address, [output])

    #        Wire.beginTransmission(_address)
    #        Wire.write(output)
    #        Wire.endTransmission()

    def LCD_Write(self, output, initialization=False):
        self._output.data = output

        self._output.E = True
        self.I2C_Write(self._output.GetHighData())
        self.delayMicroseconds(1)  # High part of enable should be >450 nS

        self._output.E = False
        self.I2C_Write(self._output.GetHighData())

        # During initialization we only send half a byte
        if not initialization:
            self.delayMicroseconds(37)  # I think we need a delay between half byte writes, but no sure how long it needs to be.

            self._output.E = True
            self.I2C_Write(self._output.GetLowData())
            self.delayMicroseconds(1)  # High part of enable should be >450 nS

            self._output.E = False
            self.I2C_Write(self._output.GetLowData())
        # self.delayMicroseconds(37); # Some commands have different timing requirement,
        # so every command should handle its own delay after execution

    def delayMicroseconds(self, microsec):
        time.sleep(microsec * 1e-6)

    def delayMiliseconds(self, milisec):
        time.sleep(milisec * 1e-3)

    def print(self, text):
        for c in bytearray(text, 'ASCII'):
            self.write(c)
#            self.
