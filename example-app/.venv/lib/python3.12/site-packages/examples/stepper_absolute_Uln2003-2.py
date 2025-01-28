"""
 Copyright (c) 2021 Alan Yorinks All rights reserved.

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

import sys
import time

from telemetrix import telemetrix

"""
Run a motor to an absolute position. Server will send a callback notification 
when motion is complete.
"""

# global variables
current_position_complete = False
current_position = None

distance_to_go_complete = False
distance_to_go = None


def distance_to_go_callback(data):
    global distance_to_go_complete, distance_to_go
    distance_to_go = data[2]
    distance_to_go_complete = True


def completion_callback(data):
    print(f'complete: {data}')


def get_current_position(data):
    # print(f' info {data}')
    global current_position, current_position_complete
    current_position = data[2]
    current_position_complete = True


def setup(the_motor, the_board):
    global current_position, current_position_complete
    the_board.stepper_get_current_position(the_motor, get_current_position)
    while not current_position_complete:
        time.sleep(.0001)
    current_position_complete = False
    print(f'Setup: current position = {current_position}')

    the_board.stepper_set_max_speed(the_motor, 1000)
    the_board.stepper_set_acceleration(the_motor, 100)
    the_board.stepper_set_speed(the_motor, 200)
    the_board.stepper_move_to(the_motor, 1024)


def loop(the_motor, the_board):
    global current_position, current_position_complete
    global distance_to_go_complete, distance_to_go
    endpoint = 1024

    while True:
        the_board.stepper_get_distance_to_go(the_motor, distance_to_go_callback)
        while not distance_to_go_complete:
            time.sleep(.0000001)
        distance_to_go_complete = False

        if distance_to_go == 0:
            the_board.stepper_set_current_position(the_motor, 0)
            endpoint = -endpoint
            the_board.stepper_move_to(the_motor, endpoint)
        the_board.stepper_run(the_motor, completion_callback)


# Create a Telemetrix instance.
board = telemetrix.Telemetrix(arduino_wait=4)
motor = board.set_pin_mode_stepper(interface=8, pin1=8, pin2=9, pin3=10, pin4=11)
setup(motor, board)
loop(motor, board)
