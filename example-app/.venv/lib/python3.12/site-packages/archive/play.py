import struct

data = -2000
position_bytes = (struct.pack("!l", data))

udata = struct.unpack("<l", position_bytes)

int_val = int.from_bytes(cdata, "big")
print(int_val)