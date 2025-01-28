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

"""

"""
This is a program to read a BME280 humidity, pressure and temperature sensor.
The code is a loosely based upon https://github.com/Zanduino/BME280

"""

import time
import sys
from telemetrix import telemetrix


class BME280Spi:
    """
    This class provides SPI control of a BME280
    """

    def __init__(self, chip_select_pin=10):
        """

        :param chip_select_pin: SPI chip select pin used for this device
        """

        # BME280 Register Constants
        
        
        self.BM280_CHIPID_REG = 0xD0 # ID register
        self.BM280_CHIPID = 0x60 # expected ID

        self.BM280_SOFT_RESET_REG = 0xE0  # Reset when 0xB6 is written here
        self.BM280_RESET_CODE = 0xB6

        self.BM280_CONTROL_HUMID_REG = 0xF2
        
        self.BM280_STATUS_REG = 0xF3
        
        self.BM280_CONTROL_REG = 0xF4
        
        self.BM280_CONFIG_REG = 0xF5
        
        self.BM280_PRESSURE_DATA_REG = 0xF7
        
        self.BM280_TEMP_DATA_REG = 0xFA        
        
        self.BM280_HUMID_DATA_REG = 0xFD
        
        # calibration registers
        
        # temperature
        self.BM280_T1_REG = 0x88
            
        self.BM280_T2_REG = 0x8A
        
        self.BM280_T3_REG = 0x8C
        
        # pressure
        self.BM280_P1_REG = 0x8E
        
        self.BM280_P2_REG = 0x90
        
        self.BM280_P3_REG = 0x92
        
        self.BM280_P4_REG = 0x94
        
        self.BM280_P5_REG = 0x96
        
        self.BM280_P6_REG = 0x98
        
        self.BM280_P7_REG = 0x9A
        
        self.BM280_P8_REG = 0x9C
        
        self.BM280_P9_REG = 0x9E
        
        # humidity
        self.BM280_H1_REG = 0xA1
        
        self.BM280_H2_REG = 0xE1
        
        self.BM280_H3_REG = 0xE3
        
        self.BM280_H4_REG = 0xE4
        
        self.BM280_H5_REG = 0xE5
        
        self.BM280_H6_REG = 0xE7

        

        # temperature calibration data
        self.calibration_T1 = None
        self.calibration_T2 = None
        self.calibration_T3 = None

        self.chip_select_pin = chip_select_pin

        # instantiate telemetrix
        self.board = telemetrix.Telemetrix(arduino_wait=4)

        # initialize the SPI interface
        self.board.set_pin_mode_spi([self.chip_select_pin])
        time.sleep(.3)

        # self.board.spi_set_format(2, 1, 0)

        # initialize the device
        self.init_device()

        time.sleep(1)

        # continuously read the temperature
        self.get_temperature()

    def device_callback(self, data):
        """
        :param data: Report data sent from the board resident telemetrix sketch

        Indices into data:
            chip_select_pin = 1
            register = 2
            number bytes returned = 3
            data bytes 4...
        """
        # Index to spi register value in data
        CHIP_SELECT = 1
        REGISTER = 2
        # NUMBER_OF_BYTES_RETURNED = 3
        START_OF_DATA = 4

        if data[CHIP_SELECT] == self.chip_select_pin:
            # chip ID handler
            if data[REGISTER] == self.BME_280_ID_REGISTER:
                if data[START_OF_DATA] == 96:
                    # print('Valid ID returned')
                    return
                else:
                    print(f'Invalid ID: {data[START_OF_DATA]}')

            # calibration data handlers
            elif data[REGISTER] == self.BME280_REGISTER_DIG_T1:
                self.calibration_T1 = (data[START_OF_DATA] >> 8) | (data[START_OF_DATA +
                                                                       1] << 8)

            elif data[REGISTER] == self.BME280_REGISTER_DIG_T2:
                self.calibration_T2 = (data[START_OF_DATA] >> 8) | (data[START_OF_DATA +
                                                                       1] << 8)

            elif data[REGISTER] == self.BME280_REGISTER_DIG_T3:
                self.calibration_T3 = (data[START_OF_DATA] >> 8) | (data[START_OF_DATA +
                                                                       1] << 8)

                print(f'cal t1: {self.calibration_T1}  cal t2: {self.calibration_T2} '
                      f'cal t3: {self.calibration_T3} ')

        # temperature data handler
            elif data[REGISTER] == self.BME280_TEMPERATURE_REG:
                print(data)
                raw_data = bytearray()
                raw_data.append(data[START_OF_DATA])
                raw_data.append(data[START_OF_DATA + 1])
                raw_data.append(data[START_OF_DATA + 2])

                raw_value = int.from_bytes(raw_data, "big")

                print(f'raw value {raw_value}')

                adjusted_value = raw_value >> 4

                print(f'adjusted: {adjusted_value}')

                var1 = (adjusted_value / 8) - (self.calibration_T1 * 2)
                var1 = (var1 * self.calibration_T2) / 2048
                var2 = (adjusted_value / 16) - self.calibration_T1
                var2 = ((var2 * var2) / 4096) * (self.calibration_T3 / 16384)

                print(f'var1 = {var1}  var2 = {var2}')

                t_fine = var1 + var2

                T = ((t_fine * 5 + 128) / 256) / 100

                print(f'Temperature - degrees C: {T:.2f}  degrees F: '
                      f'{((T * 9) / 5 + 32):.2f}')

    def init_device(self):

        print('Initializing BME280...')

        # get id byte from bme280

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME_280_ID_REGISTER,
                                     1, call_back=self.device_callback)
        # read calibration values for temperature
        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_REGISTER_DIG_T1,
                                     2, call_back=self.device_callback)
        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_REGISTER_DIG_T2,
                                     2, call_back=self.device_callback)

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_REGISTER_DIG_T3,
                                     2, call_back=self.device_callback)

        # set measurement mode to normal
        self.board.spi_write_blocking(self.chip_select_pin, [self.BME280_CTRL_MEAS_REG,
                                                             163])
        print('BME280 successfully initialized!')

    def get_temperature(self):
        """
        Continuously retrieve temperature in degrees C.
        """

        while True:
            try:
                self.board.spi_read_blocking(self.chip_select_pin,
                                             self.BME280_TEMPERATURE_REG,
                                             3,
                                             call_back=self.device_callback)
                time.sleep(.5)

            except KeyboardInterrupt:
                self.board.shutdown()
                sys.exit(0)


CS_PIN = 10

bme = BME280Spi(CS_PIN)
