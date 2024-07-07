import math
import random
import os.path
import argparse
import numpy as np 

from PIL import Image, ImageColor

def encode_file(filename, rainbow, scale):
    with open(filename, 'rb') as file:
        binary_content = file.read()
    text_binary = ''.join(format(byte, '08b') for byte in binary_content)

    side_length = get_square_size(len(text_binary))
    img = Image.new('RGB', (side_length,side_length), color = (254,254,254))

    used_height = 0
    current_pixel = 0

    for i in range(side_length):
        for j in range(side_length):
            if(not (current_pixel >= len(text_binary))):
                if(text_binary[current_pixel] == '0'):
                    color = ImageColor.getrgb("white")
                    img.putpixel((j,i),color)
                    current_pixel += 1
                else:
                    if(rainbow):
                        while (True):
                            color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
                            if(color != ImageColor.getrgb("white") and color != (254,254,254)):
                                break
                    else:
                        color = ImageColor.getrgb("black")
                    img.putpixel((j,i),color)
                    current_pixel += 1
            
            elif(used_height == 0):
                used_height = i+2

    print(used_height)
    extension = os.path.splitext(filename)[1][1:]
    filename_no_extension = filename.split('.')[0]
    img = img.crop((0,0,side_length,used_height))
    img = img.resize((side_length * scale, used_height * scale), Image.NEAREST)
    img.save(filename.replace(extension,"png").replace(filename_no_extension,filename_no_extension + "_converted"))
    

def decode_img(filename, scale):
    img = Image.open(filename)

    width = img.width
    height = img.height

    img = img.resize((int(width * 1/scale), int(height * 1/scale)), Image.NEAREST)

    numpy_array = np.array(img)
    text_binary = ""

    white = np.array([255, 255, 255])
    end = np.array([254, 254, 254])

    for line in numpy_array:
        for pixel in line:
            if(np.array_equal(pixel, end)):
               return text_binary
            elif(np.array_equal(pixel, white)):
                text_binary += '0'
            else:
                text_binary += '1'

def binary_string_to_file(binary_string, filename):
    byte_array = bytearray()
    
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        byte_array.append(int(byte, 2))
    
    with open(filename, 'wb') as file:
        file.write(byte_array)

def get_square_size(x):
    s = math.ceil(math.sqrt(x))
    if s % 8 != 0:
        s += 8 - (s % 8)
    return s

parser = argparse.ArgumentParser(description='file-to-image')
parser.add_argument('-e',type=str, help="File to be encoded")
parser.add_argument('-d',type=str, nargs=2, help="[file to be decoded] [original filetype]")
parser.add_argument('-r',action=argparse.BooleanOptionalAction, help="Enable rainbow")
parser.add_argument('-s',type=int, help="Scale factor. If converted image was scaled then same scale needs to be supplied when decoding")
args = parser.parse_args()

scale = 1

if(args.s):
    scale = args.s

if(args.e and args.r):
    encode_file(args.e, True, scale)
if(args.e and not args.r):
    encode_file(args.e, False, scale)
if(args.d):
    orig_filename = args.d[0].split("_converted")[0] + "_original." + args.d[1]
    binary_string  = decode_img(args.d[0], scale)
    binary_string_to_file(binary_string, orig_filename)