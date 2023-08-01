import struct
import os
import sys
from PIL import Image, ImagePalette
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

class DinoImage:
    def __init__(self, width, height, palette, data):
        self.width = width
        self.height = height
        self.palette = palette
        self.data = data

    def save_image(self, index):
        if len(self.data) == self.width * self.height:
            newarray = ubyte(array(self.data).reshape(self.height, self.width))
            im = Image.fromarray(newarray, mode='L')
            im.putpalette([4*x for x in self.palette])
            if not os.path.exists(base_name):
                os.mkdir(base_name)
            filepath = os.path.join(base_name, 'pic' + str(index) + ".png")
            im.save(filepath)
        else:
            print("Warning: Couldn't read " + str(index) + "th picture.")

images = list()
with open(sys.argv[1], "br") as picfile:
    header = picfile.read(4)
    pointers = list()
    pointers.append(read_u32(picfile))
    while (picfile.tell() < pointers[0]):
        pointers.append(read_u32(picfile))
    pic_num = 0
    for pointer in pointers:
        picfile.seek(pointer)
        image_size = read_u32(picfile)
        image_width = ceil(read_u16(picfile)/2)*2
        image_height = read_u16(picfile)
        palette = list()
        for i in range(PALETTE_SIZE):
            palette += list(read_rgb(picfile))
        datasize = read_u16(picfile)
        data = list()
        i = 0
        while i < datasize:
            command = read_s8(picfile)
            # uncompressed bytes incoming
            if command >= 0:
                for j in range(command+1):
                    data.append(read_u8(picfile))
                i += command+1
            else:
                length = 1 - command
                color = read_u8(picfile)
                data += [color]*length
                i += 1
            i += 1
        image = DinoImage(image_width, image_height, palette, data)
        image.save_image(pic_num)
        pic_num += 1
