# Extract Pixels from a PNG file
# @JustinEducation Justin Edwards 15 March 2023
# A python file that opens a PNG file, shrinks the picture to a set size ('x' and 'y') in pixels and then converts this into an array of Minecraft Wool Blocks, which can be used
# with the pixel_art_create.py or pixel_art_withbuilder.py (second one much faster) in Minecraft Education MakeCode Python Interface.
# Recommend use Visual Studio Code to run this particular code. 
# You will need to install 'pillow' (use PIP INSTALL PILLOW) on your python to run code.

from PIL import Image
import numpy as np
import os

# Define the path to the image file
# Here I saved teh image to my local drive.
path = r'D:\pi.png'

# Set dimentions (in pixels and ultimatley in blocks) of the output file
# Builds larger than 100x100 have problems as the builder or agent go out of range. Suggest staying within 100x100 maximum.
x = 16
y = 16

# Open the image and resize it to 16 x 16 pixels
image = Image.open(path)
# The image is inverted to ensure that the build starts at the bottom of the picture, not the top. You could invert the array, but this method is simpler
image = image.rotate(180)
resized_image = image.resize((x, y))

# Check if the mode and size of the images match
if resized_image.mode != 'RGBA':
    resized_image = resized_image.convert('RGBA')

if resized_image.size != (x, y):
    raise ValueError("Resized image size does not match (16, 16)")

# Create a new background image filled with white color
# this manages transparent PNG files.
background = Image.new('RGBA', resized_image.size, (255, 255, 255, 255))

# Save the resized image with "2" added to the filename
filename, extension = os.path.splitext(path)
new_filename = f"{filename}2{extension}"
resized_image.save(new_filename)
resized_image.show()

# Convert the resized image to a NumPy array
image_array = np.asarray(resized_image)

# Remove the alpha channel by deleting the fourth element from each pixel array
image_array = np.delete(image_array, 3, axis=2)

# Define the color table
color_table = {
    # WHITE WOOL does not display in Miencraft Education, so uses AIR instead. AIR causes an error with builder, so this is managed in the pixel_art_create.py file
    (255, 255, 255): 'AIR',
    (255, 128, 0): 'ORANGE_WOOL',
    (255, 0, 255): 'MAGENTA_WOOL',
    (173, 216, 230): 'LIGHT_BLUE_WOOL',
    (255, 255, 0): 'YELLOW_WOOL',
    (191, 255, 0): 'LIME_WOOL',
    (255, 192, 203): 'PINK_WOOL',
    (128, 128, 128): 'GRAY_WOOL',
    (211, 211, 211): 'LIGHT_GRAY_WOOL',
    (0, 255, 255): 'CYAN_WOOL',
    (128, 0, 128): 'PURPLE_WOOL',
    (0, 0, 255): 'BLUE_WOOL',
    (139, 69, 19): 'BROWN_WOOL',
    (0, 128, 0): 'GREEN_WOOL',
    (255, 0, 0): 'RED_WOOL',
    (0, 0, 0): 'BLACK_WOOL'
}

# Convert each RGB value to the nearest color name
color_names = []
for row in image_array:
    color_row = []
    for pixel in row:
        # Find the closest color in the table using the Euclidean distance
        distances = [(np.linalg.norm(pixel - color), name) for color, name in color_table.items()]
        sorted_distances = sorted(distances, key=lambda x: x[0])
        closest_distance, closest_name = sorted_distances[0]
        second_closest_distance, second_closest_name = sorted_distances[1]
        if closest_distance == second_closest_distance:
            # If there's a tie, choose the color with the smallest Euclidean distance to white
            white_distance = np.linalg.norm(pixel - np.array([255, 255, 255]))
            if white_distance < closest_distance:
                closest_name = 'AIR'
        color_row.append(closest_name)
    color_names.append(color_row)

# Save the color names as a text file with the same name as the amended image item
color_filename = f"{filename}2_colors.txt"
with open(color_filename, 'w') as file:
    for i, row in enumerate(color_names):
        if i == 0:
            file.write("[")
        file.write(str(row).replace("'", ""))
        if i == len(color_names) - 1:
            file.write("]")
        else:
            file.write(",\n")

# Print the results
width, height = resized_image.size
pixels = width * height
print("Width:", width, "pixels")
print("Height:", height, "pixels")
print("Total pixels:", pixels)
print("Color names:")
print(np.array(color_names))
