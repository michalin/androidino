from telemetrix import telemetrix
import time

board = telemetrix.Telemetrix()
rot_motor = board.set_pin_mode_stepper(interface=1, pin1=11, pin2=12)


def running_callback(data):
    global exit_flag
    exit_flag += 1


def dummy_callback(data):
    pass


exit_flag = 0
board.stepper_move_to(rot_motor, 10)
board.stepper_run(rot_motor, running_callback)
board.stepper_is_running(rot_motor, dummy_callback)
while exit_flag == 0:
    time.sleep(1)
