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

"""

"""
This is a very simple program to read the BME280 id byte using an SPI interface.
It will change the SPI frequency and then do another read.
"""

import time
import sys
from telemetrix import telemetrix

CHIP_SELECT_PIN = 10

BME280_ID_REGISTER = 0xD0

NUM_BYTE_TO_READ = 1  # the BME280 ID is a single byte

VALID_ID_RETURN = 96


def device_callback(data):

    print(data)
    # Index to spi register value in data
    REGISTER = 2

    # Index to returned ID value in data
    ID_VALUE = 4

    if data[REGISTER] == BME280_ID_REGISTER:
        if data[ID_VALUE] == 96:
            print('Valid ID returned')
        else:
            print(f'Invalid ID: {data[ID_VALUE]}')


# instantiate an instance of Telemetrix
board = telemetrix.Telemetrix()

# Enable the SPI interface using pin 10 as the Chip Select Pin
board.set_pin_mode_spi([CHIP_SELECT_PIN])

print('Retrieving ID byte')

board.spi_read_blocking(CHIP_SELECT_PIN, BME280_ID_REGISTER,  NUM_BYTE_TO_READ,
                        call_back=device_callback)
time.sleep(1)
print("Changing SPI settings an then rereading ID Byte")
board.spi_set_format(8, 1, 0)
time.sleep(1)
board.spi_read_blocking(CHIP_SELECT_PIN, BME280_ID_REGISTER,  1,  call_back=device_callback)
time.sleep(1)
board.shutdown()
sys.exit(0)

