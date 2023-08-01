import struct
import os
import sys
from PIL import Image, ImagePalette
import numpy
from math import ceil

def read_header(file):
    return file.read(4).decode('ascii')

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

class MaskCommand:
    def __init__(self, value):
        self.newline = (value & 0b10000000) != 0;
        self.colored = (value & 0b01000000) != 0;
        self.length = value & 0b00111111;

class ActorImage:
    def __init__(self, width, height, mask_commands, colors):
        self.width = width
        self.height = height
        self.create_data(mask_commands, colors)

    def create_data(self, mask_commands, colors):
        self.data = [(0, 0, 0, 0) for i in range(self.width*self.height)]
        pointer = {'x':0, 'y':0}
        colors_iter = iter(colors)
        for command in mask_commands:
            if command.newline:
                pointer['x'] = 0
                pointer['y'] += 1
            if command.colored:
                for i in range(command.length):
                    color = palette[next(colors_iter)]
                    rgba_color = (color[0], color[1], color[2], 255)
                    pos = pointer['y']*self.width + pointer['x']
                    self.data[pos] = rgba_color
                    pointer['x'] += 1
            else:
                pointer['x'] += command.length

    def save_image(self, index):
        im = Image.new(mode='RGBA', size=(self.width, self.height))
        im.putdata(self.data)
        if not os.path.exists(base_name):
            os.mkdir(base_name)
        filepath = os.path.join(base_name, 'act' + str(index) + ".png")
        im.save(filepath)

base_name = os.path.splitext(sys.argv[1])[0]
palettefile = ''
palette = list()
if len(sys.argv) < 3:
    palettefile = base_name + ".PAL"
else:
    palettefile = sys.argv[2]

if not os.path.exists(palettefile):
    print("Warning: palette " + palettefile + " does not exist. Using grayscale.")
    palette = [(i, i, i) for i in range(256)]
else:
    with open(palettefile, 'br') as palfile:
        for i in range(256):
            palette.append(read_rgb(palfile))

images = list()
with open(sys.argv[1], "br") as picfile:
    header = read_header(picfile)
    if header != "UNC2":
        print("This script supports only UNC2 files, this file is of type: " + header)
        exit()
    image_count = read_u16(picfile)
    total_data_size = read_u32(picfile)
    read_u32(picfile) # unknown
    for pic_index in range(image_count):
        image_width = read_u16(picfile)
        image_height = read_u8(picfile)
        # unknown values
        read_u32(picfile)
        read_u32(picfile)
        read_u8(picfile)
        lines_data_size = read_u16(picfile)
        colors_data_size = read_u16(picfile)
        mask_commands = list()
        for i in range(lines_data_size):
            mask_value = read_u8(picfile)
            mask_commands.append(MaskCommand(mask_value))

        #read_u8(picfile) # empty 0x00 separator

        colors = list()
        for i in range(colors_data_size):
            colors.append(read_u8(picfile))

        image = ActorImage(image_width, image_height, mask_commands, colors)
        image.save_image(pic_index)
