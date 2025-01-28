import sys
import time

from telemetrix import telemetrix




board = telemetrix.Telemetrix()
ENABLE_PIN =  8
board.set_pin_mode_digital_output(pin_number=ENABLE_PIN)
board.digital_write(pin=ENABLE_PIN,value=0)

def the_callback(data):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
    print(f'Motor {data[1]} runSpeedToPosition motion completed at: {date}.')


motor = board.set_pin_mode_stepper(interface=1, pin1=2, pin2=5)
board.stepper_set_max_speed(motor, 800)
board.stepper_move_to(motor, 10)
# board.stepper_set_speed(motor, 400)    #can not use  stepper_set_speed two times


motor1 = board.set_pin_mode_stepper(interface=1, pin1=3, pin2=6)
board.stepper_set_max_speed(motor1, 800)
board.stepper_move_to(motor1, 10)
# board.stepper_set_speed(motor1, 400)




# run the motor
board.stepper_run_speed_to_position(motor, completion_callback=the_callback)
board.stepper_run_speed_to_position(motor1, completion_callback=the_callback)

# keep application running
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)


