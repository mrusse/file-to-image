import math
import time
import random
import os.path
import argparse
import numpy as np 
from tqdm import tqdm
from PIL import Image, ImageColor
Image.MAX_IMAGE_PIXELS = None

def encode_file(filename, color_options, scale):
    with open(filename, 'rb') as file:
        binary_content = file.read()
    text_binary = ''.join(format(byte, '08b') for byte in binary_content)

    side_length = get_square_size(len(text_binary))
    img = Image.new('RGB', (side_length,side_length), color = (254,254,254))

    used_height = 0
    current_pixel = 0
    fade_counter = 0
    fade_step= math.ceil(side_length/255)

    progress_bar = tqdm(range(side_length), desc = "Encoding file: ", bar_format='{desc}{percentage:3.0f}% |{bar}| Image Line Count: {n_fmt}/{total_fmt}')

    for i in progress_bar:
        for j in range(side_length):
            if(not (current_pixel >= len(text_binary))):
                if(text_binary[current_pixel] == '0'):
                    color = ImageColor.getrgb("white")
                    img.putpixel((j,i),color)
                    current_pixel += 1
                else:
                    if(color_options):
                        while (True):
                            if(color_options[0] == "random"):
                                color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                            elif("fade" in color_options):
                                if(color_options[0] == "fade"):
                                    color = ImageColor.getrgb(color_options[1])
                                else:
                                    color = ImageColor.getrgb(color_options[0])

                                max_index = 0
                                color_list = list(color)

                                for x in range(len(color)):
                                    if(color_list[x] < color_list[max_index]):
                                        max_index = x
                                
                                if(fade_counter == 0):
                                    color_list[max_index] = 0
                                else:
                                    color_list[max_index] = fade_counter
                                
                                color = tuple(color_list)

                                if(color == ImageColor.getrgb("white")):
                                    color = (253,253,253)
                            elif(color_options):
                                if(color_options[0] == "white"):
                                    color = (253,253,253)
                                else:
                                    color = ImageColor.getrgb(color_options[0])
                            if(color != ImageColor.getrgb("white") and color != (254,254,254)):
                                break
                    else:
                        color = ImageColor.getrgb("black")

                    img.putpixel((j,i),color)
                    current_pixel += 1

            elif(used_height == 0):
                used_height = i+2

        if(i % fade_step == 0):
            fade_counter += 1

    extension = os.path.splitext(filename)[1][1:]
    filename_no_extension = filename.split('.')[0]

    if(used_height == 0):
        used_height = side_length
        
    img = img.crop((0,0,side_length,used_height))
    img = img.resize((side_length * scale, used_height * scale), Image.NEAREST)

    if(extension == ""):
        img.save((filename + ".png").replace(filename_no_extension,filename_no_extension + "_converted"))
    else:
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

    progress_bar = tqdm(numpy_array, desc = "Decoding image: ", bar_format='{desc}{percentage:3.0f}% |{bar}| Image Line Count: {n_fmt}/{total_fmt}')

    for line in progress_bar:
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
parser.add_argument('-e', '--encode', type=str, help="File to be encoded")
parser.add_argument('-d', '--decode', type=str, nargs=2, help="[file to be decoded] [original filetype]")
parser.add_argument('-c', '--color', type=str, nargs='+', help="Colour options: random, color, color fade")
parser.add_argument('-s', '--scale', type=int, help="Scale factor. If converted image was scaled then same scale needs to be supplied when decoding")
args = parser.parse_args()

start_time = time.time()

scale = 1
if(args.scale):
    scale = args.scale

if(args.encode and args.color):
    encode_file(args.encode, args.color, scale)
if(args.encode and not args.color):
    encode_file(args.encode, args.color, scale)
if(args.decode):
    orig_filename = args.decode[0].split("_converted")[0].split(".")[0] + "_original." + args.decode[1]
    binary_string  = decode_img(args.decode[0], scale)
    binary_string_to_file(binary_string, orig_filename)

print("\nFinished in: %s seconds!" % '{0:.2f}'.format(time.time() - start_time))