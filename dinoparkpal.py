import struct
import os
import sys
import pickle
from numpy import array, ubyte
from math import ceil

def read_u32(file):
    return struct.unpack('I', file.read(4))[0]

def read_u16(file):
    return struct.unpack('H', file.read(2))[0]

def read_u8(file):
    return struct.unpack('B', file.read(1))[0]

def read_s8(file):
    return struct.unpack('b', file.read(1))[0]

def read_rgb(file):
    return struct.unpack('BBB', file.read(3))

PALETTE_SIZE = 256

base_name = os.path.splitext(sys.argv[1])[0]
index = 0
if len(sys.argv) >= 3:
    index = int(sys.argv[2])

with open(sys.argv[1], "br") as picfile:
    header = picfile.read(4)
    pointers = list()
    pointers.append(read_u32(picfile))
    while (picfile.tell() < pointers[0]):
        pointers.append(read_u32(picfile))
    pic_num = 0
    pointer = pointers[index]
    picfile.seek(pointer)
    image_size = read_u32(picfile)
    image_width = ceil(read_u16(picfile)/2)*2
    image_height = read_u16(picfile)
    palette = list()
    for i in range(PALETTE_SIZE):
        colors = read_rgb(picfile)
        palette += [colors[0]*4, colors[1]*4, colors[2]*4]
    palname = ''
    if index != 0:
        palname = base_name + str(index) + ".PAL"
    else:
        palname = base_name + ".PAL"
    with open(palname, 'bw') as palfile:
        palfile.write(bytearray(palette))
