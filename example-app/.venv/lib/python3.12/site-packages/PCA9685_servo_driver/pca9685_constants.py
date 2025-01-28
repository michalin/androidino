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
This file contains the register and other values to control the PCA9685 i2c Servo
Driver. The code is based upon the Adafruit library located at:
https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library
"""

# REGISTER ADDRESSES
PCA9685_MODE1 = 0x00  # Mode Register 1
PCA9685_MODE2 = 0x01  # Mode Register 2
PCA9685_SUBADR1 = 0x02  # I2C-bus subaddress 1
PCA9685_SUBADR2 = 0x03  # I2C-bus subaddress 2
PCA9685_SUBADR3 = 0x04  # I2C-bus subaddress 3
PCA9685_ALLCALLADR = 0x05  # LED All Call I2C-bus address
PCA9685_LED0_ON_L = 0x06  # LED0 on tick, low byte
PCA9685_LED0_ON_H = 0x07  # LED0 on tick, high byte
PCA9685_LED0_OFF_L = 0x08  # LED0 off tick, low byte
PCA9685_LED0_OFF_H = 0x09  # LED0 off tick, high byte

#  etc all 16:  LED15_OFF_H = 0x45
PCA9685_ALLLED_ON_L = 0xFA  # load all the LEDn_ON registers, low 
PCA9685_ALLLED_ON_H = 0xFB  # load all the LEDn_ON registers, high 
PCA9685_ALLLED_OFF_L = 0xFC  # load all the LEDn_OFF registers, low
PCA9685_ALLLED_OFF_H = 0xFD  # load all the LEDn_OFF registers,high
PCA9685_PRESCALE = 0xFE  # Prescaler for PWM output frequency
PCA9685_TESTMODE = 0xFF  # defines the test mode to be entered

#  MODE1 bits
# noinspection GrazieInspection
MODE1_ALLCAL = 0x01  # respond to LED All Call I2C-bus address
MODE1_SUB3 = 0x02  # respond to I2C-bus subaddress 3
MODE1_SUB2 = 0x04  # respond to I2C-bus subaddress 2
MODE1_SUB1 = 0x08  # respond to I2C-bus subaddress 1
MODE1_SLEEP = 0x10  # Low power mode. Oscillator off
MODE1_AI = 0x20  # Auto-Increment enabled
MODE1_EXTCLK = 0x40  # Use EXTCLK pin clock 
MODE1_RESTART = 0x80  # Restart enabled
# MODE2 bits
MODE2_OUTNE_0 = 0x01  # Active LOW output enable input
MODE2_OUTNE_1 = 0x02  # Active LOW output enable input - high impedance
MODE2_OUTDRV = 0x04  # totem pole structure vs open-drain
MODE2_OCH = 0x08  # Outputs change on ACK vs STOP
MODE2_INVRT = 0x10  # Output logic state inverted 

PCA9685_I2C_ADDRESS = 0x40  # Default PCA9685 I2C Slave Address
FREQUENCY_OSCILLATOR = 27000000  # Int. osc. frequency in datasheet

PCA9685_PRESCALE_MIN = 3  # minimum prescale value
PCA9685_PRESCALE_MAX = 255  # maximum prescale value

DEFAULT_PWM_FREQUENCY = 50
