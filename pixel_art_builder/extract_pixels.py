# Extract Pixels
# @JustinEducation Justin Edwards 14 March 2023
# A python file that opens a PNG file, shrinks the picture to 32x32 pixels and then converts this into an array of Minecraft wool blocks, which can be used
# with the pizel_art_builder.py in Minecraft Education MakeCode Python Interface.
# Recommend use Visual Studio Code to run this code. 
# You will need to install 'pillow' PIP INSTALL PILLOW on your python to run.

from PIL import Image
import numpy as np
import os

# Define the path to the image file
path = r'D:\zombie.png'

# Open the image and resize it to 32 x 32 pixels
image = Image.open(path)
resized_image = image.resize((32, 32))

# Save the resized image with "2" added to the filename
filename, extension = os.path.splitext(path)
new_filename = f"{filename}2{extension}"
resized_image.save(new_filename)

# Convert the resized image to a NumPy array
image_array = np.asarray(resized_image)

# Remove the alpha channel by deleting the fourth element from each pixel array
image_array = np.delete(image_array, 3, axis=2)

# Define the color table
color_table = {
    (255, 255, 255): 'WHITE_WOOL',
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
                closest_name = 'White Wool'
        color_row.append(closest_name)
    color_names.append(color_row)

# Save the color names as a text file with the same name as the amended image item
color_filename = f"{filename}2_colors.txt"
with open(color_filename, 'w') as file:
    for row in color_names:
        file.write(str(row) + '\n')

# Print the results
width, height = resized_image.size
pixels = width * height
print("Width:", width, "pixels")
print("Height:", height, "pixels")
print("Total pixels:", pixels)
print("Color names:")
print(np.array(color_names))
