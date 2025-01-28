import sys
import time

from telemetrix import telemetrix


class ArmServo:
    def __init__ (self, pin, pos=90):
        board.set_pin_mode_servo(pin)
        board.servo_write(pin, pos)

        self.pin = pin
        self.pos = pos

    def read(self):
        return self.pos

    def write(self, new_pos, servo_delay=0.0025):
        print("writing")
        curr_pos = self.pos
        if new_pos == curr_pos:
            return
        elif new_pos < curr_pos:
            for pos in range(curr_pos, new_pos-1, -1):
                board.servo_write(self.pin, pos)
                sleep(servo_delay)
                self.pos = pos
        else:
            for pos in range(curr_pos, new_pos+1):
                board.servo_write(self.pin, pos)
                sleep(servo_delay)
                self.pos = pos

board = telemetrix.Telemetrix()

claw = ArmServo(2)           # red
wrist_rotate = ArmServo(3)   # orange
wrist_up_down = ArmServo(4)  # yellow
elbow = ArmServo(5)          # green
shoulder = ArmServo(6)       # blue
base = ArmServo(7)           # violet