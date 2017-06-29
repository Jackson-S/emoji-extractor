import os
import sys
import struct

def bin_to_int(input_bin):
    return struct.unpack(">I", input_bin)[0]

# List to store the count of emoji in each folder
folder_index = dict()
writing = False
index = 0

if os.path.exists("/System/Library/Fonts/Apple Color Emoji.ttc"):
    font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"
elif os.path.exists("/System/Library/Fonts/Apple Color Emoji.ttf"):
    font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"
else:
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        font_path = sys.argv[1]
    else:
        print("Font not detected, ensure you are running on MacOS or have"
              " the font as the first argument!")
        sys.exit(1)

with open(font_path, "rb") as font_file:
    font = font_file.read()

while index < len(font):
    # Find the PNG header
    if font[index:index + 8] == b'\x89PNG\r\n\x1a\n':
        # Get the width of the image for the folder name as an integer
        width = bin_to_int(font[index+16:index+20])
        chunk_size = bin_to_int(font[index+8:index+12]) + 20

        folder_name = "{}x{}".format(width, width)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        if width not in folder_index:
            folder_index[width] = 0

        path = os.path.join(folder_name, "{}.png".format(folder_index[width]))

        writing = True
        out_file = open(path, "wb")
        folder_index[width] += 1

        # Write the header and the IHDR chunk code
        out_file.write(font[index:index+chunk_size])

        index += chunk_size

    # Check for the IEND (Final) block
    elif writing and font[index+4:index+8] == b"IEND":
        chunk_size = bin_to_int(font[index:index+4]) + 12
        out_file.write(font[index:index+chunk_size])
        out_file.close()
        writing = False

        index += chunk_size

    # For all blocks between IHDR and IEND
    elif writing:
        chunk_size = bin_to_int(font[index:index+4]) + 12
        out_file.write(font[index:index+chunk_size])

        index += chunk_size

    # Traverse while not writing
    else:
        index += 1
