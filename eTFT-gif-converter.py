#!python

# File:                     eTFT-gif-converter.py
# Revision::                0.2
# Last Modified By:         Edward Krayer <github@edwardkrayer.com>
# Last Modified Date:       12.24.2021

# Original Author Notes:
#   VERSION 0.1 - eTFT screens - GIF Converter
#   ALEX ARCE | alex.arce@pm.me - DEC.2020


import os
import re
import glob
import platform

from PIL import Image

import subprocess
import argparse

# --------------------------------------------------------------------

# Windows Default Path (as of 12/24/2021)
IMAGE_MAGICK_DIRECTORY: str = "C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/"
TFT_SCREEN_HEIGHT: int = 240
TFT_SCREEN_WIDTH: int = 320
CURRENT_OS: str = platform.system()
OUTPUT_DIR = ""
COUNT = 0

class AnimationConverter:
    def __init__(self, original_animation, animation_header):
        self.gif = original_animation
        self.anim_header = animation_header

    def get_image_size_total(self, filename):
        img = Image.open(filename)
        total_size = img.width * img.height
        img.close()
        return total_size

    def get_pixel_data(self, filename, file_descriptor):
        img = Image.open(filename)
        if img.mode in ("RGB", "LA") or (
            img.mode == "P" and "transparency" in img.info
        ):
            pixels = list(img.convert("RGB").getdata())
            pixels_len = len(pixels) - 1
            for index, pix in enumerate(pixels):
                rgb565 = ((pix[0] & 0xF8) << 8) + ((pix[1] & 0xFC) << 3) + (pix[2] >> 3)
                if index == pixels_len:
                    file_descriptor.write("0x{:04X}".format(rgb565))
                else:
                    file_descriptor.write("0x{:04X}".format(rgb565))
                    file_descriptor.write(",")
        img.close()

    def generate_frames(self):
        cmd = [
            IMAGE_MAGICK_DIRECTORY + "convert",
            "-resize",
            str(TFT_SCREEN_WIDTH) + "x" + str(TFT_SCREEN_HEIGHT) + "^",
            "-gravity", "center",
            "-extent", str(TFT_SCREEN_WIDTH) + "x" + str(TFT_SCREEN_HEIGHT),
            "-coalesce",
            self.gif,
            OUTPUT_DIR + "/frame_%d.jpg",
        ]
        print(cmd)
        subprocess.call(cmd, shell=False)

    def get_frames_filelist(self):
        filelist = glob.glob(OUTPUT_DIR + "/*.jpg")
        print(filelist)
        filelist.sort(key=lambda f: int(re.sub("\D", "", f)))
        return filelist

    def generate_header_file(self, filelist):
        if len(filelist) > 0:
            fd = open(self.anim_header, "x")
            fd.write("int frames = %d;\n" % len(filelist))

            first_frame = filelist[0]
            img = Image.open(first_frame)
            fd.write("int animation_width = %d;\n" % img.width)
            fd.write("int animation_height = %d;\n" % img.height)
            img.close()

            # const unsigned short PROGMEM animation[][6700]=
            total_size = self.get_image_size_total(first_frame)
            fd.write("const unsigned short PROGMEM animation[][%d] = {\n" % total_size)

            current_block = 0
            last_block = len(filelist)
            for filename in filelist:
                fd.write("{")
                # fd.write("DATA_BLOCK_%d" % current_block)
                self.get_pixel_data(filename, fd)
                if current_block < last_block - 1:
                    fd.write("},\n")
                else:
                    fd.write("}\n")
                current_block = current_block + 1
            fd.write("};")
            fd.close()
            return True
        else:
            return False

    def Generate(self):
        self.generate_frames()
        frames = self.get_frames_filelist()
        ret = self.generate_header_file(frames)
        return ret


# --------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-width", "--width", required=False)
    parser.add_argument("-height", "--height", required=False)
    parser.add_argument("-imdir", "--imagemagickdirectory", required=False)
    args = parser.parse_args()

    gif_file = args.input
    header_file = args.output
    TFT_SCREEN_HEIGHT = args.height or 240
    TFT_SCREEN_WIDTH = args.width or 320

    if (CURRENT_OS == "Windows"):
        IMAGE_MAGICK_DIRECTORY = (
            args.imagemagickdirectory or "C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/"
        )
    elif (CURRENT_OS == "Linux"):
        IMAGE_MAGICK_DIRECTORY = (
            args.imagemagickdirectory or "/usr/bin/"
        )

    OUTPUT_DIR = os.path.splitext(header_file)[0]

    while os.path.exists(OUTPUT_DIR):
        OUTPUT_DIR = os.path.splitext(header_file)[0] + "_" + str(COUNT)
        COUNT += 1

    os.mkdir(OUTPUT_DIR)

    converter = AnimationConverter(gif_file, OUTPUT_DIR + '/' + header_file)
    status = converter.Generate()
    print("[+] Conversion result: %d" % status)

# --------------------------------------------------------------------
