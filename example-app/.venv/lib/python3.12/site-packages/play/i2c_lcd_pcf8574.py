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
        board.i2c_write(self._address, [0])

    def begin(self):
        self.delayMiliseconds(50)  # Wait more than 40ms after powerOn.
        self.I2C_Write(0b00000000)  # Clear i2c adapter
        self.delayMiliseconds(50)  # Wait more than 40ms after powerOn.

        self.InitializeLCD()

    def backlight(self):
        self._output.Led = 1
        # Led pin is independent of LCD data and control lines.
        self.I2C_Write(0b00000000 | self._output.Led << 3)

    def noBacklight(self):
        self._output.Led = 0
        # Led pin is independent of LCD data and control lines.
        self.I2C_Write(0b00000000 | self._output.Led << 3)

    def clear(self):
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00000001)
        self.delayMiliseconds(160)

    def home(self):
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00000010)
        self.delayMiliseconds(160)

    # Part of Entry mode set
    def leftToRight(self):
        self._output.rs = 0
        self._output.rw = 0

        self._entryState |= 1 << 1

        self.LCD_Write(0b00000100 | self._entryState)
        self.delayMiliseconds(37)

    # Part of Entry mode set
    def rightToLeft(self):
        self._output.rs = 0
        self._output.rw = 0

        self._entryState &= ~(1 << 1)

        self.LCD_Write(0b00000100 | self._entryState)
        self.delayMiliseconds(37)

    # Part of Entry mode set
    def autoscroll(self):
        self._output.rs = 0
        self._output.rw = 0

        self._entryState |= 1

        self.LCD_Write(0b00000100 | self._entryState)
        self.delayMiliseconds(37)

    # Part of Entry mode set
    def noAutoscroll(self):
        self._output.rs = 0
        self._output.rw = 0

        self._entryState &= ~1

        self.LCD_Write(0b00000100 | self._entryState)
        self.delayMiliseconds(37)

    # Part of Display control
    def display(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState |= 1 << 2

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMiliseconds(37)

    # Part of Display control
    def noDisplay(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState &= ~(1 << 2)

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMiliseconds(37)

    # Part of Display control
    def cursor(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState |= 1 << 1

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMiliseconds(37)

    # Part of Display control
    def noCursor(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState &= ~(1 << 1)

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMiliseconds(37)

    # Part of Display control
    def blink(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState |= 1

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMiliseconds(37)

    # Part of Display control
    def noBlink(self):
        self._output.rs = 0
        self._output.rw = 0

        self._displayState &= ~1

        self.LCD_Write(0b00001000 | self._displayState)
        self.delayMiliseconds(37)

    # Part of Cursor or display shift
    def scrollDisplayLeft(self):
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00011000)
        self.delayMiliseconds(37)

    # Part of Cursor or display shift
    def scrollDisplayRight(self):
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00011100)
        self.delayMiliseconds(37)

    # Set CGRAM address
    def createChar(self, location, charmap=[]):
        self._output.rs = 0
        self._output.rw = 0

        location %= 8

        self.LCD_Write(0b01000000 | (location << 3))
        self.delayMiliseconds(37)

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
        self.delayMiliseconds(37)

    def write(self, character):
        self._output.rs = 1
        self._output.rw = 0

        self.LCD_Write(character)
        self.delayMiliseconds(41)

        return 1

    def InitializeLCD(self):
        # See HD44780U datasheet "Initializing by Instruction" Figure 24 (4-Bit Interface)
        self._output.rs = 0
        self._output.rw = 0

        self.LCD_Write(0b00110000, True)
        self.delayMiliseconds(42)
        self.LCD_Write(0b00110000, True)
        self.delayMiliseconds(150)
        self.LCD_Write(0b00110000, True)
        self.delayMiliseconds(37)
        self.LCD_Write(0b00100000, True)  # Function Set - 4 bits mode
        self.delayMiliseconds(37)
        self.LCD_Write(0b00101000)  # Function Set - 4 bits(Still), 2 lines, 5x8 font
        self.delayMiliseconds(37)

        self.display()
        self.clear()
        self.leftToRight()

    def I2C_Write(self, output):
        self.board.i2c_write(self._address, [output])

    def LCD_Write(self, output, initialization=False):
        self._output.data = output

        self._output.E = True
        self.I2C_Write(self._output.GetHighData())
        self.delayMicroseconds(1)  # High part of enable should be >450 nS

        self._output.E = False
        self.I2C_Write(self._output.GetHighData())

        # During initialization, we only send half a byte
        if not initialization:
            # I think we need a delay between half byte writes,
            # but no sure how long it needs to be.
            self.delayMicroseconds(37)

            self._output.E = True
            self.I2C_Write(self._output.GetLowData())
            self.delayMicroseconds(1)  # High part of enable should be >450 nS

            self._output.E = False
            self.I2C_Write(self._output.GetLowData())
        # self.delayMicroseconds(37) # Some commands have different timing requirement,
        # so every command should handle its own delay after execution

    def delayMicroseconds(self, microsec):
        time.sleep(microsec * 1e-6)

    def delayMiliseconds(self, milisec):
        time.sleep(milisec * 1e-3)

    def print(self, text):
        for c in bytearray(text, 'ASCII'):
            self.write(c)
