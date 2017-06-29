import os
import struct

# List to store the count of emoji in each folder
folder_index = {20:0, 32:0, 40:0, 48:0, 64:0, 96:0, 160:0}
writing = False
index = 0

with open("/System/Library/Fonts/Apple Color Emoji.ttc", "rb") as font_file:
    font = font_file.read()

while index < len(font):
    # Find the PNG header
    if font[index:index + 8] == b'\x89PNG\r\n\x1a\n':
        # Get the width of the image for the folder name as an integer
        width = struct.unpack(">I", font[index+16:index+20])[0]
        chunk_size = struct.unpack(">I", font[index+8:index+12])[0] + 20
        folder_name = "{}x{}".format(width, width)

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        writing = True
        out_file = open("{}/{}.png".format(folder_name, folder_index[width]), "wb")
        folder_index[width] += 1

        # Write the header and the IHDR chunk code
        out_file.write(font[index:index + chunk_size])
        index += chunk_size

    # Check for the IEND (Final) block
    elif writing and font[index+4:index+8] == b"IEND":
        chunk_size = struct.unpack(">I", font[index:index+4])[0] + 12
        out_file.write(font[index:index+chunk_size])
        out_file.close()
        writing = False

        index += chunk_size

    # For all blocks between IHDR and IEND
    elif writing:
        chunk_size = struct.unpack(">I", font[index:index+4])[0] + 12
        out_file.write(font[index:index+chunk_size])

        index += chunk_size

    # Traverse while not writing
    else:
        index += 1
