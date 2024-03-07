# Möbius Strip Builder for MakeCode Python, with color wool
# @JustinEducation
# 7 March 2024

# Set global variables
playerX = 0
playerY = 0
playerZ = 0

def on_chat():
    # Capture player position
    playerX = player.position().get_value(Axis.X)
    playerY = player.position().get_value(Axis.Y)
    playerZ = player.position().get_value(Axis.Z)
    
    # Define parameters for the Möbius strip
    u_range = 100
    v_range = 100
    strip_width = 10
    strip_radius = 20
    pi=3.14

    # Build the Möbius strip
    for u in range(u_range):
        for v in range(v_range):
            # Calculate parametric equations for the Möbius strip
            x = (1 + 0.5 * (v / v_range) * Math.cos(u / (2 * pi))) * Math.cos(u / (2 * pi))
            y = (1 + 0.5 * (v / v_range) * Math.cos(u / (2 * pi))) * Math.sin(u / (2 * pi))
            z = 0.5 * (v / v_range) * Math.sin(u / (2 * pi))

            # Convert coordinates to Minecraft world coordinates
            build_x = playerX + x * strip_radius
            build_y = playerY + y * strip_radius
            build_z = playerZ + z * strip_radius
            
            # Place blocks in the Minecraft world with different colored wool blocks based on the value of u
            color_index = u % 8
            if color_index == 0:
                builder.teleport_to(world(build_x, build_y, build_z))
                builder.place(RED_WOOL)
            elif color_index == 1:
                builder.teleport_to(world(build_x, build_y, build_z))
                builder.place(GREEN_WOOL)
            elif color_index == 2:
                builder.teleport_to(world(build_x, build_y, build_z))
                builder.place(BLUE_WOOL)
            elif color_index == 3:
                builder.teleport_to(world(build_x, build_y, build_z))
                builder.place(CYAN_WOOL)
            elif color_index == 4:
                builder.teleport_to(world(build_x, build_y, build_z))
                builder.place(PINK_WOOL)
            elif color_index == 5:
                builder.teleport_to(world(build_x, build_y, build_z))
                builder.place(LIME_WOOL)
            elif color_index == 6:
                builder.teleport_to(world(build_x, build_y, build_z))
                builder.place(ORANGE_WOOL)
            else:
                builder.teleport_to(world(build_x, build_y, build_z))
                builder.place(PURPLE_WOOL)

# Call Möbius strip build function
player.on_chat("mobius", on_chat)
