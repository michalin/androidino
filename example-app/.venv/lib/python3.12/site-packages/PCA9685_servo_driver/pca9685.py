"""
 Copyright (c) 2021 Alan Yorinks All rights reserved.

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

"""
This file is contains the class to control a PCA9685 i2c servo driver.
The code is loosely based upon the Adafruit library located at:
https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library
"""

import time

import pca9685_constants
from telemetrix import telemetrix


# noinspection GrazieInspection
class PCA9685:
    def __init__(self, i2c_address=pca9685_constants.PCA9685_I2C_ADDRESS,
                 osc_freq=pca9685_constants.FREQUENCY_OSCILLATOR,
                 i2c_port=0, prescale=0, board=None, position_min=150,
                 position_max=600):
        """

        :param i2c_address: i2c device address
        :param i2c_port: 0 or 1 for 2 port devices
        :param prescale: prescale value for external clock (optional)
        :param board: instance of Telemetrix. If none, one will be created.
        :param position_min: minimum servo position
        :param position_max: maximum servo position
        """
        self.i2c_address = i2c_address
        self.i2c_port = i2c_port
        self.prescale = prescale
        self.position_min = position_min
        self.position_max = position_max

        self.totempole = True
        self.pwm_data = None

        self.oscillator_freq = osc_freq

        self.position_per_degree = (self.position_max - self.position_min) // 180

        self.write_m_servo_number_pulse = []

        # create a telemetrix instance
        if board:
            self.board = board
        else:
            self.board = telemetrix.Telemetrix()

        # initialize the PCA9685
        self.board.set_pin_mode_i2c(self.i2c_port)
        self.reset()

        # set clock
        if self.prescale:
            self.set_ext_clk(self.prescale)
        else:
            # set a default pwm frequency
            self.set_pwm_freq(pca9685_constants.DEFAULT_PWM_FREQUENCY)

        # set default internal frequency
        self.set_oscillator_frequency(pca9685_constants.FREQUENCY_OSCILLATOR)

    def reset(self):
        """
        Sends a reset command to the PCA9685 chip over I2C
        """
        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                pca9685_constants.MODE1_RESTART])
        time.sleep(0.01)

    def sleep(self):
        """
        Puts board into sleep mode
        First performs a read, and then processes return
        in _i2c_read_complete_sleep
        """
        self.board.i2c_read(self.i2c_address,
                            pca9685_constants.PCA9685_MODE1, 1,
                            self._i2c_read_complete_sleep)
        time.sleep(.5)

    def _i2c_read_complete_sleep(self, data):
        """
        Finish processing sleep command
        :param data: data from i2c device
        """
        # data is [i2c_read_report, port, number of bytes read, i2c address,
        #           device_register, data value, time_stamp]
        awake = data[5]
        # set sleep-bit high
        sleep_value = awake | pca9685_constants.MODE1_SLEEP

        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                sleep_value])
        time.sleep(.005)  # wait until cycle ends for sleep to be active

    def wakeup(self):
        """
        Wakes board from sleep.
        First performs a read, and then continues processing
        in the _i2c_read_complete_wake callback.
        """
        self.board.i2c_read(self.i2c_address,
                            pca9685_constants.PCA9685_MODE1, 1,
                            self._i2c_read_complete_wake)
        time.sleep(0.5)

    def _i2c_read_complete_wake(self, data):
        # data is [i2c_read_report, port, number of bytes read, i2c address,
        #           device_register, data value, time_stamp]
        sleep = data[5]
        # set sleep-bit high
        wake = sleep & ~pca9685_constants.MODE1_SLEEP

        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                wake])
        time.sleep(0.05)

    def set_ext_clk(self, prescale):
        """
        Sets EXTCLK pin to use the external clock
        First, performs a read, and then continues
        processing in the _i2c_read_complete_ext_clock callback.

        """
        self.prescale = prescale
        self.board.i2c_read(self.i2c_address,
                            pca9685_constants.PCA9685_MODE1, 1,
                            self._i2c_read_complete_ext_clock)
        time.sleep(0.5)

    def _i2c_read_complete_ext_clock(self, data):
        # data is [i2c_read_report, port, number of bytes read, i2c address,
        #           device_register, data value, time_stamp]
        old_mode = data[5]  # offset of 5 is the External Clock data value
        new_mode = (old_mode & ~pca9685_constants.MODE1_RESTART) | \
                   pca9685_constants.MODE1_SLEEP

        # go to sleep, turn off internal oscillator
        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                new_mode])
        # this sets the SLEEP and EXTCLK bits of the mode1 register to
        # switch to use the external clock

        write_value = new_mode | pca9685_constants.MODE1_EXTCLK
        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                write_value])

        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_PRESCALE,
                                                self.prescale])
        time.sleep(.005)

        # clear the SLEEP bit to start
        write_value = (new_mode & ~pca9685_constants.MODE1_SLEEP)
        write_value |= pca9685_constants.MODE1_RESTART
        write_value |= pca9685_constants.MODE1_AI

        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                write_value])

        time.sleep(0.05)

    def set_pwm_freq(self, freq):
        """
        Sets the PWM frequency for the entire chip, up to ~1.6 KHz
        Begins with a read, and then continues processing in the
        _i2c_read_complete_set_pwm_freq callback

        :param freq: Floating point frequency that we will attempt to match
        """
        if freq < 1:
            freq = 1
        if freq > 3500:
            freq = 3500

        prescale_value = ((self.oscillator_freq / (freq * 4096.0)) + 0.5) - 1

        if prescale_value < pca9685_constants.PCA9685_PRESCALE_MIN:
            prescale_value = pca9685_constants.PCA9685_PRESCALE_MIN
        if prescale_value > pca9685_constants.PCA9685_PRESCALE_MAX:
            prescale_value = pca9685_constants.PCA9685_PRESCALE_MAX

        self.prescale = int(prescale_value)

        self.board.i2c_read(self.i2c_address,
                            pca9685_constants.PCA9685_MODE1, 1,
                            self._i2c_read_complete_set_pwm_freq)

    def _i2c_read_complete_set_pwm_freq(self, data):
        old_mode = data[5]  # offset 5 is the reported mode value
        new_mode = (old_mode & ~pca9685_constants.MODE1_RESTART) | \
                   pca9685_constants.MODE1_SLEEP
        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                new_mode])
        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_PRESCALE,
                                                int(self.prescale)])
        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                old_mode])
        time.sleep(0.005)

        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE1,
                                                old_mode |
                                                pca9685_constants.MODE1_RESTART |
                                                pca9685_constants.MODE1_AI])

    def set_output_mode(self, totempole=True):
        """
        Sets the output mode of the PCA9685 to either
        open drain or push pull / totempole.

        Begins with a read and completes the operation
        in the _i2c_read_complete_set_output callback

        Warning: LEDs with integrated zener diodes should
        only be driven in open drain mode.

        :param totempole: If true set to totempole, open drain if false.
        """
        self.totempole = totempole
        self.board.i2c_read(self.i2c_address,
                            pca9685_constants.PCA9685_MODE2, 1,
                            self._i2c_read_complete_set_output)
        time.sleep(0.5)

    def _i2c_read_complete_set_output(self, data):
        old_mode = data[5]
        if self.totempole:
            new_mode = old_mode | pca9685_constants.MODE2_OUTDRV
        else:
            new_mode = old_mode & ~pca9685_constants.MODE2_OUTDRV
        self.board.i2c_write(self.i2c_address, [pca9685_constants.PCA9685_MODE2,
                                                new_mode])

    def read_pre_scale(self):
        """
        Returns prescale value set in the device
        Begins with a read and completes the process in
        the _i2c_read_complete_read_prescale callback
        :return: prescale value
        """
        self.prescale = None
        self.board.i2c_read(self.i2c_address, pca9685_constants.PCA9685_PRESCALE, 1,
                            self._i2c_read_complete_read_prescale)
        time.sleep(0.05)

    def _i2c_read_complete_read_prescale(self, data):
        """
        data[5] = data value returned
        Modify this callback to notify your code when it
        is executed.
        :param data:
        :return:
        """
        self.prescale_read = True
        self.prescale = int(data[5])  # data value returned

    def get_pwm(self, num):
        """
        Gets the PWM output of one of the PCA9685 pins
        :param num: One of the PWM output pins (0 - 15)
        :return: requested PWM output value
        """
        self.pwm_data = None
        register = pca9685_constants.PCA9685_LED0_ON_L + 4 * num
        self.board.i2c_read(self.i2c_address,
                            register, 4,
                            self._i2c_read_complete_get_pwm)

    def _i2c_read_complete_get_pwm(self, data):
        """
        Modify this method to notify your code when the read
        completes
        :param data[5]: pwm value
        """
        self.pwm_data = data[5]

    def set_pwm(self, num, on, off):
        """
        Sets the PWM output of one of the PCA9685 pins
        :param num: One of the PWM output pins (0 - 15)
        :param on: Point in the 4096-part cycle to turn the PWM output ON
        :param off: Point in the 4096-part cycle to turn the PWM output OFF
        :return:
        """
        self.board.i2c_write(self.i2c_address,
                             [pca9685_constants.PCA9685_LED0_ON_L + 4 * num, on & 0xff,
                              on >> 8, off & 0xff, off >> 8])

    def set_pin(self, num, value, invert=False):
        """
        Helper to set pin PWM output.
        Sets pin without having to deal with on/off tick
        placement and properly handles a zero value as completely off and
        4095 as completely on.  Optional invert parameter supports inverting the
        pulse for sinking to ground.

        :param num: pwm output pin (0 - 15)
        :param value: The number of ticks out of 4096 to be active,
                      should be a value from 0 to 4095 inclusive.
        :param invert: Inverts the output
        """

        # Clamp value between 0 and 4095 inclusive.
        value = min(value, 4095)
        if invert:
            if value == 0:
                # Special value for signal fully on.
                self.set_pwm(num, 4096, 0)
            elif value == 4095:
                # Special value for signal fully off
                self.set_pwm(num, 0, 4096)
            else:
                self.set_pwm(num, 0, 4095 - value)
        else:
            if value == 4095:
                # set fully on
                self.set_pwm(num, 4096, 0)
            elif value == 0:
                # set fully off
                self.set_pwm(num, 0, 4096)
            else:
                self.set_pwm(num, 0, value)

    def get_oscillator_frequency(self):
        """
        Get the internally tracked oscillator frequency.
        :return: oscillator frequency
        """
        return self.oscillator_freq

    def set_oscillator_frequency(self, frequency):
        """
        Set the internally tracked oscillator frequency.
        :param frequency: frequency
        """
        self.oscillator_freq = frequency

    def set_angle(self, servo_num, angle):
        self.set_pwm(servo_num, 0, (angle * self.position_per_degree) + self.position_min)


p = PCA9685()
time.sleep(0.1)
PIN=15
while True:
    for x in range(p.position_min, p.position_max):
        p.set_pwm(PIN, 0, x)
    time.sleep(.5)
    for x in range(p.position_max, p.position_min, -1):
        p.set_pwm(PIN, 0, x)
    time.sleep(.5)

    p.set_angle(PIN, 0)
    time.sleep(1)
    p.set_angle(PIN, 90)
    time.sleep(1)
    p.set_angle(PIN, 180)
    time.sleep(1)
    p.set_angle(PIN, 0)
    time.sleep(1)
