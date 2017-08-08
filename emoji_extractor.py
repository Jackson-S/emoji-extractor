import re
import os
import sys

if len(sys.argv) == 1:
    # Some versions of OSX store the font as a ttf, and other as ttc.
    font_location = "/System/Library/Fonts/Apple Color Emoji.ttc"
    if not os.path.exists(font_location):
        font_location = font_location[:-1] + "f"
else:
    # If a font file is provided as an argument use it
    font_location = sys.argv[1]

try:
    with open(font_location, "rb") as in_file:
        font = in_file.read()
except FileNotFoundError:
    print("File \"{}\" not found.".format(font_location))
    exit(1)

# This regex should match all PNG files in the emoji font.
pattern = re.compile(b"\x89PNG\r\n\x1a\n.*?IEND", flags=re.DOTALL)

file_number = 0

for item in re.finditer(pattern, font):
    start = item.start()
    end = item.end()
    # Get the ending location of each match, up to the ending of the IEND
    # identifier, then add data and CRC fields
    end += int.from_bytes(font[end-8:end-4], byteorder='big') + 4
    # Get the size (in pixels) of the image, to be used as a folder name
    size = str(int.from_bytes(font[start+16:start+20], byteorder='big'))

    if not os.path.exists(size):
        os.mkdir(size)
        # The apple emoji fonts are laid out by size, so if we haven't
        # encountered that size, reset the file number counter
        file_number = 0

    # Write the output to a folder
    with open(f"{size}/{file_number}.png", "wb") as out_file:
        out_file.write(font[item.start():end])
        file_number += 1
