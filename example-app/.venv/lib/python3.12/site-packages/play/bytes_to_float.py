import struct

rList = [92, 15, 149, 66]


list1=[0x64, 0xD8, 0x6E, 0x3F]
# aa=str(bytearray(list1))  # edit: this conversion wasn't needed
aa= bytearray(rList)
print(struct.unpack('<f', aa))


