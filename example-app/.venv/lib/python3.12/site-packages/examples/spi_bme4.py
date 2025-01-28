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
This is a very simple program to read the temperature using the BMe280 device.
The code is a loosely based port of the Sparkfun BME280 library and SPI example.
https://github.com/sparkfun/SparkFun_BME280_Arduino_Library

Note: the temperature reported may not be accurate. The intent of this program is to
provide examples of using the telemetrix API.
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

        self.chip_select_pin = chip_select_pin

        # some "constants"
        self.BME_280_ID_REGISTER = 0xD0
        self.VALID_ID_VALUE = 96
        self.SLEEP_MODE = 0
        self.NORMAL_MODE = 3

        # temp calibration registers
        self.BME280_DIG_T1_LSB_REG = 0x88
        self.BME280_DIG_T1_MSB_REG = 0x89
        self.BME280_DIG_T2_LSB_REG = 0x8A
        self.BME280_DIG_T2_MSB_REG = 0x8B
        self.BME280_DIG_T3_LSB_REG = 0x8C
        self.BME280_DIG_T3_MSB_REG = 0x8D

        # temperature calibration data
        self.calibration_T1 = None
        self.calibration_T2 = None
        self.calibration_T3 = None

        # control register
        self.BME280_CTRL_MEAS_REG = 0xF4
        self.control_register_value = None

        # temperature register
        self.BME280_TEMPERATURE_MSB_REG = 0xFA

        # flag to indicate that program is waiting
        # upon a report

        self.report_ready = False

        # instantiate telemetrix
        self.board = telemetrix.Telemetrix(arduino_wait=4)

        # initialize the SPI interface
        self.board.set_pin_mode_spi([self.chip_select_pin])
        time.sleep(1)

        # initialize the device
        self.init_device()

        # continuously read the temperature
        self.get_temperature()

    def init_device(self):

        print('Initializing BME280...')

        # get id byte from bme280

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME_280_ID_REGISTER,
                                     1, call_back=self.device_callback)
        self.report_ready = False

        # read calibration values for temperature
        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_DIG_T1_MSB_REG,
                                     1, call_back=self.device_callback)
        while not self.report_ready:
            time.sleep(.001)
        self.report_ready = False

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_DIG_T1_LSB_REG,
                                     1, call_back=self.device_callback)
        while not self.report_ready:
            time.sleep(.001)
        self.report_ready = False

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_DIG_T2_MSB_REG,
                                     1, call_back=self.device_callback)
        while not self.report_ready:
            time.sleep(.001)
        self.report_ready = False

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_DIG_T2_LSB_REG,
                                     1, call_back=self.device_callback)

        while not self.report_ready:
            time.sleep(.001)
        self.report_ready = False

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_DIG_T3_MSB_REG,
                                     1, call_back=self.device_callback)
        while not self.report_ready:
            time.sleep(.001)
        self.report_ready = False

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME280_DIG_T3_LSB_REG,
                                     1, call_back=self.device_callback)
        while not self.report_ready:
            time.sleep(.001)
        self.report_ready = False

        print(f't1 {self.calibration_T1} t2 {self.calibration_T2} t2 '
              f'{self.calibration_T3}')

        # get current control register value
        self.board.spi_read_blocking(self.chip_select_pin, self.BME280_CTRL_MEAS_REG,
                                     1, call_back=self.device_callback)
        while not self.report_ready:
            time.sleep(.001)

        self.report_ready = False

        print(f'control register: {self.control_register_value}')

        # set mode to sleep
        self.board.spi_write_blocking(self.chip_select_pin, [self.BME280_CTRL_MEAS_REG,
                                                             self.SLEEP_MODE])
        time.sleep(.3)

        # Set the osrs_t bits (7, 6, 5) to overSampleAmount
        self.board.spi_read_blocking(self.chip_select_pin, self.BME280_CTRL_MEAS_REG,
                                     1, call_back=self.device_callback)
        while not self.report_ready:
            time.sleep(.001)

        self.report_ready = False
        # Clear bits 765
        self.control_register_value &= ~((1 << 7) | (1 << 6) | (1 << 5))
        over_sample_amount = 1
        self.control_register_value |= over_sample_amount << 5  # Align overSampleAmount to bits 7/6/5
        self.board.spi_write_blocking(self.chip_select_pin, [self.BME280_CTRL_MEAS_REG,
                                                             self.control_register_value])
        print(f'updated cr: {self.control_register_value}')
        time.sleep(.3)

        # set measurement mode to normal
        self.board.spi_write_blocking(self.chip_select_pin, [self.BME280_CTRL_MEAS_REG,
                                                             35])
        time.sleep(.3)

        # self.board.spi_write_blocking(self.chip_select_pin, [self.BME280_CTRL_MEAS_REG,
        #                                                      35])
        time.sleep(.3)

        self.board.spi_read_blocking(self.chip_select_pin,
                                     self.BME_280_ID_REGISTER,
                                     1, call_back=self.device_callback)
        self.report_ready = False

        # write8(BME280_REGISTER_CONTROL, 163)

        # finally reread the ID byte to make sure nothing has changed
        # self.board.spi_read_blocking(self.chip_select_pin,
        #                              self.BME_280_ID_REGISTER,
        #                              1, call_back=self.device_callback)
        # time.sleep(.3)

        print('BME280 successfully initialized!')

    def get_temperature(self):
        """
        Continuously retrieve temperature in degrees C.
        """

        while True:
            try:
                self.board.spi_read_blocking(self.chip_select_pin,
                                             self.BME280_TEMPERATURE_MSB_REG,
                                             3,
                                             call_back=self.device_callback)
                time.sleep(2)

            except KeyboardInterrupt:
                self.board.shutdown()
                sys.exit(0)

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
                    self.report_ready = True
                    return
                else:
                    print(f'Invalid ID: {data[START_OF_DATA]}')
                    self.report_ready = True

            # calibration data handlers
            elif data[REGISTER] == self.BME280_DIG_T1_MSB_REG:
                self.calibration_T1 = data[START_OF_DATA] << 8
                self.report_ready = True
            elif data[REGISTER] == self.BME280_DIG_T1_LSB_REG:
                self.calibration_T1 += data[START_OF_DATA]
                self.report_ready = True
                # print(f't1 {self.calibration_T1}')

            elif data[REGISTER] == self.BME280_DIG_T2_MSB_REG:
                self.calibration_T2 = data[START_OF_DATA] << 8
                self.report_ready = True
            elif data[REGISTER] == self.BME280_DIG_T2_LSB_REG:
                self.calibration_T2 += data[START_OF_DATA]
                self.report_ready = True
                # print(f't2 {self.calibration_T2}')

            elif data[REGISTER] == self.BME280_DIG_T3_MSB_REG:
                self.calibration_T3 = data[START_OF_DATA] << 8
                self.report_ready = True

            elif data[REGISTER] == self.BME280_DIG_T3_LSB_REG:
                self.calibration_T3 += data[START_OF_DATA]
                self.report_ready = True
                # print(f't3 {self.calibration_T3}')

            elif data[REGISTER] == self.BME280_CTRL_MEAS_REG:
                self.control_register_value = data[START_OF_DATA] & 0x3
                self.report_ready = True

            # temperature data handler
            elif data[REGISTER] == self.BME280_TEMPERATURE_MSB_REG:
                print(f'temp data = {data}')
                raw_temperature = data[START_OF_DATA] << 12 or data[START_OF_DATA + 1] \
                                  << 4 or ((data[START_OF_DATA + 2] >> 4) & 0x0F)
                print(raw_temperature)
                time.sleep(.5)
                print('here')

                """

                var1 = (((raw_temperature >> 3) - (self.calibration_T1 << 1)) * \
                        self.calibration_T2) >> 11

                var2 = (((((raw_temperature >> 4) - (self.calibration_T1)) * (
                        (raw_temperature >> 4) - (self.calibration_T1))) >> 12) *
                        self.calibration_T1) >> 14

                t_fine = var1 + var2

                output = (t_fine * 5 + 128) >> 8

                output = output / 100
                """
                # print(
                #     f'Temperature - degrees C: {output}  degrees F:
                #    {(output * 9) / 5 + 32}')


CS_PIN = 10

bme = BME280Spi(CS_PIN)
