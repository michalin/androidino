import serial
import sys
import time


class NoJson:
    """
    This file sends the equivalent of

    {
          "count": 0,
          "type": "r",
          "device": "i2c",
          "address": 83,
          "register": 232,
          "big_data": 2048,
          "data":[1,2,3,4,5,6]
    }
    across the serial link.

    It takes 1.1878118515014648 seconds to send 1000 packets.
    """

    def __init__(self):
        self.serial_port = serial.Serial('/dev/ttyACM0', 115200,
                                         timeout=1, writeTimeout=0)
        self.serial_port.reset_output_buffer()
        self.serial_port.reset_input_buffer()
        self.start_time = 0
        print('open')

        while True:
            try:
                if self.serial_port.inWaiting():
                    # here we know the size of the packet
                    the_packet_size = int.from_bytes(self.serial_port.read(), "big")
                    # the_packet_size = int(self.serial_port.read())
                    the_packet = self.serial_port.read(the_packet_size)
                    # print(the_packet)
                    # c = self.serial_port.read(14)

                    # retrieve the count within the data received
                    count = the_packet[0:2]
                    #print(f'count {count}')
                    x = int.from_bytes(count, "big")
                    # print(x)
                    if x == 0:
                        self.start_time = time.time()
                    # if x == 255:
                    #     print('here')
                    if x == 999:
                        print(f'Elapsed time: {time.time() - self.start_time}')
                        sys.exit(0)
                else:
                    time.sleep(.000001)
                    # continue
            except OSError:
                pass


NoJson()
