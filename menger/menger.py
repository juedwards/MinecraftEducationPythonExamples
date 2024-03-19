# Menger Sponge Builder for MakeCode Python, with color wool
# Adaptation of Möbius Strip Builder Template
# @JustinEducation
# 19 March 2024

# Set global variables
playerX = 0
playerY = 0
playerZ = 0
gameplay.time_set(DayTime.DAY)

def menger_sponge(x, y, z, size, level):
    if level == 0:
        # Place a block at the given position with a random color
        color_index = randint(0, 8)  # Randomly choose a color
        builder.teleport_to(world(x + playerX, y + playerY, z + playerZ))
        # Use a switch or if-else statement to place a block of the chosen color
        if color_index == 0:
            builder.place(WHITE_CONCRETE)
        elif color_index == 1:
            builder.place(BLUE_CONCRETE)
        elif color_index == 2:
            builder.place(LIGHT_BLUE_CONCRETE)
        elif color_index == 3:
            builder.place(RED_CONCRETE)
        elif color_index == 4:
            builder.place(PINK_CONCRETE)
        elif color_index == 5:             
            builder.place(LIME_CONCRETE)
        elif color_index == 6:
            builder.place(ORANGE_CONCRETE)
        elif color_index == 7:
            builder.place(CYAN_CONCRETE)
        else:
            builder.place(PURPLE_CONCRETE)
    else:
        newSize = size / 3
        for dx in range(3):
            for dy in range(3):
                for dz in range(3):
                    if dx == 1 and dy == 1 or dy == 1 and dz == 1 or dz == 1 and dx == 1:
                        continue  # Skip the central cubes of faces and the very center cube
                    menger_sponge(x + dx * newSize, y + dy * newSize, z + dz * newSize, newSize, level - 1)

def on_chat():
    global playerX, playerY, playerZ
    # Capture player position
    playerX = player.position().get_value(Axis.X)
    playerY = player.position().get_value(Axis.Y)
    playerZ = player.position().get_value(Axis.Z)

    # Define parameters for the Menger Sponge
    start_size = 99  # Adjust as needed, but keep in mind performance implications
    recursion_level = 4  # Adjust based on the desired complexity

    # Call the Menger Sponge function to start building
    player.say("Execute Code...")
    menger_sponge(0, 0, 0, start_size, recursion_level)
    player.say("Finished.")

# Bind the Menger Sponge build function to a chat command
player.on_chat("menger", on_chat)

