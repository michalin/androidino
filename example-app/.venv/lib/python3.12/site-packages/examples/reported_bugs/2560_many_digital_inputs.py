import time
from telemetrix import telemetrix


class Main:
    def __init__(self):
        self.board = telemetrix.Telemetrix()
        # init password buttons callback
        for i in range(10, 23):
            self.board.set_pin_mode_digital_input_pullup(i, callback=self.ringBack)
            time.sleep(.02)

    def ringBack(self, state):
        print(state)


if __name__ == '__main__':
    game = Main()
    while True:
        time.sleep(0.01)
