def write_16_bit_i2c(register, value):
    """
    Write a 16 value to an i2c register
    :param register: i2c register
    :param value: 16 bit value
    :return: None
    """
    msb = value >> 8
    lsb = value & 0xff
    my_board.i2c_write(register, [msb, lsb])
