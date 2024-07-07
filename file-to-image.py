import math
import random
import os.path
import argparse
import numpy as np 

from PIL import Image, ImageColor

def encode_text(filename, rainbow):
    with open(filename, 'r',encoding='utf8') as file:
        text_string = file.read()

    text_binary = ''.join(format(ord(i),'b').zfill(8) for i in text_string)

    side_length = get_square_size(len(text_binary))
    img = Image.new('RGB', (side_length,side_length), color = ImageColor.getrgb("white"))

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
                            if(color != ImageColor.getrgb("white")):
                                break
                    else:
                        color = ImageColor.getrgb("black")
                    img.putpixel((j,i),color)
                    current_pixel += 1

    extension = os.path.splitext(filename)[1][1:]
    img.save(filename.replace(extension,"png"))

def decode_img(filename):
    img = Image.open(filename)
    numpy_array = np.array(img)
    text_binary = ""
    text_binary_array = []
    byte_count = 0

    white = np.array([255, 255, 255])

    for line in numpy_array:
        for pixel in line:
            if(byte_count == 8):
                if(text_binary == "00000000"):
                    return binary_array_to_string(text_binary_array)

                byte_count = 0
                text_binary_array.append(text_binary)
                text_binary = ""

            if(np.array_equal(pixel, white)):
                byte_count += 1
                text_binary += '0'
            else:
                byte_count += 1
                text_binary += '1'

def binary_array_to_string(binary_array):
    characters = []
    for b in binary_array:
        character = chr(int(b, 2))
        if ord(character) < 128:
            characters.append(character)
        else:
            characters.append('?')

    return ''.join(characters)

def get_square_size(x):
    s = math.ceil(math.sqrt(x))
    if s % 8 != 0:
        s += 8 - (s % 8)
    return s

parser = argparse.ArgumentParser(description='file-to-image')
parser.add_argument('-e',type=str, help="file to be encoded")
parser.add_argument('-d',type=str, help="file to be decoded")
parser.add_argument('-r',action=argparse.BooleanOptionalAction, help="enable rainbow")
args = parser.parse_args()

if(args.e and args.r):
    encode_text(args.e, True)
if(args.e and not args.r):
    encode_text(args.e, False)
if(args.d):
    with open("output.txt", "w") as output_file:
        output_file.write(decode_img(args.d))