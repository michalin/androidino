stepper_info = {'instance': False, 'is_running': None,
                             'maximum_speed': 1, 'speed': 0, 'acceleration': 0,
                             'distance_to_go_callback': None,
                             'target_position_callback': None,
                             'current_position_callback': None,
                             'is_running_callback': None,
                             'motion_complete_callback': None,
                             'acceleration_callback': None}

stepper_info_list = []

# a list of dictionaries to hold stepper information
for motor in range(8):
    stepper_info_list.append(stepper_info)

stepper_info_list[0]['is_running'] = True

for motor in range(8):
    running = stepper_info_list[motor]['is_running']
    print(f'entry: {motor} value: {running}')
