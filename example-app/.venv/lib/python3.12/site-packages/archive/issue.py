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

 DHT support courtesy of Martyn Wheeler
 Based on the DHTNew library - https://github.com/RobTillaart/DHTNew
"""

import sys
import time
import threading
from telemetrix import telemetrix

pinout = {}  # Leave empty
# Dictionary to hold analog pins' raw ADC values.
ADC_results = {
    0: 0,  # pin 0 -> "A0" : 0V
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0
}

# Digital pins based on Arduino Digital pin numbering.
# When number is used for digital_ functions, the number is according to digital pins.  (13 = D13 != A13)
output_pins = {
    "d_LED": 13,  # Internal LED on MEGA
}

# When number is used for analog_ functions, the number is according to analog pins ??  (13 = A13 != D13)
# Alternatively use the digital pin numberation instead.  54 = D54 = A0
analog_input_pins = {
    "a_ADC_A0": 0,
    "a_ADC_A1": 1,
    "a_ADC_A2": 2,
    "a_ADC_A3": 3,
    "a_ADC_A4": 4,
    "a_ADC_A5": 5,
    "a_ADC_A6": 6
}

# merge all pins to one dictionary for easier referencing
pinout = analog_input_pins | output_pins

led_state = 1 # for this example

# Mega has 10bits, thus 0 - 1023
def convert_analog(analog_reading: int, Vs: int = 5):
    return (analog_reading * (Vs / 1023))

## ================================================================================================================

# specific class with Telemetrix interface
class Test:
    def __init__(self, com_port=None, arduino_instance_id=1):
        self.board = telemetrix.Telemetrix(com_port, arduino_instance_id)
        self.read_analog_timeout = 3  # in seconds.
        self.cb_flag = 0 # callback filter flag. Only do stuff when requested.

        # Configure pins specific to this example
        self.configure_pins()  # Configure test pin definitions. Assumes pins dictionary is well defined

    # Analog input callback function
    def cb_analog_input_read(self, data):
        '''
        Refreshes every analog input readout. This implementation guarantees, the pin of interest is updated.
        So setting any analog pin mode, can be used to read any analog pin result once updated.
        :param data: required by Telemetrix
        :return: currently nothing
        '''
        if (self.cb_flag == 1): # Filter. Only act when requested. Otherwise callback is empty and terminates quickly.
            print(f'Stored value: Pin Type: {data[0]} Pin: {data[1]} Value: {data[2]}')
            ADC_results[data[1]] = data[2]  # Store the measured value at the corresponding analog pin index
            self.cb_flag = 0  # reset the flag - otherwise no way of stopping the reporting spam.

        ''' message just to show how much callback is piling up and increases calls within the script flow '''
        print(f'Spamming callback from  Pin: {data[1]}')
        # return data  # not needed at the moment as no way of getting the return from callback ?


    def configure_pins(self):
        # If you setting the mode for multiple pins, you may wish to add a short delay after setting each pin.
        # https: // mryslab.github.io / telemetrix / pin_modes /

        # Outputs
        for x in output_pins:  # iterating through outputs to configure them as outputs in Arduino
            self.board.set_pin_mode_digital_output(output_pins[x])
            time.sleep(.02)
        print(f'# Digital output set done')

        # Analog inputs
        # This seems unnecessary to be done at startup. Since during read_analog, this pretty much repeats per pin.
        print("# Setting analog inputs:")
        for x in analog_input_pins:
            # Once pin_mode is set, callbacks are automatically enabled.
            self.board.set_pin_mode_analog_input(analog_input_pins[x], callback=self.cb_analog_input_read)
            self.board.disable_analog_reporting(analog_input_pins[x]) # immediately stop reporting spam
            time.sleep(.02)
        self.board.set_analog_scan_interval(200)
        print(f'# Analog input set done')

    def read_analog(self, a_pin_name: str, delay=0.5):
        '''
        :param a_pin_name: string of a pin name written in the dictionary pinout
        :param delay:   default 0 seconds. Time stalled until reading a measurement.
        :return: ([0]return value, [1]return message)
                 [0] - 0-5V - Specific pin's converted value of raw 10bit ADC value;
                 -1 - cb_flag is not reset during timeout
                 -2 - Reading callback not reached - something wrong with calling the callback;
                 [1] "status message")
        '''
        time.sleep(delay)  # wait for the delay before reading measurement. use >0.1 when making first measurements.
        pin = pinout[a_pin_name]  # get the pin number from dictionary
        self.cb_flag = 1 # set flag to store values in callback

        print(f'# Reading: {a_pin_name}, A{pin}')
        time_now = time.time()  # used to do timeout checks.
        while (self.cb_flag == 1): # as long as flag is set
            if time.time() <= time_now + self.read_analog_timeout:  # implemented some timeout
                # Setting any analog pin causes callback to be activated automatically !
                self.board.set_pin_mode_analog_input(pin, callback=self.cb_analog_input_read)
                time.sleep(0.1)
            else:
                print("analog read timeout")
                return (-1, "analog read timeout")

        if (self.cb_flag == 0):  # check if callback had been reached
            # return converted value
            # print(f'read_analog: {a_pin_name} on {pin}, raw: {ADC_results[pin]}') # dbg
            rslt = convert_analog(ADC_results[pin])
            return (rslt, 'A' + str(pin) + ': ' + str(ADC_results[pin]))
            # result is stored in ADC_results dictionary via callback function.
            # cb_flag is reset also in callback
        else:
            print("analog read callback not reached")
            return (-2, "analog read callback not reached")


    def LED_blink(self, dir_delay: int = 0.5):
        '''
        Call this as a separate Thread !
        :param dir_delay: Time to wait until direction is changed
        :return:
        '''
        global led_state
        time_now = time.time()  # get time when function was called
        while True:  # infinite loop
            if (time.time() > (time_now + dir_delay)):  # When timeout has reached
                time_now = time.time()  # update the start of timer
                self.board.digital_write(pinout["d_LED"], led_state)
                print(f"Blinking LED {led_state}")
                led_state ^= 1
            pass  # else do nothing

# ===============================================================================================================
# ===============================================================================================================

# Create a Telemetrix instance.
# board = telemetrix.Telemetrix()
test = Test()  # Creates an ServOCP test instance
print(f'# Telemetrix instance creation successful\n')
time.sleep(1)

try:

    # background task
    print("# LED Blink")
    # set 'daemon = True' to terminate function when main program exits.
    led = threading.Thread(target=test.LED_blink, args=(0.5,), daemon=True)
    led.start()

    time.sleep(2)

    print("# Read single ADCs")
    print(f'Test acknowledges: {test.read_analog("a_ADC_A0")}') # A0
    time.sleep(1)
    print(f'Test acknowledges: {test.read_analog("a_ADC_A6")}') # A6
    time.sleep(1)
    print(f'Test acknowledges: {test.read_analog("a_ADC_A2")}') # A2
    time.sleep(1)
    print(f'Test acknowledges: {test.read_analog("a_ADC_A3")}') # A3
    # at this point callbacks are very frequent by all analog pins.
    # Although I was interested in the callback at the time of the call, not later.

    time.sleep(2)

    print("# Test script finished")

except KeyboardInterrupt:
    test.board.shutdown()
    sys.exit(0)

finally:
    test.board.shutdown()
    sys.exit(0)